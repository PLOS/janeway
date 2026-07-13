__copyright__ = "Copyright 2017 Birkbeck, University of London"
__author__ = "Martin Paul Eve & Andy Byers"
__license__ = "AGPL v3"
__maintainer__ = "Birkbeck Centre for Technology and Publishing"

import json

from django.contrib import messages
from django.http import Http404, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.http import require_POST
from django.core.exceptions import ValidationError

from form_builder import models
from form_builder.validation.form_validator import FormValidator
from form_builder.processors.form_processor import FormProcessor
from form_builder.signals import form_submission_processed, form_submission_processing
from security.decorators import has_journal, editor_user_required
from utils.logger import get_logger

logger = get_logger(__name__)


@has_journal
@editor_user_required
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


@editor_user_required
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
            # Save the uploaded file temporarily
            import tempfile
            import os
            
            with tempfile.NamedTemporaryFile(mode='w+b', delete=False, suffix='.json') as temp_file:
                for chunk in json_file.chunks():
                    temp_file.write(chunk)
                temp_file_path = temp_file.name
            
            try:
                # Process the form document using FormProcessor
                processor = FormProcessor()
                result = processor.process_form_document_file(temp_file_path)
                
                if result.success:
                    messages.add_message(
                        request,
                        messages.SUCCESS,
                        f'Form "{result.form_definition.name}" uploaded successfully.',
                    )
                    
                    # Clean up the temporary file
                    os.unlink(temp_file_path)
                    
                    return redirect(reverse("form_builder_list_forms"))
                else:
                    # Handle validation errors
                    error_messages = []
                    for error in result.errors:
                        error_messages.append(str(error))

                    messages.add_message(
                        request,
                        messages.ERROR,
                        f'Form processing failed: {"; ".join(error_messages)}',
                    )
                    logger.error(f'Form processing failed: {"; ".join(error_messages)}')
                    
                    # Clean up the temporary file
                    os.unlink(temp_file_path)
            except Exception as error:
                messages.add_message(
                    request,
                    messages.ERROR,
                    f"Error processing form: {str(error)}",
                )
                logger.error("Error processing form", error)
                
                # Clean up the temporary file
                if 'temp_file_path' in locals():
                    os.unlink(temp_file_path)
        else:
            messages.add_message(
                request,
                messages.ERROR,
                "No file uploaded.",
            )

    template = "admin/form_builder/upload_form.html"
    context = {}

    return render(request, template, context)


@editor_user_required
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


@editor_user_required
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


@editor_user_required
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


@editor_user_required
def render_form(request, form_id):
    """
    Display forms for testing/validation.

    This view renders a form for testing and validation purposes.
    Only staff members can access this view.
    """
    form_definition = get_object_or_404(models.FormDefinition, pk=form_id)

    # Check if the form has role restrictions
    if form_definition.allowed_roles.exists():
        # Get the user's roles for the current journal
        user_roles = request.user.roles.get(request.journal.code, set())
        
        # Get the role names for the allowed roles
        allowed_role_names = set(form_definition.allowed_roles.values_list('slug', flat=True))
        
        # Check if the user has any of the allowed roles
        # Also allow access if the user is staff or journal manager
        if not user_roles.intersection(allowed_role_names) and not (request.user.is_staff or request.user.is_journal_manager(request.journal)):
            messages.add_message(
                request,
                messages.ERROR,
                "You do not have permission to access this form.",
            )
            return redirect(reverse("form_builder_list_forms"))

    template = "admin/form_builder/render_form.html"
    context = {
        "form_definition": form_definition,
    }

    return render(request, template, context)


