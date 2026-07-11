__copyright__ = "Copyright 2017 Birkbeck, University of London"
__author__ = "Martin Paul Eve & Andy Byers"
__license__ = "AGPL v3"
__maintainer__ = "Birkbeck Centre for Technology and Publishing"

import json

from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.http import Http404, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.http import require_POST

from form_builder import models
from form_builder.validation.form_validator import FormValidator
from security.decorators import has_journal
from utils.logger import get_logger

logger = get_logger(__name__)


@has_journal
@staff_member_required
def list_forms(request):
    """
    Display all created forms.

    This view shows a list of all form definitions in the system.
    Only staff members can access this view.
    """
    forms = models.FormDefinition.objects.all().order_by("-created_date")

    template = "admin/form_builder/list_forms.html"
    context = {
        "forms": forms,
    }

    return render(request, template, context)


@staff_member_required
def upload_form(request):
    """
    Handle JSON form document uploads.

    This view allows staff members to upload a JSON form document
    which will be validated and converted to Django models.
    Only staff members can access this view.
    """
    if request.method == "POST":
        # Handle form upload
        json_file = request.FILES.get("json_file")

        if json_file:
            try:
                # Read and parse the JSON file
                form_data = json.load(json_file)

                # Validate the form document
                validator = FormValidator()
                is_valid, errors = validator.validate_form_document(form_data)

                if is_valid:
                    # Create the form definition
                    form_definition = models.FormDefinition.objects.create(
                        name=form_data.get("name", "Untitled Form"),
                        description=form_data.get("description", ""),
                    )

                    # Create form variables
                    variables = form_data.get("variables", [])
                    for variable_data in variables:
                        models.FormVariable.objects.create(
                            form_definition=form_definition,
                            variable_id=variable_data.get("id"),
                            variable_type=variable_data.get("type", "any"),
                            value=variable_data.get("value", None),
                        )

                    # Create form inputs
                    inputs = form_data.get("inputs", [])
                    for input_data in inputs:
                        # Extract validation rules
                        validation_data = input_data.get("validation", {})
                        validation_rules = validation_data.get("rules", [])

                        # Create the form input
                        form_input = models.FormInput.objects.create(
                            form_definition=form_definition,
                            input_id=input_data.get("id"),
                            name=input_data.get("name"),
                            input_type=input_data.get("type"),
                            enum_choices=input_data.get("enum", None),
                            label=input_data.get("label", ""),
                            help_text=input_data.get("help_text", ""),
                            value=input_data.get("value", None),
                            default_value=input_data.get("default", None),
                            placeholder_value=input_data.get("placeholder", ""),
                            required=input_data.get("required", False),
                            hidden=input_data.get("hidden", False),
                            variable_to_save_as=input_data.get("saveAs"),
                            logic=input_data.get("logic", None),
                            validation=validation_data,
                        )

                        # Create validation rules
                        for rule_data in validation_rules:
                            models.FormValidationRule.objects.create(
                                form_input=form_input,
                                rule_type=rule_data.get("type"),
                                value=rule_data.get("value", None),
                                error_message=rule_data.get("message", ""),
                                condition=rule_data.get("condition", ""),
                            )

                    messages.add_message(
                        request,
                        messages.SUCCESS,
                        f'Form "{form_definition.name}" uploaded successfully.',
                    )

                    return redirect(reverse("form_builder_list_forms"))
                else:
                    # Handle validation errors
                    error_messages = []
                    for error in errors:
                        error_messages.append(str(error))

                    messages.add_message(
                        request,
                        messages.ERROR,
                        f'Form validation failed: {"; ".join(error_messages)}',
                    )
                    logger.error(f'Form validation failed: {"; ".join(error_messages)}')
            except json.JSONDecodeError as error:
                messages.add_message(
                    request,
                    messages.ERROR,
                    "Invalid JSON file uploaded.",
                )
                logger.error("JSON Decoder error encountered", error)
            except Exception as error:
                messages.add_message(
                    request,
                    messages.ERROR,
                    f"Error processing form: {str(error)}",
                )
                logger.error("JSON Decoder error encountered", error)
        else:
            messages.add_message(
                request,
                messages.ERROR,
                "No file uploaded.",
            )

    template = "admin/form_builder/upload_form.html"
    context = {}

    return render(request, template, context)


