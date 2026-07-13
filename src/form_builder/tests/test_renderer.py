"""
Tests for the form builder renderer.
"""

from django.test import TestCase, override_settings
from django.utils.safestring import SafeString

from form_builder import models
from form_builder.rendering.renderer import FormRenderer, render_form_input


class FormBuilderRendererTest(TestCase):
    """
    Test class for form builder renderer.
    """

    def setUp(self):
        """
        Set up the test environment.
        """
        # Create a test form definition
        self.form_definition = models.FormDefinition.objects.create(
            name="Test Form",
            description="A test form for renderer testing"
        )

    def test_get_component_function_default(self):
        """
        Test getting a default component function.
        """
        renderer = FormRenderer()
        
        # Test text input
        component_func = renderer.get_component_function('text')
        from form_builder.rendering.components import render_text_input
        self.assertEqual(component_func, render_text_input)
        
        # Test number input
        component_func = renderer.get_component_function('number')
        from form_builder.rendering.components import render_number_input
        self.assertEqual(component_func, render_number_input)

    @override_settings(FORM_BUILDER_COMPONENTS={
        'text': 'form_builder.tests.test_renderer.custom_text_renderer'
    })
    def test_get_component_function_custom(self):
        """
        Test getting a custom component function from settings.
        """
        renderer = FormRenderer()
        
        # Test custom text input
        component_func = renderer.get_component_function('text')
        # Should be our custom function
        self.assertEqual(component_func.__name__, 'custom_text_renderer')

    def test_get_component_function_fallback(self):
        """
        Test that the renderer falls back to default components for unknown types.
        """
        renderer = FormRenderer()
        
        # Test unknown input type
        component_func = renderer.get_component_function('unknown_type')
        from form_builder.rendering.components import render_text_input
        # Should fall back to text input
        self.assertEqual(component_func, render_text_input)

    def test_render_input(self):
        """
        Test rendering a form input.
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
        
        # Render the input
        html = render_form_input(
            form_input=form_input,
            scope={},
            request=None
        )
        
        # Check that the HTML contains expected elements
        self.assertIn('type="text"', html)
        self.assertIn('id="test_text_id"', html)
        self.assertIn('name="test_text"', html)
        self.assertIn('value="Default text"', html)
        self.assertIsInstance(html, SafeString)

    def test_render_input_with_errors(self):
        """
        Test rendering a form input with errors.
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
        html = render_form_input(
            form_input=form_input,
            scope={},
            request=None,
            errors=errors
        )
        
        # Check that the HTML contains the error message
        self.assertIn('This field is required.', html)
        self.assertIsInstance(html, SafeString)

    def test_render_input_with_form_data(self):
        """
        Test rendering a form input with form data.
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
        html = render_form_input(
            form_input=form_input,
            scope={},
            request=None,
            form_data=form_data
        )
        
        # Check that the HTML contains the submitted value, not the default
        self.assertIn('value="Submitted value"', html)
        self.assertNotIn('value="Default value"', html)
        self.assertIsInstance(html, SafeString)


def custom_text_renderer(form_input, scope, request, form_data=None, errors=None, **kwargs):
    """
    A custom text renderer for testing purposes.
    """
    return f'<input type="text" name="{form_input.name}" value="Custom rendered">'