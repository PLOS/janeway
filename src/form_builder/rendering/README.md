# Form Builder Rendering System

This directory contains the implementation of the form builder's rendering system, which converts Django form models into HTML forms.

## Overview

The rendering system provides a flexible way to convert form models into HTML with support for user-defined component overrides while providing default Janeway implementations as fallbacks.

## Components

### `components.py`

Contains default rendering functions for all standard input types:
- Text inputs
- Paragraph (textarea) inputs
- Date inputs
- Selection (dropdown) inputs
- Number inputs
- Checkbox inputs
- Radio button groups
- File inputs
- Email inputs
- Password inputs

Each component function accepts standardized parameters and returns HTML strings representing the rendered inputs.

### `renderer.py`

Contains the main rendering system that handles component resolution, settings-based configuration, and fallback to default components.

Key features:
- Component function resolution based on input type
- Settings-based custom component configuration
- Caching of component functions for performance
- Graceful fallback to default components

### `templatetags/form_builder_tags.py`

Contains Django template tags for rendering form inputs in templates:
- `get_item` filter for accessing dictionary items
- `render_form_input_tag` for rendering form inputs using the component system

## Usage

### Basic Rendering

To render a form input, use the `render_form_input` function:

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

To render a form input in a Django template, use the `render_form_input_tag` template tag:

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

When a custom component is specified, the system will:
1. Try to import the custom component function
2. Use the custom component if successfully imported
3. Fall back to the default component if import fails

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

## Testing

The rendering system includes comprehensive tests:
- `tests/test_rendering_components.py` - Tests for individual component rendering
- `tests/test_renderer.py` - Tests for the main renderer functionality
- `tests/test_template_tags.py` - Tests for the Django template tags

## Accessibility

All default components follow accessibility best practices:
- Proper labeling with `for` and `id` attributes
- ARIA attributes where appropriate
- Keyboard navigation support
- Screen reader compatibility