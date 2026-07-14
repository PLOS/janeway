"""
Default component implementations for rendering form inputs as HTML.

This module provides default rendering functions for all standard input types
supported by the form builder. Each function accepts standardized parameters
and returns HTML strings representing the rendered inputs.
"""

from django.utils.html import escape
from django.utils.safestring import mark_safe


def render_text_input(form_input, scope, request, form_data=None, errors=None, **kwargs):
    """
    Render a text input with all its properties and validation.
    
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
    # Extract properties from form_input
    input_id = form_input.input_id or f"input_{form_input.id}"
    name = form_input.name or ""
    value = form_data.get(name, form_input.default_value) if form_data else form_input.default_value
    required = form_input.required or False
    placeholder = form_input.placeholder_value or ""
    help_text = form_input.help_text or ""
    label = form_input.label or ""
    
    # Render HTML
    html = f'<input type="text" id="{escape(input_id)}" name="{escape(name)}"'
    if value:
        html += f' value="{escape(value)}"'
    if required:
        html += ' required'
    if placeholder:
        html += f' placeholder="{escape(placeholder)}"'
    
    # Add any additional attributes from validation rules
    if form_input.validation_rules.exists():
        for rule in form_input.validation_rules.all():
            if rule.rule_type == "min_length":
                html += f' minlength="{rule.value}"'
            elif rule.rule_type == "max_length":
                html += f' maxlength="{rule.value}"'
            elif rule.rule_type == "pattern":
                html += f' pattern="{rule.value}"'
    
    html += '>'
    
    # Add label
    if label:
        html = f'<label for="{escape(input_id)}">{escape(label)}</label>' + html
    
    # Add help text if present
    if help_text:
        html += f'<p class="help-text">{escape(help_text)}</p>'
    
    # Add error display if needed
    if errors and name in errors:
        html += f'<span class="error">{escape(errors[name])}</span>'
    
    return mark_safe(html)


def render_paragraph_input(form_input, scope, request, form_data=None, errors=None, **kwargs):
    """
    Render a paragraph (textarea) input with all its properties and validation.
    
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
    # Extract properties from form_input
    input_id = form_input.input_id or f"input_{form_input.id}"
    name = form_input.name or ""
    value = form_data.get(name, form_input.default_value) if form_data else form_input.default_value
    required = form_input.required or False
    placeholder = form_input.placeholder_value or ""
    help_text = form_input.help_text or ""
    label = form_input.label or ""
    
    # Render HTML
    html = f'<textarea id="{escape(input_id)}" name="{escape(name)}"'
    if required:
        html += ' required'
    if placeholder:
        html += f' placeholder="{escape(placeholder)}"'
    
    # Add any additional attributes from validation rules
    if form_input.validation_rules.exists():
        for rule in form_input.validation_rules.all():
            if rule.rule_type == "min_length":
                html += f' minlength="{rule.value}"'
            elif rule.rule_type == "max_length":
                html += f' maxlength="{rule.value}"'
    
    html += '>'
    
    if value:
        html += escape(value)
    
    html += '</textarea>'
    
    # Add label
    if label:
        html = f'<label for="{escape(input_id)}">{escape(label)}</label>' + html
    
    # Add help text if present
    if help_text:
        html += f'<p class="help-text">{escape(help_text)}</p>'
    
    # Add error display if needed
    if errors and name in errors:
        html += f'<span class="error">{escape(errors[name])}</span>'
    
    return mark_safe(html)


