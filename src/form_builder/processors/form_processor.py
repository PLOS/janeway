"""
Form Processor Module

This module provides functionality to process form documents by parsing JSON,
validating against a schema, and converting to Django models.
"""

import json
import logging
from typing import Dict, Any, List, Tuple, Optional
from django.db import transaction
from form_builder.models import (
    FormDefinition,
    FormVariable,
    FormInput,
    FormValidationRule,
)
from form_builder.validation.form_validator import FormValidator
from form_builder.signals import form_processed, form_processing


# Custom exceptions for different error types
class FormValidationError(Exception):
    """Exception raised for schema validation errors."""

    pass


class FormProcessingError(Exception):
    """Exception raised for general processing errors."""

    pass


class FormPersistenceError(Exception):
    """Exception raised for database operation errors."""

    pass


class FormProcessorResult:
    """
    Standardized result object for form processing operations.

    Attributes:
        success (bool): Whether the operation was successful
        form_definition (Optional[FormDefinition]): The processed form definition
        errors (List[str]): List of error messages
    """

    def __init__(
        self,
        success: bool,
        form_definition: Optional[FormDefinition] = None,
        errors: List[str] = None,
    ):
        self.success = success
        self.form_definition = form_definition
        self.errors = errors or []


class FormProcessor:
    """
    A class to process form documents by parsing JSON, validating against a schema,
    and converting to Django models.

    Attributes:
        validator (FormValidator): Instance of the form validator
    """

    def __init__(self, schema_path: str = None):
        """
        Initialize the FormProcessor with a form validator.

        Args:
            schema_path (str, optional): Path to the JSON schema file.
        """
        self.validator = FormValidator(schema_path)
        self.logger = logging.getLogger(__name__)

    def process_form_document(self, document: Dict[str, Any]) -> FormProcessorResult:
        """
        Process a form document by parsing, validating, and converting to Django models.

        Args:
            document (Dict[str, Any]): The form document to process.

        Returns:
            FormProcessorResult: Result object indicating success or failure.
        """
        try:
            # Send signal that form processing is starting
            form_processing.send(sender=self.__class__, document=document)

            # Step 1: Validate the form document against the schema
            is_valid, errors = self.validator.validate_form_document(document)
            if not is_valid:
                self.logger.error(f"Form validation failed: {errors}")
                return FormProcessorResult(
                    success=False,
                    errors=[f"FormValidationError: {error}" for error in errors],
                )

            # Step 2: Convert the validated document to Django models
            form_definition = self._convert_to_models(document)

            # Step 3: Save the models to the database
            self._save_models(form_definition, document.get("id"))

            # Send signal that form processing is complete
            form_processed.send(sender=self.__class__, form_definition=form_definition)

            self.logger.info(f"Successfully processed form: {form_definition.name}")
            return FormProcessorResult(success=True, form_definition=form_definition)

        except FormValidationError as e:
            self.logger.error(f"Form validation error: {str(e)}")
            return FormProcessorResult(
                success=False, errors=[f"FormValidationError: {str(e)}"]
            )
        except FormProcessingError as e:
            self.logger.error(f"Form processing error: {str(e)}")
            return FormProcessorResult(
                success=False, errors=[f"FormProcessingError: {str(e)}"]
            )
        except FormPersistenceError as e:
            self.logger.error(f"Form persistence error: {str(e)}")
            return FormProcessorResult(
                success=False, errors=[f"FormPersistenceError: {str(e)}"]
            )
        except Exception as e:
            self.logger.error(f"Unexpected error during form processing: {str(e)}")
            return FormProcessorResult(
                success=False, errors=[f"Unexpected error: {str(e)}"]
            )

    def process_form_document_file(self, file_path: str) -> FormProcessorResult:
        """
        Process a form document file by parsing, validating, and converting to Django models.

        Args:
            file_path (str): Path to the form document file (JSON format).

        Returns:
            FormProcessorResult: Result object indicating success or failure.
        """
        try:
            with open(file_path, "r") as file:
                document = json.load(file)

            # Send signal that form processing is starting
            form_processing.send(
                sender=self.__class__, document=document, file_path=file_path
            )

            result = self.process_form_document(document)

            # If processing was successful, send signal that form processing is complete
            if result.success:
                form_processed.send(
                    sender=self.__class__,
                    form_definition=result.form_definition,
                    file_path=file_path,
                )

            return result
        except FileNotFoundError:
            error_msg = f"Form document file not found at {file_path}"
            self.logger.error(error_msg)
            return FormProcessorResult(success=False, errors=[error_msg])
        except json.JSONDecodeError as e:
            error_msg = f"Invalid JSON in form document file: {e.msg}"
            self.logger.error(error_msg)
            return FormProcessorResult(success=False, errors=[error_msg])
        except Exception as e:
            error_msg = f"Unexpected error while reading form document file: {str(e)}"
            self.logger.error(error_msg)
            return FormProcessorResult(success=False, errors=[error_msg])

    def _convert_to_models(self, document: Dict[str, Any]) -> FormDefinition:
        """
        Convert a validated form document to Django models.

        Args:
            document (Dict[str, Any]): The validated form document.

        Returns:
            FormDefinition: The created FormDefinition instance.

        Raises:
            FormProcessingError: If there's an error during conversion.
        """
        try:
            # Create the main FormDefinition
            metadata = document.get("metadata", {})

            form_definition = FormDefinition(
                name=metadata.get("name", ""),
                description=metadata.get("description", ""),
            )

            # Process variables if they exist
            variables_data = document.get("variables", [])
            form_variables = []
            for var_data in variables_data:
                form_variable = FormVariable(
                    form_definition=form_definition,
                    variable_id=var_data.get("id", ""),
                    variable_type=var_data.get("type", "any"),
                    value=(
                        str(var_data.get("value", ""))
                        if var_data.get("value") is not None
                        else None
                    ),
                )
                form_variables.append(form_variable)

            # Process inputs
            inputs_data = document.get("inputs", [])
            form_inputs = []
            form_validation_rules = []

            for input_data in inputs_data:
                form_input = FormInput(
                    form_definition=form_definition,
                    input_id=input_data.get("id"),
                    name=input_data.get("name"),
                    input_type=input_data.get("type"),
                    enum_choices=input_data.get("enum"),
                    label=input_data.get("label"),
                    help_text=input_data.get("helpText"),
                    value=(
                        str(input_data.get("value", ""))
                        if input_data.get("value") is not None
                        else None
                    ),
                    default_value=(
                        str(input_data.get("defaultValue", ""))
                        if input_data.get("defaultValue") is not None
                        else None
                    ),
                    placeholder_value=input_data.get("placeholderValue"),
                    required=input_data.get("required", False),
                    hidden=input_data.get("hidden", False),
                    variable_to_save_as=input_data.get("variableToSaveAs"),
                    logic=input_data.get("logic"),
                    validation=input_data.get("validation"),
                )
                form_inputs.append(form_input)

                # Process validation rules if they exist
                validation_data = input_data.get("validation", [])
                for validation_rule in validation_data:
                    rule_data = validation_rule.get("rule", {})
                    form_validation_rule = FormValidationRule(
                        form_input=form_input,
                        rule_type=rule_data.get("type"),
                        value=(
                            str(rule_data.get("value", ""))
                            if rule_data.get("value") is not None
                            else None
                        ),
                        error_message=rule_data.get("error", ""),
                        condition=validation_rule.get("condition", ""),
                    )
                    form_validation_rules.append(form_validation_rule)

            # Attach related objects to the form definition for saving later
            form_definition.variables_data = form_variables
            form_definition.inputs_data = form_inputs
            form_definition.validation_rules_data = form_validation_rules

            return form_definition

        except Exception as e:
            raise FormProcessingError(f"Error converting document to models: {str(e)}")

    def _save_models(
        self, form_definition: FormDefinition, form_id: str = None
    ) -> None:
        """
        Save the form definition and related models to the database.

        Args:
            form_definition (FormDefinition): The form definition to save.
            form_id (str, optional): The ID of an existing form to update.

        Raises:
            FormPersistenceError: If there's an error during saving.
        """
        try:
            with transaction.atomic():
                # Check if we're updating an existing form
                if form_id:
                    try:
                        existing_form = FormDefinition.objects.get(id=form_id)
                        # Update the existing form
                        existing_form.name = form_definition.name
                        existing_form.description = form_definition.description
                        existing_form.save()

                        # Update related objects
                        form_definition.id = existing_form.id
                        form_definition.created_date = existing_form.created_date
                        form_definition.modified_date = existing_form.modified_date
                    except FormDefinition.DoesNotExist:
                        # If the form doesn't exist, create a new one with the specified ID
                        form_definition.id = form_id
                        form_definition.save()
                else:
                    # Create a new form
                    form_definition.save()

                # Save variables
                if hasattr(form_definition, "variables_data"):
                    # Clear existing variables if updating
                    if form_id:
                        FormVariable.objects.filter(
                            form_definition=form_definition
                        ).delete()

                    for variable in form_definition.variables_data:
                        variable.form_definition = form_definition
                        variable.save()

                # Save inputs
                if hasattr(form_definition, "inputs_data"):
                    # Clear existing inputs and validation rules if updating
                    if form_id:
                        inputs = FormInput.objects.filter(
                            form_definition=form_definition
                        )
                        # Delete validation rules first due to foreign key constraints
                        FormValidationRule.objects.filter(
                            form_input__in=inputs
                        ).delete()
                        inputs.delete()

                    for input_obj in form_definition.inputs_data:
                        input_obj.form_definition = form_definition
                        input_obj.save()

                        # Save validation rules for this input
                        if hasattr(form_definition, "validation_rules_data"):
                            for rule in form_definition.validation_rules_data:
                                if rule.form_input == input_obj:
                                    rule.form_input = input_obj
                                    rule.save()

        except Exception as e:
            raise FormPersistenceError(f"Error saving models to database: {str(e)}")


def main():
    """
    Main function to demonstrate the usage of FormProcessor.
    """
    # Example usage
    processor = FormProcessor()

    # Example valid form document
    valid_document = {
        "metadata": {
            "name": "Sample Form",
            "description": "A sample form for testing",
        },
        "inputs": [
            {
                "Type": "text",
                "Variable To Save As": "article.title",
                "Label": "Title",
                "Required": True,
            }
        ],
    }

    # Process the document
    result = processor.process_form_document(valid_document)

    if result.success:
        print(f"Successfully processed form: {result.form_definition.name}")
    else:
        print("Failed to process form:")
        for error in result.errors:
            print(f"- {error}")


if __name__ == "__main__":
    main()
