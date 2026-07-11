"""
Tests for the form builder models.

This module tests the Django models for saving and deleting form definitions,
variables, inputs, and validation rules using pytest-django.
"""

import pytest
from django.utils import timezone

from form_builder.models import FormDefinition, FormVariable, FormInput, FormValidationRule


class TestFormModels:
    """Test cases for form models."""

    @pytest.mark.django_db
    def test_create_and_save_form_definition(self):
        """Test creating and saving a FormDefinition instance."""
        form_def = FormDefinition.objects.create(
            name="Test Form",
            description="A test form for pytest"
        )
        
        # Verify the form was saved correctly
        assert form_def.id is not None
        assert form_def.name == "Test Form"
        assert form_def.description == "A test form for pytest"
        assert form_def.created_date is not None
        assert form_def.modified_date is not None
        
        # Verify string representation
        assert str(form_def) == "Test Form"
        
        # Verify meta information
        assert form_def._meta.verbose_name == "Form Definition"
        assert form_def._meta.verbose_name_plural == "Form Definitions"

    @pytest.mark.django_db
    def test_create_and_save_form_variable(self):
        """Test creating and saving a FormVariable instance."""
        # First create a form definition
        form_def = FormDefinition.objects.create(
            name="Test Form",
            description="A test form for pytest"
        )
        
        # Create a form variable
        form_var = FormVariable.objects.create(
            form_definition=form_def,
            variable_id="test_var",
            variable_type="str",
            value="test value"
        )
        
        # Verify the variable was saved correctly
        assert form_var.id is not None
        assert form_var.variable_id == "test_var"
        assert form_var.variable_type == "str"
        assert form_var.value == "test value"
        assert form_var.form_definition == form_def
        
        # Verify string representation
        assert str(form_var) == "test_var (Test Form)"
        
        # Verify meta information
        assert form_var._meta.verbose_name == "Form Variable"
        assert form_var._meta.verbose_name_plural == "Form Variables"
        
        # Verify relationship
        assert form_var in form_def.variables.all()

    @pytest.mark.django_db
    def test_create_and_save_form_input(self):
        """Test creating and saving a FormInput instance."""
        # First create a form definition
        form_def = FormDefinition.objects.create(
            name="Test Form",
            description="A test form for pytest"
        )
        
        # Create a form input
        form_input = FormInput.objects.create(
            form_definition=form_def,
            input_id="test_input",
            name="Test Input",
            input_type="text",
            label="Test Label",
            help_text="Test help text",
            required=True,
            hidden=False,
            variable_to_save_as="test_variable",
            logic={"condition": "always"},
            validation={"rules": ["required"]}
        )
        
        # Verify the input was saved correctly
        assert form_input.id is not None
        assert form_input.input_id == "test_input"
        assert form_input.name == "Test Input"
        assert form_input.input_type == "text"
        assert form_input.label == "Test Label"
        assert form_input.help_text == "Test help text"
        assert form_input.required is True
        assert form_input.hidden is False
        assert form_input.variable_to_save_as == "test_variable"
        assert form_input.logic == {"condition": "always"}
        assert form_input.validation == {"rules": ["required"]}
        assert form_input.form_definition == form_def
        
        # Verify string representation
        assert str(form_input) == "Test Input (text) - Test Form"
        
        # Verify meta information
        assert form_input._meta.verbose_name == "Form Input"
        assert form_input._meta.verbose_name_plural == "Form Inputs"
        
        # Verify relationship
        assert form_input in form_def.inputs.all()

    @pytest.mark.django_db
    def test_create_and_save_form_validation_rule(self):
        """Test creating and saving a FormValidationRule instance."""
        # First create a form definition
        form_def = FormDefinition.objects.create(
            name="Test Form",
            description="A test form for pytest"
        )
        
        # Create a form input
        form_input = FormInput.objects.create(
            form_definition=form_def,
            input_id="test_input",
            name="Test Input",
            input_type="text",
            variable_to_save_as="test_variable"
        )
        
        # Create a validation rule
        validation_rule = FormValidationRule.objects.create(
            form_input=form_input,
            rule_type="min_length",
            value="5",
            error_message="Minimum length is 5 characters",
            condition="always"
        )
        
        # Verify the validation rule was saved correctly
        assert validation_rule.id is not None
        assert validation_rule.rule_type == "min_length"
        assert validation_rule.value == "5"
        assert validation_rule.error_message == "Minimum length is 5 characters"
        assert validation_rule.condition == "always"
        assert validation_rule.form_input == form_input
        
        # Verify string representation
        assert str(validation_rule) == "min_length validation for Test Input"
        
        # Verify meta information
        assert validation_rule._meta.verbose_name == "Form Validation Rule"
        assert validation_rule._meta.verbose_name_plural == "Form Validation Rules"
        
        # Verify relationship
        assert validation_rule in form_input.validation_rules.all()

    @pytest.mark.django_db
    def test_delete_form_definition_cascade(self):
        """Test that deleting a FormDefinition cascades to related objects."""
        # Create a form definition
        form_def = FormDefinition.objects.create(
            name="Test Form",
            description="A test form for pytest"
        )
        
        # Create related objects
        form_var = FormVariable.objects.create(
            form_definition=form_def,
            variable_id="test_var",
            variable_type="str"
        )
        
        form_input = FormInput.objects.create(
            form_definition=form_def,
            input_id="test_input",
            name="Test Input",
            input_type="text",
            variable_to_save_as="test_variable"
        )
        
        validation_rule = FormValidationRule.objects.create(
            form_input=form_input,
            rule_type="min_length",
            value="5"
        )
        
        # Verify all objects exist
        assert FormDefinition.objects.filter(id=form_def.id).exists()
        assert FormVariable.objects.filter(id=form_var.id).exists()
        assert FormInput.objects.filter(id=form_input.id).exists()
        assert FormValidationRule.objects.filter(id=validation_rule.id).exists()
        
        # Delete the form definition
        form_def_id = form_def.id
        form_def.delete()
        
        # Verify cascade deletion
        assert not FormDefinition.objects.filter(id=form_def_id).exists()
        assert not FormVariable.objects.filter(id=form_var.id).exists()
        assert not FormInput.objects.filter(id=form_input.id).exists()
        assert not FormValidationRule.objects.filter(id=validation_rule.id).exists()

    @pytest.mark.django_db
    def test_delete_form_variable(self):
        """Test deleting a FormVariable instance."""
        # Create a form definition
        form_def = FormDefinition.objects.create(
            name="Test Form",
            description="A test form for pytest"
        )
        
        # Create a form variable
        form_var = FormVariable.objects.create(
            form_definition=form_def,
            variable_id="test_var",
            variable_type="str"
        )
        
        # Verify the variable exists
        assert FormVariable.objects.filter(id=form_var.id).exists()
        
        # Delete the variable
        form_var_id = form_var.id
        form_var.delete()
        
        # Verify the variable is deleted
        assert not FormVariable.objects.filter(id=form_var_id).exists()
        
        # Verify the form definition still exists
        assert FormDefinition.objects.filter(id=form_def.id).exists()

    @pytest.mark.django_db
    def test_delete_form_input_cascade(self):
        """Test that deleting a FormInput cascades to validation rules."""
        # Create a form definition
        form_def = FormDefinition.objects.create(
            name="Test Form",
            description="A test form for pytest"
        )
        
        # Create a form input
        form_input = FormInput.objects.create(
            form_definition=form_def,
            input_id="test_input",
            name="Test Input",
            input_type="text",
            variable_to_save_as="test_variable"
        )
        
        # Create a validation rule
        validation_rule = FormValidationRule.objects.create(
            form_input=form_input,
            rule_type="min_length",
            value="5"
        )
        
        # Verify all objects exist
        assert FormInput.objects.filter(id=form_input.id).exists()
        assert FormValidationRule.objects.filter(id=validation_rule.id).exists()
        
        # Delete the form input
        form_input_id = form_input.id
        form_input.delete()
        
        # Verify cascade deletion
        assert not FormInput.objects.filter(id=form_input_id).exists()
        assert not FormValidationRule.objects.filter(id=validation_rule.id).exists()
        
        # Verify the form definition still exists
        assert FormDefinition.objects.filter(id=form_def.id).exists()

    @pytest.mark.django_db
    def test_delete_form_validation_rule(self):
        """Test deleting a FormValidationRule instance."""
        # Create a form definition
        form_def = FormDefinition.objects.create(
            name="Test Form",
            description="A test form for pytest"
        )
        
        # Create a form input
        form_input = FormInput.objects.create(
            form_definition=form_def,
            input_id="test_input",
            name="Test Input",
            input_type="text",
            variable_to_save_as="test_variable"
        )
        
        # Create a validation rule
        validation_rule = FormValidationRule.objects.create(
            form_input=form_input,
            rule_type="min_length",
            value="5"
        )
        
        # Verify the validation rule exists
        assert FormValidationRule.objects.filter(id=validation_rule.id).exists()
        
        # Delete the validation rule
        validation_rule_id = validation_rule.id
        validation_rule.delete()
        
        # Verify the validation rule is deleted
        assert not FormValidationRule.objects.filter(id=validation_rule_id).exists()
        
        # Verify the form input and definition still exist
        assert FormInput.objects.filter(id=form_input.id).exists()
        assert FormDefinition.objects.filter(id=form_def.id).exists()
