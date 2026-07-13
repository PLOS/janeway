"""
Tests for the form builder rendering components.
"""

from django.test import TestCase
from django.utils.safestring import SafeString

from form_builder import models
from form_builder.rendering.components import (
    render_text_input,
    render_paragraph_input,
    render_date_input,
    render_selection_input,
    render_number_input,
    render_checkbox_input,
    render_radio_input,
    render_file_input,
    render_email_input,
    render_password_input,
)


class FormBuilderRenderingComponentsTest(TestCase):
    """
    Test class for form builder rendering components.
    """

    def setUp(self):
        """
        Set up the test environment.
        """
        # Create a test form definition
        self.form_definition = models.FormDefinition.objects.create(
            name="Test Form",
            description="A test form for rendering component testing"
        )

    def test_render_text_input(self):
        """
        Test rendering a text input.
        """
        # Create a test form input
        form_input = models.FormInput.objects.create(
            form_definition=self.form_definition,
            name="test_text",
            label="Test Text",
            input_type="text",
            input_id="test_text_id",
            default_value="Default text",
            required=True,
            placeholder_value="Enter text here"
        )
        
        # Render the input
        html = render_text_input(
            form_input=form_input,
            scope={},
            request=None
        )
        
        # Check that the HTML contains expected elements
        self.assertIn('type="text"', html)
        self.assertIn('id="test_text_id"', html)
        self.assertIn('name="test_text"', html)
        self.assertIn('value="Default text"', html)
        self.assertIn('required', html)
        self.assertIn('placeholder="Enter text here"', html)
        self.assertIsInstance(html, SafeString)

    def test_render_paragraph_input(self):
        """
        Test rendering a paragraph (textarea) input.
        """
        # Create a test form input
        form_input = models.FormInput.objects.create(
            form_definition=self.form_definition,
            name="test_paragraph",
            label="Test Paragraph",
            input_type="paragraph",
            input_id="test_paragraph_id",
            default_value="Default paragraph text",
            required=True,
            placeholder_value="Enter paragraph here"
        )
        
        # Render the input
        html = render_paragraph_input(
            form_input=form_input,
            scope={},
            request=None
        )
        
        # Check that the HTML contains expected elements
        self.assertIn('textarea', html)
        self.assertIn('id="test_paragraph_id"', html)
        self.assertIn('name="test_paragraph"', html)
        self.assertIn('required', html)
        self.assertIn('Enter paragraph here', html)
        self.assertIn('Default paragraph text', html)
        self.assertIsInstance(html, SafeString)

    def test_render_date_input(self):
        """
        Test rendering a date input.
        """
        # Create a test form input
        form_input = models.FormInput.objects.create(
            form_definition=self.form_definition,
            name="test_date",
            label="Test Date",
            input_type="date",
            input_id="test_date_id",
            default_value="2023-01-01",
            required=True
        )
        
        # Render the input
        html = render_date_input(
            form_input=form_input,
            scope={},
            request=None
        )
        
        # Check that the HTML contains expected elements
        self.assertIn('type="date"', html)
        self.assertIn('id="test_date_id"', html)
        self.assertIn('name="test_date"', html)
        self.assertIn('value="2023-01-01"', html)
        self.assertIn('required', html)
        self.assertIsInstance(html, SafeString)

    def test_render_selection_input(self):
        """
        Test rendering a selection (dropdown) input.
        """
        # Create a test form input
        form_input = models.FormInput.objects.create(
            form_definition=self.form_definition,
            name="test_selection",
            label="Test Selection",
            input_type="selection",
            input_id="test_selection_id",
            required=True,
            enum_choices=[
                {"value": "option1", "label": "Option 1"},
                {"value": "option2", "label": "Option 2"},
                {"value": "option3", "label": "Option 3"}
            ]
        )
        
        # Render the input
        html = render_selection_input(
            form_input=form_input,
            scope={},
            request=None
        )
        
        # Check that the HTML contains expected elements
        self.assertIn('select', html)
        self.assertIn('id="test_selection_id"', html)
        self.assertIn('name="test_selection"', html)
        self.assertIn('required', html)
        self.assertIn('option1', html)
        self.assertIn('Option 1', html)
        self.assertIn('option2', html)
        self.assertIn('Option 2', html)
        self.assertIn('option3', html)
        self.assertIn('Option 3', html)
        self.assertIsInstance(html, SafeString)

    def test_render_number_input(self):
        """
        Test rendering a number input.
        """
        # Create a test form input
        form_input = models.FormInput.objects.create(
            form_definition=self.form_definition,
            name="test_number",
            label="Test Number",
            input_type="number",
            input_id="test_number_id",
            default_value="42",
            required=True
        )
        
        # Render the input
        html = render_number_input(
            form_input=form_input,
            scope={},
            request=None
        )
        
        # Check that the HTML contains expected elements
        self.assertIn('type="number"', html)
        self.assertIn('id="test_number_id"', html)
        self.assertIn('name="test_number"', html)
        self.assertIn('value="42"', html)
        self.assertIn('required', html)
        self.assertIsInstance(html, SafeString)

    def test_render_checkbox_input(self):
        """
        Test rendering a checkbox input.
        """
        # Create a test form input
        form_input = models.FormInput.objects.create(
            form_definition=self.form_definition,
            name="test_checkbox",
            label="Test Checkbox",
            input_type="checkbox",
            input_id="test_checkbox_id",
            default_value="1",
            required=True
        )
        
        # Render the input
        html = render_checkbox_input(
            form_input=form_input,
            scope={},
            request=None
        )
        
        # Check that the HTML contains expected elements
        self.assertIn('type="checkbox"', html)
        self.assertIn('id="test_checkbox_id"', html)
        self.assertIn('name="test_checkbox"', html)
        self.assertIn('checked', html)
        self.assertIn('required', html)
        self.assertIsInstance(html, SafeString)

    def test_render_radio_input(self):
        """
        Test rendering a radio button group.
        """
        # Create a test form input
        form_input = models.FormInput.objects.create(
            form_definition=self.form_definition,
            name="test_radio",
            label="Test Radio",
            input_type="radio",
            input_id="test_radio_id",
            required=True,
            enum_choices=[
                {"value": "option1", "label": "Option 1"},
                {"value": "option2", "label": "Option 2"}
            ]
        )
        
        # Render the input
        html = render_radio_input(
            form_input=form_input,
            scope={},
            request=None
        )
        
        # Check that the HTML contains expected elements
        self.assertIn('type="radio"', html)
        self.assertIn('name="test_radio"', html)
        self.assertIn('required', html)
        self.assertIn('option1', html)
        self.assertIn('Option 1', html)
        self.assertIn('option2', html)
        self.assertIn('Option 2', html)
        self.assertIsInstance(html, SafeString)

    def test_render_file_input(self):
        """
        Test rendering a file input.
        """
        # Create a test form input
        form_input = models.FormInput.objects.create(
            form_definition=self.form_definition,
            name="test_file",
            label="Test File",
            input_type="file",
            input_id="test_file_id",
            required=True
        )
        
        # Render the input
        html = render_file_input(
            form_input=form_input,
            scope={},
            request=None
        )
        
        # Check that the HTML contains expected elements
        self.assertIn('type="file"', html)
        self.assertIn('id="test_file_id"', html)
        self.assertIn('name="test_file"', html)
        self.assertIn('required', html)
        self.assertIsInstance(html, SafeString)

    def test_render_email_input(self):
        """
        Test rendering an email input.
        """
        # Create a test form input
        form_input = models.FormInput.objects.create(
            form_definition=self.form_definition,
            name="test_email",
            label="Test Email",
            input_type="email",
            input_id="test_email_id",
            default_value="test@example.com",
            required=True
        )
        
        # Render the input
        html = render_email_input(
            form_input=form_input,
            scope={},
            request=None
        )
        
        # Check that the HTML contains expected elements
        self.assertIn('type="email"', html)
        self.assertIn('id="test_email_id"', html)
        self.assertIn('name="test_email"', html)
        self.assertIn('value="test@example.com"', html)
        self.assertIn('required', html)
        self.assertIsInstance(html, SafeString)

    def test_render_password_input(self):
        """
        Test rendering a password input.
        """
        # Create a test form input
        form_input = models.FormInput.objects.create(
            form_definition=self.form_definition,
            name="test_password",
            label="Test Password",
            input_type="password",
            input_id="test_password_id",
            default_value="secret123",
            required=True
        )
        
        # Render the input
        html = render_password_input(
            form_input=form_input,
            scope={},
            request=None
        )
        
        # Check that the HTML contains expected elements
        self.assertIn('type="password"', html)
        self.assertIn('id="test_password_id"', html)
        self.assertIn('name="test_password"', html)
        self.assertIn('value="secret123"', html)
        self.assertIn('required', html)
        self.assertIsInstance(html, SafeString)

    def test_render_with_errors(self):
        """
        Test rendering an input with errors.
        """
        # Create a test form input
        form_input = models.FormInput.objects.create(
            form_definition=self.form_definition,
            name="test_text",
            label="Test Text",
            input_type="text",
            input_id="test_text_id"
        )
        
        # Render the input with errors
        errors = {"test_text": "This field is required."}
        html = render_text_input(
            form_input=form_input,
            scope={},
            request=None,
            errors=errors
        )
        
        # Check that the HTML contains the error message
        self.assertIn('This field is required.', html)
        self.assertIsInstance(html, SafeString)

    def test_render_with_form_data(self):
        """
        Test rendering an input with form data.
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
        
        # Render the input with form data
        form_data = {"test_text": "Submitted value"}
        html = render_text_input(
            form_input=form_input,
            scope={},
            request=None,
            form_data=form_data
        )
        
        # Check that the HTML contains the submitted value, not the default
        self.assertIn('value="Submitted value"', html)
        self.assertNotIn('value="Default value"', html)
        self.assertIsInstance(html, SafeString)