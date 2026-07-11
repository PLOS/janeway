"""
Django models for the document-driven form builder.

This module defines the models used to store form definitions and related data
as specified in the form schema.
"""

from django.db import models
from django.utils import timezone


class FormDefinition(models.Model):
    """
    Main model for storing form metadata.
    
    This model represents a form definition that can be used to generate
    HTML forms dynamically based on JSON schema.
    """
    
    name = models.CharField(max_length=255, help_text="The name of the form")
    description = models.TextField(blank=True, help_text="Description of the form")
    created_date = models.DateTimeField(default=timezone.now, help_text="When the form was created")
    modified_date = models.DateTimeField(auto_now=True, help_text="When the form was last modified")
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Form Definition"
        verbose_name_plural = "Form Definitions"


class FormVariable(models.Model):
    """
    Model for storing variables used in forms.
    
    Variables are used to store dynamic values that can be referenced
    in form inputs or logic sections.
    """
    
    form_definition = models.ForeignKey(FormDefinition, on_delete=models.CASCADE, related_name='variables')
    variable_id = models.CharField(max_length=255, help_text="The id used to reference this value")
    variable_type = models.CharField(
        max_length=255, 
        default="any", 
        help_text="The python literal type for the given object. Defaults to 'any'."
    )
    value = models.TextField(blank=True, null=True, help_text="The starting value for the variable")
    
    def __str__(self):
        return f"{self.variable_id} ({self.form_definition.name})"
    
    class Meta:
        verbose_name = "Form Variable"
        verbose_name_plural = "Form Variables"


class FormInput(models.Model):
    """
    Model for storing input fields.
    
    Each input represents an HTML form element with various properties
    that define its behavior, validation, and appearance.
    """
    
    INPUT_TYPES = [
        ('text', 'Text'),
        ('paragraph', 'Paragraph'),
        ('date', 'Date'),
        ('selection', 'Selection'),
        ('number', 'Number'),
    ]
    
    form_definition = models.ForeignKey(FormDefinition, on_delete=models.CASCADE, related_name='inputs')
    input_id = models.CharField(max_length=255, help_text="The id for the input (literally the `id=\"[value]\"` of an HTML tag)")
    name = models.CharField(max_length=255, help_text="The name for the input (literally the `name=\"[value]\"` of an HTML tag)")
    input_type = models.CharField(max_length=20, choices=INPUT_TYPES, help_text="The type of input which the user is expected to enter")
    
    # Optional fields
    enum_choices = models.JSONField(blank=True, null=True, help_text="A list of restricted input choices")
    label = models.CharField(max_length=255, blank=True, help_text="The label for the input")
    help_text = models.TextField(blank=True, help_text="The help text for the input")
    value = models.TextField(blank=True, null=True, help_text="Allows the user to set a value for the input")
    default_value = models.TextField(blank=True, null=True, help_text="The default value for the input if the user does not enter one")
    placeholder_value = models.CharField(max_length=255, blank=True, help_text="The placeholder value for the user")
    required = models.BooleanField(default=False, help_text="True if the input requires the user to enter some value")
    hidden = models.BooleanField(default=False, help_text="True if the input is hidden or not rendered on the page")
    variable_to_save_as = models.CharField(max_length=255, help_text="The name of the variable to save as")
    
    # Logic and validation fields stored as JSON
    logic = models.JSONField(blank=True, null=True, help_text="Conditional logic for the input")
    validation = models.JSONField(blank=True, null=True, help_text="Validation rules for the input")
    
    def __str__(self):
        return f"{self.name} ({self.input_type}) - {self.form_definition.name}"
    
    class Meta:
        verbose_name = "Form Input"
        verbose_name_plural = "Form Inputs"


class FormValidationRule(models.Model):
    """
    Model for storing validation rules.
    
    These rules define how form inputs should be validated when the form is submitted.
    """
    
    VALIDATION_TYPES = [
        ('min_length', 'Minimum Length'),
        ('max_length', 'Maximum Length'),
        ('min_value', 'Minimum Value'),
        ('max_value', 'Maximum Value'),
        ('pattern', 'Pattern'),
        ('required', 'Required'),
        ('email', 'Email'),
        ('url', 'URL'),
        ('custom', 'Custom'),
        ('min_date', 'Minimum Date'),
        ('max_date', 'Maximum Date'),
        ('format', 'Format'),
        ('enum', 'Enum'),
        ('file_types', 'File Types'),
        ('max_size', 'Maximum Size'),
        ('min_checked', 'Minimum Checked'),
        ('max_checked', 'Maximum Checked'),
        ('step', 'Step'),
    ]
    
    form_input = models.ForeignKey(FormInput, on_delete=models.CASCADE, related_name='validation_rules')
    rule_type = models.CharField(max_length=20, choices=VALIDATION_TYPES, help_text="The type of validation rule")
    value = models.TextField(blank=True, null=True, help_text="Parameters for the rule")
    error_message = models.TextField(blank=True, help_text="Custom error message for when the validation fails")
    condition = models.TextField(blank=True, help_text="Optional condition for when the validation should apply")
    
    def __str__(self):
        return f"{self.rule_type} validation for {self.form_input.name}"
    
    class Meta:
        verbose_name = "Form Validation Rule"
        verbose_name_plural = "Form Validation Rules"