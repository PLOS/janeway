"""
Main rendering system for converting form models to HTML.

This module provides the core rendering functionality that converts Django form models
into HTML forms. It handles component resolution, settings-based configuration,
and fallback to default components.
"""

from django.conf import settings
from django.utils.module_loading import import_string
from django.utils.safestring import mark_safe

from .components import DEFAULT_COMPONENTS


class FormRenderer:
    """
    Main class for rendering form models to HTML.
    
    This class handles the resolution of appropriate rendering functions for
    form inputs based on their type and user-defined settings, then renders
    the inputs as HTML.
    """
    
    def __init__(self):
        """Initialize the form renderer."""
        self._component_cache = {}
    
    def get_component_function(self, input_type):
        """
        Get the appropriate component function for an input type.
        
        This method first checks user-defined components in settings,
        then falls back to default components.
        
        Args:
            input_type: String representing the input type
            
        Returns:
            Function: The component rendering function
        """
        # Check cache first
        if input_type in self._component_cache:
            return self._component_cache[input_type]
        
        # Check settings for custom component
        custom_components = getattr(settings, 'FORM_BUILDER_COMPONENTS', {})
        if input_type in custom_components:
            try:
                # Import and cache custom component function
                component_func = import_string(custom_components[input_type])
                self._component_cache[input_type] = component_func
                return component_func
            except (ImportError, AttributeError) as e:
                # Log error and fall back to default
                # In a real implementation, you'd want to use proper logging
                print(f"Error importing custom component for {input_type}: {e}")
        
        # Fall back to default component
        component_func = DEFAULT_COMPONENTS.get(input_type, DEFAULT_COMPONENTS.get('text'))
        self._component_cache[input_type] = component_func
        return component_func
    
    def render_input(self, form_input, scope, request, form_data=None, errors=None, **kwargs):
        """
        Render a form input as HTML.
        
        Args:
            form_input: FormInput model instance
            scope: Context data for variable resolution
            request: Django request object
            form_data: Submitted form data (for re-rendering with errors)
            errors: Dictionary of field errors
            **kwargs: Additional context parameters
            
        Returns:
            str: HTML string representing the rendered input
        """
        # Get the appropriate component function
        component_func = self.get_component_function(form_input.input_type)
        
        # Render the input using the component function
        try:
            html = component_func(
                form_input=form_input,
                scope=scope,
                request=request,
                form_data=form_data,
                errors=errors,
                **kwargs
            )
            return html
        except Exception as e:
            # Handle rendering errors gracefully
            # In a real implementation, you'd want to use proper logging
            print(f"Error rendering input {form_input.name}: {e}")
            # Return a simple text input as fallback
            return f'<input type="text" name="{form_input.name}" placeholder="Error rendering input">'


# Global renderer instance
renderer = FormRenderer()


def render_form_input(form_input, scope, request, form_data=None, errors=None, **kwargs):
    """
    Render a form input as HTML using the global renderer.
    
    This is a convenience function that uses the global FormRenderer instance
    to render a form input.
    
    Args:
        form_input: FormInput model instance
        scope: Context data for variable resolution
        request: Django request object
        form_data: Submitted form data (for re-rendering with errors)
        errors: Dictionary of field errors
        **kwargs: Additional context parameters
        
    Returns:
        str: HTML string representing the rendered input
    """
    return renderer.render_input(
        form_input=form_input,
        scope=scope,
        request=request,
        form_data=form_data,
        errors=errors,
        **kwargs
    )