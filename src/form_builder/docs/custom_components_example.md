# Custom Components Example

This document provides an example of how to create and use custom components with the form builder rendering system.

## Creating Custom Components

To create a custom component, you need to define a function that follows the standard component interface:

```python
def custom_component(form_input, scope, request, form_data=None, errors=None, **kwargs):
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
    # Your custom rendering logic here
    return '<input type="text" name="{}" value="Custom rendered">'.format(form_input.name)
```

## Example Custom Component

Here's a complete example of a custom text input component that adds Bootstrap styling:

```python
# myapp/components.py

from django.utils.html import escape
from django.utils.safestring import mark_safe


def render_bootstrap_text_input(form_input, scope, request, form_data=None, errors=None, **kwargs):
    """
    Render a Bootstrap-styled text input.
    """
    # Extract properties from form_input
    input_id = form_input.input_id or f"input_{form_input.id}"
    name = form_input.name or ""
    value = form_data.get(name, form_input.default_value) if form_data else form_input.default_value
    required = form_input.required or False
    placeholder = form_input.placeholder_value or ""
    help_text = form_input.help_text or ""
    label = form_input.label or ""
    
    # Determine CSS classes based on errors
    css_classes = "form-control"
    if errors and name in errors:
        css_classes += " is-invalid"
    
    # Render HTML
    html = ""
    
    # Add label if present
    if label:
        html += f'<label for="{escape(input_id)}">{escape(label)}</label>'
    
    # Add input
    html += f'<input type="text" class="{css_classes}" id="{escape(input_id)}" name="{escape(name)}"'
    if value:
        html += f' value="{escape(value)}"'
    if required:
        html += ' required'
    if placeholder:
        html += f' placeholder="{escape(placeholder)}"'
    html += '>'
    
    # Add help text if present
    if help_text:
        html += f'<div class="form-text">{escape(help_text)}</div>'
    
    # Add error display if needed
    if errors and name in errors:
        html += f'<div class="invalid-feedback">{escape(errors[name])}</div>'
    
    return mark_safe(html)
```

## Configuring Custom Components

To use your custom components, add them to your Django settings:

```python
# settings.py

FORM_BUILDER_COMPONENTS = {
    'text': 'myapp.components.render_bootstrap_text_input',
    # Add other custom components as needed
}
```

## How It Works

1. When rendering a form input, the system first checks the `FORM_BUILDER_COMPONENTS` setting for a custom component function.
2. If a custom component is found, it attempts to import and use that function.
3. If the import fails for any reason, it falls back to the default component.
4. The custom component function is cached for performance.

## Best Practices

1. **Follow the Interface**: Ensure your custom components accept the same parameters as the default components.
2. **Handle Errors Gracefully**: Include error handling in your custom components to prevent crashes.
3. **Use Safe Strings**: Return `mark_safe()` strings from your components to ensure proper HTML rendering.
4. **Maintain Accessibility**: Ensure your custom components follow accessibility best practices.
5. **Test Thoroughly**: Write tests for your custom components to ensure they work correctly in all scenarios.