@editor_user_required
def submit_form(request, form_id):
    """
    Process form submissions and save data to article models.

    This view handles form submissions and maps form inputs to article model fields.
    """
    form_definition = get_object_or_404(models.FormDefinition, pk=form_id)

    # Check if the form has role restrictions
    if form_definition.allowed_roles.exists():
        # Get the user's roles for the current journal
        user_roles = request.user.roles.get(request.journal.code, set())
        
        # Get the role names for the allowed roles
        allowed_role_names = set(form_definition.allowed_roles.values_list('slug', flat=True))
        
        # Check if the user has any of the allowed roles
        # Also allow access if the user is staff or journal manager
        if not user_roles.intersection(allowed_role_names) and not (request.user.is_staff or request.user.is_journal_manager(request.journal)):
            messages.add_message(
                request,
                messages.ERROR,
                "You do not have permission to submit this form.",
            )
            return redirect(reverse("form_builder_list_forms"))

    if request.method == "POST":
        # Send signal that form submission processing is starting
        form_submission_processing.send(sender=submit_form, form_definition=form_definition, request=request)
        
        # Create a new article
        from submission.models import Article, STAGE_UNSUBMITTED
        from journal.models import Journal
        
        # Get the current journal from the request
        journal = request.journal
        
        # Create the article with basic information
        article = Article.objects.create(
            journal=journal,
            owner=request.user,
            stage=STAGE_UNSUBMITTED,
        )
        
        # Define a helper function to set nested attributes
        def set_nested_attribute(obj, attr_path, value):
            """
            Set a nested attribute on an object using dot notation.
            Example: set_nested_attribute(article, 'section.name', 'Test Section')
            """
            attrs = attr_path.split('.')
            for attr in attrs[:-1]:
                obj = getattr(obj, attr)
            setattr(obj, attrs[-1], value)
        
        # Process each form input and map to article fields
        errors = {}
        try:
            for form_input in form_definition.inputs.all():
                variable_name = form_input.variable_to_save_as
                input_value = request.POST.get(form_input.name)
                
                # Only process inputs that have a variable_to_save_as value
                if variable_name:
                    # Handle different data types
                    if form_input.input_type == 'number':
                        try:
                            input_value = int(input_value) if input_value else None
                        except ValueError:
                            errors[form_input.name] = f"Invalid number value: {input_value}"
                            continue
                    elif form_input.input_type == 'date':
                        try:
                            from datetime import datetime
                            input_value = datetime.strptime(input_value, '%Y-%m-%d').date() if input_value else None
                        except ValueError:
                            errors[form_input.name] = f"Invalid date value: {input_value}. Expected format: YYYY-MM-DD"
                            continue
                    elif form_input.input_type == 'boolean':
                        input_value = bool(input_value) if input_value else False
                    
                    # Use the nested attribute setter for all fields
                    try:
                        set_nested_attribute(article, variable_name, input_value)
                    except AttributeError:
                        errors[form_input.name] = f"Invalid attribute path: {variable_name}"
                        logger.error(f"Invalid attribute path: {variable_name}")
        
            # If there are errors, render the form again with errors
            if errors:
                template = "admin/form_builder/render_form.html"
                context = {
                    "form_definition": form_definition,
                    "errors": errors,
                    "form_data": request.POST  # Preserve form data
                }
                return render(request, template, context)
                
            # Save the article with the mapped data
            article.save()
        
            # Integrate with the journal's workflow
            from core.models import Workflow, WorkflowElement
            from submission.models import STAGE_UNSUBMITTED
        
            # Get the journal's submission workflow
            workflow = Workflow.objects.filter(journal=journal, elements__element_name='submission').first()
        
            if workflow:
                # Get the submission workflow element
                workflow_element = workflow.elements.filter(element_name='submission').first()
            
                if workflow_element:
                    # Create initial workflow element for the article
                    from core.models import WorkflowLog
                    WorkflowLog.objects.create(
                        article=article,
                        element=workflow_element,
                        journal=journal,
                    )
        
            # Send signal that form submission processing is complete
            form_submission_processed.send(sender=submit_form, form_definition=form_definition, article=article, request=request)
        
            # Redirect to confirmation page
            template = "admin/form_builder/submission_confirmation.html"
            context = {
                "form_definition": form_definition,
                "article": article,
            }
            return render(request, template, context)
        except Exception as e:
            messages.add_message(
                request,
                messages.ERROR,
                f"Error processing form submission: {str(e)}",
            )
            logger.error(f"Error processing form submission: {str(e)}")
            return redirect(reverse("form_builder_list_forms"))

    # For GET requests, redirect to the render form view
    return redirect(reverse("form_builder_render_form", kwargs={"form_id": form_id}))
