"""
Tests for the Form Processor Module

This module contains tests for the form processor functionality,
including parsing, validation, conversion, and persistence.
"""

import json
import os
import tempfile
from django.test import TestCase
from form_builder.models import (
    FormDefinition,
    FormVariable,
    FormInput,
    FormValidationRule,
)
from form_builder.processors.form_processor import (
    FormProcessor,
    FormProcessorResult,
    FormValidationError,
    FormProcessingError,
    FormPersistenceError,
)


class FormProcessorTest(TestCase):
    """Test cases for the FormProcessor class."""

    def setUp(self):
        """Set up test data."""
        self.processor = FormProcessor()

        # Sample valid form document
        self.valid_document = {
            "metadata": {
                "name": "Test Form",
                "description": "A test form for unit tests",
            },
            "variables": [{"id": "var1", "type": "string", "value": "test value"}],
            "inputs": [
                {
                    "id": "input1",
                    "name": "title",
                    "type": "text",
                    "label": "Title",
                    "required": True,
                    "variableToSaveAs": "article.title",
                    "validation": [
                        {
                            "rule": {
                                "type": "min_length",
                                "value": 5,
                                "error": "Title must be at least 5 characters long",
                            }
                        }
                    ],
                }
            ],
        }

        # Sample invalid form document (missing required Type field)
        self.invalid_document = {
            "metadata": {
                "name": "Invalid Test Form",
                "description": "An invalid test form for unit tests",
            },
            "inputs": [
                {
                    "id": "input1",
                    "name": "title",
                    "label": "Title",
                    "required": True,
                    "variableToSaveAs": "article.title",
                }
            ],
        }

    def test_process_form_document_success(self):
        """Test successful processing of a valid form document."""
        result = self.processor.process_form_document(self.valid_document)

        # Check that the result is successful
        self.assertTrue(result.success)
        self.assertEqual(len(result.errors), 0)
        self.assertIsNotNone(result.form_definition)

        # Check that the form definition was created correctly
        form_def = result.form_definition
        self.assertEqual(form_def.name, "Test Form")
        self.assertEqual(form_def.description, "A test form for unit tests")

        # Check that variables were created
        variables = form_def.variables.all()
        self.assertEqual(len(variables), 1)
        self.assertEqual(variables[0].variable_id, "var1")
        self.assertEqual(variables[0].variable_type, "string")
        self.assertEqual(variables[0].value, "test value")

        # Check that inputs were created
        inputs = form_def.inputs.all()
        self.assertEqual(len(inputs), 1)
        self.assertEqual(inputs[0].input_id, "input1")
        self.assertEqual(inputs[0].name, "title")
        self.assertEqual(inputs[0].input_type, "text")
        self.assertEqual(inputs[0].label, "Title")
        self.assertTrue(inputs[0].required)
        self.assertEqual(inputs[0].variable_to_save_as, "article.title")

        # Check that validation rules were created
        validation_rules = inputs[0].validation_rules.all()
        self.assertEqual(len(validation_rules), 1)
        self.assertEqual(validation_rules[0].rule_type, "min_length")
        self.assertEqual(validation_rules[0].value, "5")
        self.assertEqual(
            validation_rules[0].error_message,
            "Title must be at least 5 characters long",
        )

    def test_process_form_document_validation_error(self):
        """Test processing of an invalid form document."""
        result = self.processor.process_form_document(self.invalid_document)

        # Check that the result is not successful
        self.assertFalse(result.success)
        self.assertIsNone(result.form_definition)
        self.assertGreater(len(result.errors), 0)

        # Check that the error is a FormValidationError
        self.assertTrue(any("FormValidationError" in error for error in result.errors))

    def test_process_form_document_file_success(self):
        """Test successful processing of a form document from a file."""
        # Create a temporary file with the valid document
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump(self.valid_document, f)
            temp_file_path = f.name

        try:
            result = self.processor.process_form_document_file(temp_file_path)

            # Check that the result is successful
            self.assertTrue(result.success)
            self.assertEqual(len(result.errors), 0)
            self.assertIsNotNone(result.form_definition)

            # Check that the form definition was created correctly
            form_def = result.form_definition
            self.assertEqual(form_def.name, "Test Form")
        finally:
            # Clean up the temporary file
            os.unlink(temp_file_path)

    def test_process_form_document_file_not_found(self):
        """Test processing of a non-existent form document file."""
        result = self.processor.process_form_document_file("/non/existent/file.json")

        # Check that the result is not successful
        self.assertFalse(result.success)
        self.assertIsNone(result.form_definition)
        self.assertEqual(len(result.errors), 1)
        self.assertIn("file not found", result.errors[0].lower())

    def test_process_form_document_file_invalid_json(self):
        """Test processing of a form document file with invalid JSON."""
        # Create a temporary file with invalid JSON
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            f.write("{ invalid json }")
            temp_file_path = f.name

        try:
            result = self.processor.process_form_document_file(temp_file_path)

            # Check that the result is not successful
            self.assertFalse(result.success)
            self.assertIsNone(result.form_definition)
            self.assertEqual(len(result.errors), 1)
            self.assertIn("invalid json", result.errors[0].lower())
        finally:
            # Clean up the temporary file
            os.unlink(temp_file_path)

    def test_form_processor_result_initialization(self):
        """Test initialization of FormProcessorResult."""
        # Test with success
        result = FormProcessorResult(success=True)
        self.assertTrue(result.success)
        self.assertIsNone(result.form_definition)
        self.assertEqual(result.errors, [])

        # Test with all parameters
        form_def = FormDefinition(name="Test Form")
        errors = ["Error 1", "Error 2"]
        result = FormProcessorResult(
            success=False, form_definition=form_def, errors=errors
        )
        self.assertFalse(result.success)
        self.assertEqual(result.form_definition.name, "Test Form")
        self.assertEqual(result.errors, errors)

    def test_update_existing_form(self):
        """Test updating an existing form."""
        # First, create a form
        result = self.processor.process_form_document(self.valid_document)
        self.assertTrue(result.success)

        # Now update the form with new data
        updated_document = self.valid_document.copy()
        updated_document["metadata"]["name"] = "Updated Test Form"
        updated_document["inputs"][0]["label"] = "Updated Title"

        result = self.processor.process_form_document(updated_document)

        # Check that the result is successful
        self.assertTrue(result.success)
        self.assertEqual(len(result.errors), 0)
        self.assertIsNotNone(result.form_definition)

        # Check that the form was updated
        form_def = result.form_definition
        self.assertEqual(form_def.name, "Updated Test Form")

        # Check that the input was updated
        inputs = form_def.inputs.all()
        self.assertEqual(len(inputs), 1)
        self.assertEqual(inputs[0].label, "Updated Title")
