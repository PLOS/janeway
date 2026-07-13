"""
Integration tests for the form builder rendering system.
"""

from django.test import TestCase
from django.template import Context, Template
from django.utils.safestring import SafeString

from form_builder import models


class FormBuilderIntegrationTest(TestCase):
    """
    Integration tests for the form builder rendering system.
    """

    def setUp(self):
        """
        Set up the test environment.
        """
        # Create a test form definition
        self.form_definition = models.FormDefinition.objects.create(
            name="Test Form",
            description="A test form for integration testing"
        )
        
        # Create test form inputs of different types
        self.text_input = models.FormInput.objects.create(
            form_definition=self.form_definition,
            name="test_text",
            label="Test Text",
            input_type="text",
            input_id="test_text_id",
            default_value="Default text",
            required=True
        )
        
        self.number_input = models.FormInput.objects.create(
            form_definition=self.form_definition,
            name="test_number",
            label="Test Number",
            input_type="number",
            input_id="test_number_id",
            default_value="42"
        )
        
        self.email_input = models.FormInput.objects.create(
            form_definition=self.form_definition,
            name="test_email",
            label="Test Email",
            input_type="email",
            input_id="test_email_id",
            default_value="test@example.com"
        )

    def test_render_form_with_template_tag(self):
        """
        Test rendering a complete form using the template tag.
        """
        # Create a mock request
        class MockRequest:
            pass
        
        request = MockRequest()
        
        # Create template that mimics the render_form.html template
        template = Template(
            "{% load form_builder_tags %}"
            "<form>"
            "{% for form_input in form_definition.inputs.all %}"
            "{% render_form_input_tag form_input %}"
            "{% endfor %}"
            "</form>"
        )
        
        # Create context
        context = Context({
            'request': request,
            'scope': {},
            'form_definition': self.form_definition
        })
        
        # Render the template
        result = template.render(context)
        
        # Check that the result contains expected elements for all inputs
        # Text input
        self.assertIn('type="text"', result)
        self.assertIn('id="test_text_id"', result)
        self.assertIn('name="test_text"', result)
        self.assertIn('value="Default text"', result)
        self.assertIn('required', result)
        
        # Number input
        self.assertIn('type="number"', result)
        self.assertIn('id="test_number_id"', result)
        self.assertIn('name="test_number"', result)
        self.assertIn('value="42"', result)
        
        # Email input
        self.assertIn('type="email"', result)
        self.assertIn('id="test_email_id"', result)
        self.assertIn('name="test_email"', result)
        self.assertIn('value="test@example.com"', result)
        
        # Check that result is a safe string
        self.assertIsInstance(result, SafeString)

    def test_render_form_with_errors(self):
        """
        Test rendering a form with errors using the template tag.
        """
        # Create a mock request
        class MockRequest:
            pass
        
        request = MockRequest()
        
        # Create template
        template = Template(
            "{% load form_builder_tags %}"
            "{% render_form_input_tag form_input errors %}"
        )
        
        # Create context with errors
        errors = {"test_text": "This field is required."}
        context = Context({
            'request': request,
            'scope': {},
            'form_input': self.text_input,
            'errors': errors
        })
        
        # Render the template
        result = template.render(context)
        
        # Check that the result contains the error message
        self.assertIn('This field is required.', result)
        self.assertIsInstance(result, SafeString)

    def test_render_form_with_form_data(self):
        """
        Test rendering a form with form data using the template tag.
        """
        # Create a mock request
        class MockRequest:
            pass
        
        request = MockRequest()
        
        # Create template
        template = Template(
            "{% load form_builder_tags %}"
            "{% render_form_input_tag form_input form_data %}"
        )
        
        # Create context with form data
        form_data = {"test_text": "Submitted value"}
        context = Context({
            'request': request,
            'scope': {},
            'form_input': self.text_input,
            'form_data': form_data
        })
        
        # Render the template
        result = template.render(context)
        
        # Check that the result contains the submitted value, not the default
        self.assertIn('value="Submitted value"', result)
        self.assertNotIn('value="Default text"', result)
        self.assertIsInstance(result, SafeString)