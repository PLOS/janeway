# Form Document Schema Documentation

This document provides detailed information about the JSON schema used for form documents in the document-driven form builder.

## Overview

The form document schema defines the structure and validation rules for form documents. It ensures that form documents conform to a consistent format and contain all required information for the form builder to process them correctly.

## Schema Structure

The schema is organized into two main sections:

1. **Variables**: An array of variable objects that hold values used within the form logic
2. **Inputs**: An array of input objects that define the form fields

### Variables

Variables are objects that hold values used within the form logic. They have the following properties:

- **ID** (string, required): The identifier used to reference this variable
- **Type** (string, optional): The Python literal type for the variable (defaults to "any")
- **Value** (any type, required): The starting value for the variable

Example:
```json
{
  "ID": "thank_you_message",
  "Type": "str",
  "Value": "Thank you for submitting to PLOS!"
}
```

### Inputs

Inputs are objects that define the form fields. They have the following properties:

- **ID** (string, optional): The HTML id attribute for the input
- **Name** (string, optional): The HTML name attribute for the input
- **Type** (string, required): The type of input (must be one of: "text", "paragraph", "date", "selection", "number")
- **Enum** (array, optional): A list of restricted input choices
- **Label** (string, optional): The label for the input
- **Help Text** (string, optional): Help text for the input
- **Value** (any type, optional): A value for the input (useful for hidden variables)
- **Default Value** (any type, optional): The default value for the input
- **Placeholder Value** (string, optional): The placeholder value for the input
- **Required** (boolean, optional): Whether the input is required (defaults to false)
- **Hidden** (boolean, optional): Whether the input is hidden (defaults to false)
- **Variable To Save As** (string, required): The variable name to save the input value as
- **Logic** (object, optional): Conditional logic for the input
- **Validation** (array, optional): Validation rules for the input

Example:
```json
{
  "ID": "title",
  "Name": "title",
  "Type": "text",
  "Label": "Title",
  "Help Text": "Enter the title of your article",
  "Required": true,
  "Variable To Save As": "article.title",
  "Validation": [
    {
      "Rule": {
        "Type": "min_length",
        "Value": 5,
        "Error": "Title must be at least 5 characters long"
      }
    }
  ]
}
```

## Validation Rules

The schema supports validation rules for inputs. Each validation rule has the following structure:

- **Rule** (object, required): The validation rule definition
  - **Type** (string, required): The type of validation rule
  - **Value** (any type, optional): Parameters for the rule
  - **Error** (string, optional): Custom error message
- **Condition** (string, optional): Optional condition for when the validation should apply

Supported validation rule types:
- min_length
- max_length
- min_value
- max_value
- pattern
- required
- email
- url
- custom
- min_date
- max_date
- format
- enum
- file_types
- max_size
- min_checked
- max_checked
- step

## Usage

To validate a form document against the schema:

1. Ensure the `jsonschema` library is installed:
   ```
   pip install jsonschema
   ```

2. Use the FormValidator class:
   ```python
   from form_builder.validation.form_validator import FormValidator

   validator = FormValidator()
   is_valid, errors = validator.validate_form_document(your_form_document)
   ```

## Example Form Document

Here's a complete example of a valid form document:

```json
{
  "variables": [
    {
      "ID": "thank_you_message",
      "Type": "str",
      "Value": "Thank you for submitting to PLOS!"
    }
  ],
  "inputs": [
    {
      "ID": "title",
      "Name": "title",
      "Type": "text",
      "Label": "Title",
      "Help Text": "Enter the title of your article",
      "Required": true,
      "Variable To Save As": "article.title",
      "Validation": [
        {
          "Rule": {
            "Type": "min_length",
            "Value": 5,
            "Error": "Title must be at least 5 characters long"
          }
        }
      ]
    }
  ]
}
```