def render_date_input(form_input, scope, request, form_data=None, errors=None, **kwargs):
    """
    Render a date input with all its properties and validation.
    
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
    # Extract properties from form_input
    input_id = form_input.input_id or f"input_{form_input.id}"
    name = form_input.name or ""
    value = form_data.get(name, form_input.default_value) if form_data else form_input.default_value
    required = form_input.required or False
    placeholder = form_input.placeholder_value or ""
    help_text = form_input.help_text or ""
    label = form_input.label or ""
    
    # Render HTML
    html = f'<input type="date" id="{escape(input_id)}" name="{escape(name)}"'
    if value:
        html += f' value="{escape(value)}"'
    if required:
        html += ' required'
    if placeholder:
        html += f' placeholder="{escape(placeholder)}"'
    
    # Add any additional attributes from validation rules
    if form_input.validation_rules.exists():
        for rule in form_input.validation_rules.all():
            if rule.rule_type == "min_date":
                html += f' min="{rule.value}"'
            elif rule.rule_type == "max_date":
                html += f' max="{rule.value}"'
    
    html += '>'
    
    # Add label
    if label:
        html = f'<label for="{escape(input_id)}">{escape(label)}</label>' + html
    
    # Add help text if present
    if help_text:
        html += f'<p class="help-text">{escape(help_text)}</p>'
    
    # Add error display if needed
    if errors and name in errors:
        html += f'<span class="error">{escape(errors[name])}</span>'
    
    return mark_safe(html)


def render_selection_input(form_input, scope, request, form_data=None, errors=None, **kwargs):
    """
    Render a selection (dropdown) input with all its properties and validation.
    
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
    # Extract properties from form_input
    input_id = form_input.input_id or f"input_{form_input.id}"
    name = form_input.name or ""
    value = form_data.get(name, form_input.default_value) if form_data else form_input.default_value
    required = form_input.required or False
    help_text = form_input.help_text or ""
    enum_choices = form_input.enum_choices or []
    label = form_input.label or ""
    
    # Render HTML
    html = f'<select id="{escape(input_id)}" name="{escape(name)}"'
    if required:
        html += ' required'
    html += '>'
    
    # Add empty option if not required
    if not required:
        html += '<option value="">-- Select --</option>'
    
    # Add options from enum_choices
    for choice in enum_choices:
        option_value = choice.get('value', choice) if isinstance(choice, dict) else choice
        option_label = choice.get('label', option_value) if isinstance(choice, dict) else choice
        selected = ' selected' if str(option_value) == str(value) else ''
        html += f'<option value="{escape(str(option_value))}"{selected}>{escape(str(option_label))}</option>'
    
    html += '</select>'
    
    # Add label
    if label:
        html = f'<label for="{escape(input_id)}">{escape(label)}</label>' + html
    
    # Add help text if present
    if help_text:
        html += f'<p class="help-text">{escape(help_text)}</p>'
    
    # Add error display if needed
    if errors and name in errors:
        html += f'<span class="error">{escape(errors[name])}</span>'
    
    return mark_safe(html)


def render_number_input(form_input, scope, request, form_data=None, errors=None, **kwargs):
    """
    Render a number input with all its properties and validation.
    
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
    # Extract properties from form_input
    input_id = form_input.input_id or f"input_{form_input.id}"
    name = form_input.name or ""
    value = form_data.get(name, form_input.default_value) if form_data else form_input.default_value
    required = form_input.required or False
    placeholder = form_input.placeholder_value or ""
    help_text = form_input.help_text or ""
    label = form_input.label or ""
    
    # Render HTML
    html = f'<input type="number" id="{escape(input_id)}" name="{escape(name)}"'
    if value is not None and value != "":
        html += f' value="{escape(str(value))}"'
    if required:
        html += ' required'
    if placeholder:
        html += f' placeholder="{escape(placeholder)}"'
    
    # Add any additional attributes from validation rules
    if form_input.validation_rules.exists():
        for rule in form_input.validation_rules.all():
            if rule.rule_type == "min_value":
                html += f' min="{rule.value}"'
            elif rule.rule_type == "max_value":
                html += f' max="{rule.value}"'
            elif rule.rule_type == "step":
                html += f' step="{rule.value}"'
    
    html += '>'
    
    # Add label
    if label:
        html = f'<label for="{escape(input_id)}">{escape(label)}</label>' + html
    
    # Add help text if present
    if help_text:
        html += f'<p class="help-text">{escape(help_text)}</p>'
    
    # Add error display if needed
    if errors and name in errors:
        html += f'<span class="error">{escape(errors[name])}</span>'
    
    return mark_safe(html)


def render_checkbox_input(form_input, scope, request, form_data=None, errors=None, **kwargs):
    """
    Render a checkbox input with all its properties and validation.
    
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
    # Extract properties from form_input
    input_id = form_input.input_id or f"input_{form_input.id}"
    name = form_input.name or ""
    value = form_data.get(name) if form_data else None
    checked = value is not None or (form_input.default_value is not None and form_input.default_value != "")
    required = form_input.required or False
    help_text = form_input.help_text or ""
    label = form_input.label or ""
    
    # Render HTML
    html = f'<input type="checkbox" id="{escape(input_id)}" name="{escape(name)}" value="1"'
    if checked:
        html += ' checked'
    if required:
        html += ' required'
    html += '>'
    
    # Add label
    if label:
        html += f'<label for="{escape(input_id)}">{escape(label)}</label>'
    
    # Add help text if present
    if help_text:
        html += f'<p class="help-text">{escape(help_text)}</p>'
    
    # Add error display if needed
    if errors and name in errors:
        html += f'<span class="error">{escape(errors[name])}</span>'
    
    return mark_safe(html)


