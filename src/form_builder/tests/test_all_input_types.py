"""
Tests for rendering all input types with the form builder rendering system.
"""

from django.test import TestCase
from django.utils.safestring import SafeString

from form_builder import models
from form_builder.rendering.renderer import render_form_input


class FormBuilderAllInputTypesTest(TestCase):
    """
    Test class for rendering all input types.
    """

    def setUp(self):
        """
        Set up the test environment.
        """
        # Create a test form definition
        self.form_definition = models.FormDefinition.objects.create(
            name="Test Form",
            description="A test form for all input types testing"
        )

    def test_render_all_input_types(self):
        """
        Test rendering all supported input types.
        """
        # Create a mock request
        class MockRequest:
            pass
        
        request = MockRequest()
        
        # Test text input
        text_input = models.FormInput.objects.create(
            form_definition=self.form_definition,
            name="test_text",
            label="Test Text",
            input_type="text",
            input_id="test_text_id",
            default_value="Default text"
        )
        
        html = render_form_input(
            form_input=text_input,
            scope={},
            request=request
        )
        
        self.assertIn('type="text"', html)
        self.assertIsInstance(html, SafeString)
        
        # Test paragraph input
        paragraph_input = models.FormInput.objects.create(
            form_definition=self.form_definition,
            name="test_paragraph",
            label="Test Paragraph",
            input_type="paragraph",
            input_id="test_paragraph_id",
            default_value="Default paragraph text"
        )
        
        html = render_form_input(
            form_input=paragraph_input,
            scope={},
            request=request
        )
        
        self.assertIn('textarea', html)
        self.assertIsInstance(html, SafeString)
        
        # Test date input
        date_input = models.FormInput.objects.create(
            form_definition=self.form_definition,
            name="test_date",
            label="Test Date",
            input_type="date",
            input_id="test_date_id",
            default_value="2023-01-01"
        )
        
        html = render_form_input(
            form_input=date_input,
            scope={},
            request=request
        )
        
        self.assertIn('type="date"', html)
        self.assertIsInstance(html, SafeString)
        
        # Test selection input
        selection_input = models.FormInput.objects.create(
            form_definition=self.form_definition,
            name="test_selection",
            label="Test Selection",
            input_type="selection",
            input_id="test_selection_id",
            enum_choices=[
                {"value": "option1", "label": "Option 1"},
                {"value": "option2", "label": "Option 2"}
            ]
        )
        
        html = render_form_input(
            form_input=selection_input,
            scope={},
            request=request
        )
        
        self.assertIn('select', html)
        self.assertIsInstance(html, SafeString)
        
        # Test number input
        number_input = models.FormInput.objects.create(
            form_definition=self.form_definition,
            name="test_number",
            label="Test Number",
            input_type="number",
            input_id="test_number_id",
            default_value="42"
        )
        
        html = render_form_input(
            form_input=number_input,
            scope={},
            request=request
        )
        
        self.assertIn('type="number"', html)
        self.assertIsInstance(html, SafeString)
        
        # Test checkbox input
        checkbox_input = models.FormInput.objects.create(
            form_definition=self.form_definition,
            name="test_checkbox",
            label="Test Checkbox",
            input_type="checkbox",
            input_id="test_checkbox_id",
            default_value="1"
        )
        
        html = render_form_input(
            form_input=checkbox_input,
            scope={},
            request=request
        )
        
        self.assertIn('type="checkbox"', html)
        self.assertIsInstance(html, SafeString)
        
        # Test radio input
        radio_input = models.FormInput.objects.create(
            form_definition=self.form_definition,
            name="test_radio",
            label="Test Radio",
            input_type="radio",
            input_id="test_radio_id",
            enum_choices=[
                {"value": "option1", "label": "Option 1"},
                {"value": "option2", "label": "Option 2"}
            ]
        )
        
        html = render_form_input(
            form_input=radio_input,
            scope={},
            request=request
        )
        
        self.assertIn('type="radio"', html)
        self.assertIsInstance(html, SafeString)
        
        # Test file input
        file_input = models.FormInput.objects.create(
            form_definition=self.form_definition,
            name="test_file",
            label="Test File",
            input_type="file",
            input_id="test_file_id"
        )
        
        html = render_form_input(
            form_input=file_input,
            scope={},
            request=request
        )
        
        self.assertIn('type="file"', html)
        self.assertIsInstance(html, SafeString)
        
        # Test email input
        email_input = models.FormInput.objects.create(
            form_definition=self.form_definition,
            name="test_email",
            label="Test Email",
            input_type="email",
            input_id="test_email_id",
            default_value="test@example.com"
        )
        
        html = render_form_input(
            form_input=email_input,
            scope={},
            request=request
        )
        
        self.assertIn('type="email"', html)
        self.assertIsInstance(html, SafeString)
        
        # Test password input
        password_input = models.FormInput.objects.create(
            form_definition=self.form_definition,
            name="test_password",
            label="Test Password",
            input_type="password",
            input_id="test_password_id",
            default_value="secret123"
        )
        
        html = render_form_input(
            form_input=password_input,
            scope={},
            request=request
        )
        
        self.assertIn('type="password"', html)
        self.assertIsInstance(html, SafeString)

    def test_render_unknown_input_type_fallback(self):
        """
        Test that unknown input types fall back to text input.
        """
        # Create a mock request
        class MockRequest:
            pass
        
        request = MockRequest()
        
        # Test unknown input type
        unknown_input = models.FormInput.objects.create(
            form_definition=self.form_definition,
            name="test_unknown",
            label="Test Unknown",
            input_type="unknown_type",
            input_id="test_unknown_id",
            default_value="Default text"
        )
        
        html = render_form_input(
            form_input=unknown_input,
            scope={},
            request=request
        )
        
        # Should fall back to text input
        self.assertIn('type="text"', html)
        self.assertIsInstance(html, SafeString)