@staff_member_required
def edit_form(request, form_id):
    """
    Allow modification of existing forms.

    This view allows staff members to edit an existing form definition.
    Only staff members can access this view.
    """
    form_definition = get_object_or_404(models.FormDefinition, pk=form_id)

    # For now, we'll just redirect to the list view since full editing
    # functionality would require a more complex implementation
    messages.add_message(
        request,
        messages.INFO,
        "Form editing is not yet implemented. Please delete and re-upload the form.",
    )

    return redirect(reverse("form_builder_list_forms"))


@staff_member_required
@require_POST
def delete_form(request, form_id):
    """
    Remove forms from the system.

    This view allows staff members to delete an existing form definition.
    Only staff members can access this view.
    """
    form_definition = get_object_or_404(models.FormDefinition, pk=form_id)

    form_name = form_definition.name
    form_definition.delete()

    messages.add_message(
        request,
        messages.SUCCESS,
        f'Form "{form_name}" deleted successfully.',
    )

    return redirect(reverse("form_builder_list_forms"))


@staff_member_required
def download_form(request, form_id):
    """
    Export forms as JSON documents.

    This view allows staff members to download a form definition as a JSON file.
    Only staff members can access this view.
    """
    form_definition = get_object_or_404(models.FormDefinition, pk=form_id)

    # Build the form data structure
    form_data = {
        "name": form_definition.name,
        "description": form_definition.description,
        "variables": [],
        "inputs": [],
    }

    # Add variables
    for variable in form_definition.variables.all():
        form_data["variables"].append(
            {
                "id": variable.variable_id,
                "type": variable.variable_type,
                "value": variable.value,
            }
        )

    # Add inputs
    for form_input in form_definition.inputs.all():
        input_data = {
            "id": form_input.input_id,
            "name": form_input.name,
            "type": form_input.input_type,
            "label": form_input.label,
            "help_text": form_input.help_text,
            "value": form_input.value,
            "default": form_input.default_value,
            "placeholder": form_input.placeholder_value,
            "required": form_input.required,
            "hidden": form_input.hidden,
            "saveAs": form_input.variable_to_save_as,
            "logic": form_input.logic,
        }

        # Add enum choices if they exist
        if form_input.enum_choices:
            input_data["enum"] = form_input.enum_choices

        # Add validation rules if they exist
        if form_input.validation_rules.exists():
            validation_rules = []
            for rule in form_input.validation_rules.all():
                rule_data = {
                    "type": rule.rule_type,
                    "value": rule.value,
                    "message": rule.error_message,
                    "condition": rule.condition,
                }
                validation_rules.append(rule_data)

            input_data["validation"] = {
                "rules": validation_rules,
            }
        elif form_input.validation:
            input_data["validation"] = form_input.validation

        form_data["inputs"].append(input_data)

    # Convert to JSON
    json_data = json.dumps(form_data, indent=2)

    # Create the HTTP response with JSON content
    response = HttpResponse(json_data, content_type="application/json")
    response["Content-Disposition"] = (
        f'attachment; filename="{form_definition.name}.json"'
    )

    return response


@staff_member_required
def render_form(request, form_id):
    """
    Display forms for testing/validation.

    This view renders a form for testing and validation purposes.
    Only staff members can access this view.
    """
    form_definition = get_object_or_404(models.FormDefinition, pk=form_id)

    template = "admin/form_builder/render_form.html"
    context = {
        "form_definition": form_definition,
    }

    return render(request, template, context)