def render_radio_input(form_input, scope, request, form_data=None, errors=None, **kwargs):
    """
    Render a radio button group with all its properties and validation.
    
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
    # Extract properties from form_input
    input_id = form_input.input_id or f"input_{form_input.id}"
    name = form_input.name or ""
    value = form_data.get(name, form_input.default_value) if form_data else form_input.default_value
    required = form_input.required or False
    help_text = form_input.help_text or ""
    enum_choices = form_input.enum_choices or []
    label = form_input.label or ""
    
    # Render HTML
    html = ""
    
    # Add group label if present
    if label:
        html += f'<fieldset><legend>{escape(label)}</legend>'
    
    # Add radio buttons from enum_choices
    for i, choice in enumerate(enum_choices):
        choice_id = f"{input_id}_{i}"
        choice_value = choice.get('value', choice) if isinstance(choice, dict) else choice
        choice_label = choice.get('label', choice_value) if isinstance(choice, dict) else choice
        checked = ' checked' if str(choice_value) == str(value) else ''
        
        html += f'<input type="radio" id="{escape(choice_id)}" name="{escape(name)}" value="{escape(str(choice_value))}"{checked}'
        if required:
            html += ' required'
        html += '>'
        html += f'<label for="{escape(choice_id)}">{escape(str(choice_label))}</label><br>'
    
    # Close fieldset if we opened one
    if label:
        # Add help text if present
        if help_text:
            html += f'<p class="help-text">{escape(help_text)}</p>'
        html += '</fieldset>'
    else:
        # Add help text if present (outside fieldset)
        if help_text:
            html += f'<p class="help-text">{escape(help_text)}</p>'
    
    # Add error display if needed
    if errors and name in errors:
        html += f'<span class="error">{escape(errors[name])}</span>'
    
    return mark_safe(html)


def render_file_input(form_input, scope, request, form_data=None, errors=None, **kwargs):
    """
    Render a file input with all its properties and validation.
    
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
    # Extract properties from form_input
    input_id = form_input.input_id or f"input_{form_input.id}"
    name = form_input.name or ""
    required = form_input.required or False
    help_text = form_input.help_text or ""
    label = form_input.label or ""
    
    # Render HTML
    html = f'<input type="file" id="{escape(input_id)}" name="{escape(name)}"'
    if required:
        html += ' required'
    
    # Add any additional attributes from validation rules
    if form_input.validation_rules.exists():
        file_types = []
        max_size = None
        for rule in form_input.validation_rules.all():
            if rule.rule_type == "file_types":
                file_types.append(rule.value)
            elif rule.rule_type == "max_size":
                max_size = rule.value
        
        if file_types:
            # Convert to accept attribute format
            accept_types = []
            for file_type in file_types:
                if file_type.startswith('.'):
                    accept_types.append(file_type)
                elif '/' in file_type:
                    accept_types.append(file_type)
                else:
                    accept_types.append(f'.{file_type}')
            html += f' accept="{",".join(accept_types)}"'
        
        # Note: max_size validation would typically be handled with JavaScript
    
    html += '>'
    
    # Add label
    if label:
        html = f'<label for="{escape(input_id)}">{escape(label)}</label>' + html
    
    # Add help text if present
    if help_text:
        html += f'<p class="help-text">{escape(help_text)}</p>'
    
    # Add error display if needed
    if errors and name in errors:
        html += f'<span class="error">{escape(errors[name])}</span>'
    
    return mark_safe(html)


