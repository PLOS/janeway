"""
Tests for the form builder template tags.
"""

from django.test import TestCase
from django.template import Context, Template
from django.utils.safestring import SafeString

from form_builder import models
from form_builder.templatetags.form_builder_tags import get_item, render_form_input_tag


class FormBuilderTemplateTagsTest(TestCase):
    """
    Test class for form builder template tags.
    """

    def setUp(self):
        """
        Set up the test environment.
        """
        # Create a test form definition
        self.form_definition = models.FormDefinition.objects.create(
            name="Test Form",
            description="A test form for template tag testing"
        )

    def test_get_item_filter(self):
        """
        Test the get_item template filter.
        """
        # Test with a dictionary
        dictionary = {"key1": "value1", "key2": "value2"}
        result = get_item(dictionary, "key1")
        self.assertEqual(result, "value1")
        
        # Test with a missing key
        result = get_item(dictionary, "key3")
        self.assertIsNone(result)
        
        # Test with a default value
        dictionary = {"key1": "value1", "key2": "value2"}
        result = get_item(dictionary, "key3")
        self.assertIsNone(result)

    def test_render_form_input_tag(self):
        """
        Test the render_form_input_tag template tag.
        """
        # Create a test form input
        form_input = models.FormInput.objects.create(
            form_definition=self.form_definition,
            name="test_text",
            label="Test Text",
            input_type="text",
            input_id="test_text_id",
            default_value="Default text"
        )
        
        # Create a mock request
        class MockRequest:
            pass
        
        request = MockRequest()
        
        # Create context
        context = Context({
            'request': request,
            'scope': {}
        })
        
        # Render the template tag
        result = render_form_input_tag(context, form_input)
        
        # Check that the result contains expected elements
        self.assertIn('type="text"', result)
        self.assertIn('id="test_text_id"', result)
        self.assertIn('name="test_text"', result)
        self.assertIn('value="Default text"', result)
        self.assertIsInstance(result, SafeString)

    def test_render_form_input_tag_with_errors(self):
        """
        Test the render_form_input_tag template tag with errors.
        """
        # Create a test form input
        form_input = models.FormInput.objects.create(
            form_definition=self.form_definition,
            name="test_text",
            label="Test Text",
            input_type="text",
            input_id="test_text_id"
        )
        
        # Create a mock request
        class MockRequest:
            pass
        
        request = MockRequest()
        
        # Create context with errors
        context = Context({
            'request': request,
            'scope': {},
            'errors': {"test_text": "This field is required."}
        })
        
        # Render the template tag with errors
        result = render_form_input_tag(context, form_input, errors=context['errors'])
        
        # Check that the result contains the error message
        self.assertIn('This field is required.', result)
        self.assertIsInstance(result, SafeString)

    def test_render_form_input_tag_with_form_data(self):
        """
        Test the render_form_input_tag template tag with form data.
        """
        # Create a test form input
        form_input = models.FormInput.objects.create(
            form_definition=self.form_definition,
            name="test_text",
            label="Test Text",
            input_type="text",
            input_id="test_text_id",
            default_value="Default value"
        )
        
        # Create a mock request
        class MockRequest:
            pass
        
        request = MockRequest()
        
        # Create context with form data
        context = Context({
            'request': request,
            'scope': {},
            'form_data': {"test_text": "Submitted value"}
        })
        
        # Render the template tag with form data
        result = render_form_input_tag(context, form_input, form_data=context['form_data'])
        
        # Check that the result contains the submitted value, not the default
        self.assertIn('value="Submitted value"', result)
        self.assertNotIn('value="Default value"', result)
        self.assertIsInstance(result, SafeString)

    def test_template_tag_in_template(self):
        """
        Test using the template tag in an actual Django template.
        """
        # Create a test form input
        form_input = models.FormInput.objects.create(
            form_definition=self.form_definition,
            name="test_text",
            label="Test Text",
            input_type="text",
            input_id="test_text_id",
            default_value="Default text"
        )
        
        # Create a mock request
        class MockRequest:
            pass
        
        request = MockRequest()
        
        # Create template
        template = Template(
            "{% load form_builder_tags %}"
            "{% render_form_input_tag form_input %}"
        )
        
        # Create context
        context = Context({
            'request': request,
            'scope': {},
            'form_input': form_input
        })
        
        # Render the template
        result = template.render(context)
        
        # Check that the result contains expected elements
        self.assertIn('type="text"', result)
        self.assertIn('id="test_text_id"', result)
        self.assertIn('name="test_text"', result)
        self.assertIn('value="Default text"', result)