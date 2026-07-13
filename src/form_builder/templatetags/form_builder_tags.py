"""
Template tags for the form builder app.
"""

from django import template

from form_builder.rendering.renderer import render_form_input

register = template.Library()


@register.filter
def get_item(dictionary, key):
    """
    Get an item from a dictionary using the key.
    Usage: {{ dictionary|get_item:key }}
    """
    return dictionary.get(key)


@register.simple_tag(takes_context=True)
def render_form_input_tag(context, form_input, form_data=None, errors=None):
    """
    Template tag to render a form input using the component system.
    
    Args:
        context: Django template context
        form_input: FormInput model instance
        form_data: Submitted form data (for re-rendering with errors)
        errors: Dictionary of field errors
        
    Returns:
        str: HTML string representing the rendered input
    """
    request = context.get('request')
    scope = context.get('scope', {})
    
    return render_form_input(
        form_input=form_input,
        scope=scope,
        request=request,
        form_data=form_data,
        errors=errors
    )