def render_email_input(form_input, scope, request, form_data=None, errors=None, **kwargs):
    """
    Render an email input with all its properties and validation.
    
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
    # Extract properties from form_input
    input_id = form_input.input_id or f"input_{form_input.id}"
    name = form_input.name or ""
    value = form_data.get(name, form_input.default_value) if form_data else form_input.default_value
    required = form_input.required or False
    placeholder = form_input.placeholder_value or ""
    help_text = form_input.help_text or ""
    label = form_input.label or ""
    
    # Render HTML
    html = f'<input type="email" id="{escape(input_id)}" name="{escape(name)}"'
    if value:
        html += f' value="{escape(value)}"'
    if required:
        html += ' required'
    if placeholder:
        html += f' placeholder="{escape(placeholder)}"'
    
    # Add any additional attributes from validation rules
    if form_input.validation_rules.exists():
        for rule in form_input.validation_rules.all():
            if rule.rule_type == "min_length":
                html += f' minlength="{rule.value}"'
            elif rule.rule_type == "max_length":
                html += f' maxlength="{rule.value}"'
            elif rule.rule_type == "pattern":
                html += f' pattern="{rule.value}"'
    
    html += '>'
    
    # Add label
    if label:
        html = f'<label for="{escape(input_id)}">{escape(label)}</label>' + html
    
    # Add help text if present
    if help_text:
        html += f'<p class="help-text">{escape(help_text)}</p>'
    
    # Add error display if needed
    if errors and name in errors:
        html += f'<span class="error">{escape(errors[name])}</span>'
    
    return mark_safe(html)


def render_password_input(form_input, scope, request, form_data=None, errors=None, **kwargs):
    """
    Render a password input with all its properties and validation.
    
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
    # Extract properties from form_input
    input_id = form_input.input_id or f"input_{form_input.id}"
    name = form_input.name or ""
    value = form_data.get(name, form_input.default_value) if form_data else form_input.default_value
    required = form_input.required or False
    placeholder = form_input.placeholder_value or ""
    help_text = form_input.help_text or ""
    label = form_input.label or ""
    
    # Render HTML
    html = f'<input type="password" id="{escape(input_id)}" name="{escape(name)}"'
    if value:
        html += f' value="{escape(value)}"'
    if required:
        html += ' required'
    if placeholder:
        html += f' placeholder="{escape(placeholder)}"'
    
    # Add any additional attributes from validation rules
    if form_input.validation_rules.exists():
        for rule in form_input.validation_rules.all():
            if rule.rule_type == "min_length":
                html += f' minlength="{rule.value}"'
            elif rule.rule_type == "max_length":
                html += f' maxlength="{rule.value}"'
    
    html += '>'
    
    # Add label
    if label:
        html = f'<label for="{escape(input_id)}">{escape(label)}</label>' + html
    
    # Add help text if present
    if help_text:
        html += f'<p class="help-text">{escape(help_text)}</p>'
    
    # Add error display if needed
    if errors and name in errors:
        html += f'<span class="error">{escape(errors[name])}</span>'
    
    return mark_safe(html)


# Default component mapping
DEFAULT_COMPONENTS = {
    'text': render_text_input,
    'paragraph': render_paragraph_input,
    'date': render_date_input,
    'selection': render_selection_input,
    'number': render_number_input,
    'checkbox': render_checkbox_input,
    'radio': render_radio_input,
    'file': render_file_input,
    'email': render_email_input,
    'password': render_password_input,
}