# Form Builder Rendering System

## Overview

The form builder rendering system provides a flexible way to convert Django form models into HTML forms. It supports user-defined component overrides while providing default Janeway implementations as fallbacks.

## Architecture

The rendering system consists of three main components:

1. **Components** - Default rendering functions for each input type
2. **Renderer** - Main rendering system that resolves components and handles fallbacks
3. **Template Tags** - Django template tags for easy integration

## Components

The `components.py` file contains default rendering functions for all standard input types:

- Text inputs (`text`)
- Paragraph inputs (`paragraph`)
- Date inputs (`date`)
- Selection inputs (`selection`)
- Number inputs (`number`)
- Checkbox inputs (`checkbox`)
- Radio button groups (`radio`)
- File inputs (`file`)
- Email inputs (`email`)
- Password inputs (`password`)

Each component function accepts standardized parameters and returns HTML strings representing the rendered inputs.

## Renderer

The `renderer.py` file contains the main rendering system:

- `FormRenderer` class for rendering form inputs
- `render_form_input` convenience function
- Component function resolution with caching
- Settings-based custom component configuration
- Graceful fallback to default components

## Template Tags

The `templatetags/form_builder_tags.py` file contains Django template tags:

- `get_item` filter for accessing dictionary items
- `render_form_input_tag` for rendering form inputs in templates

## Usage

### Basic Rendering

To render a form input programmatically:

```python
from form_builder.rendering.renderer import render_form_input

html = render_form_input(
    form_input=form_input,
    scope={},
    request=request,
    form_data=form_data,  # Optional
    errors=errors         # Optional
)
```

### In Templates

To render a form input in a Django template:

```django
{% load form_builder_tags %}

{% render_form_input_tag form_input form_data errors %}
```

### Custom Components

To specify custom components, add them to your Django settings:

```python
FORM_BUILDER_COMPONENTS = {
    'text': 'my_custom_app.components.render_fancy_text_input',
    'date': 'my_custom_app.components.render_date_picker_with_calendar',
    # ... other custom components
}
```

## Component Interface

All rendering functions should have a consistent interface:

```python
def render_component(form_input, scope, request, form_data=None, errors=None, **kwargs):
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
    # Implementation here
    pass
```

## Error Handling

The rendering system includes comprehensive error handling:

- Graceful fallback to default components when custom components fail
- Error messages for failed component imports
- Safe string handling for HTML output
- Error display for form validation

## Accessibility

All default components follow accessibility best practices:

- Proper labeling with `for` and `id` attributes
- ARIA attributes where appropriate
- Keyboard navigation support
- Screen reader compatibility

## Testing

The rendering system includes comprehensive tests:

- Individual component rendering tests
- Renderer functionality tests
- Template tag tests
- Integration tests
- All input types tests

## Performance

The rendering system is optimized for performance:

- Component function caching
- Efficient component resolution
- Minimal overhead for default components
- Graceful handling of large forms

## Extending the System

To extend the rendering system:

1. Create custom component functions following the standard interface
2. Add them to the `FORM_BUILDER_COMPONENTS` setting
3. Test thoroughly with various input scenarios
4. Document custom components for other developers

## Troubleshooting

Common issues and solutions:

1. **Custom component not loading**: Check that the module path is correct and the function exists
2. **Fallback to default components**: This happens when custom components fail to import
3. **Missing error messages**: Ensure errors are passed correctly to the rendering functions
4. **Form data not preserved**: Check that form_data is passed correctly to the rendering functions

## Best Practices

1. **Follow the Interface**: Ensure custom components accept the same parameters as default components
2. **Handle Errors Gracefully**: Include error handling in custom components to prevent crashes
3. **Use Safe Strings**: Return `mark_safe()` strings from components to ensure proper HTML rendering
4. **Maintain Accessibility**: Ensure custom components follow accessibility best practices
5. **Test Thoroughly**: Write tests for custom components to ensure they work correctly in all scenarios
6. **Document Custom Components**: Provide clear documentation for custom components for other developers