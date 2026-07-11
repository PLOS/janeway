# Form Document Validation Documentation

This document provides detailed information about the form document validation implementation in the document-driven form builder.

## Overview

The form document validation system ensures that form documents conform to the expected JSON schema. It uses the `jsonschema` library to perform validation and provides detailed error messages when validation fails.

## FormValidator Class

The `FormValidator` class is the main component of the validation system. It provides methods for validating form documents against the JSON schema.

### Constructor

```python
FormValidator(schema_path: str = None)
```

Initializes the FormValidator with a schema file.

- `schema_path` (str, optional): Path to the JSON schema file. Defaults to the standard schema location.

### Methods

#### validate_form_document

```python
validate_form_document(document: Dict[str, Any]) -> Tuple[bool, List[str]]
```

Validates a form document against the JSON schema.

- `document` (Dict[str, Any]): The form document to validate.
- Returns: A tuple containing:
  - bool: True if the document is valid, False otherwise.
  - List[str]: A list of error messages if validation fails, empty list otherwise.

#### validate_form_document_file

```python
validate_form_document_file(file_path: str) -> Tuple[bool, List[str]]
```

Validates a form document file against the JSON schema.

- `file_path` (str): Path to the form document file (JSON format).
- Returns: A tuple containing:
  - bool: True if the document is valid, False otherwise.
  - List[str]: A list of error messages if validation fails, empty list otherwise.

## Usage Examples

### Validating an In-Memory Document

```python
from form_builder.validation.form_validator import FormValidator

validator = FormValidator()

# Example valid form document
valid_document = {
    "inputs": [
        {
            "Type": "text",
            "Variable To Save As": "article.title",
            "Label": "Title",
            "Required": True
        }
    ]
}

is_valid, errors = validator.validate_form_document(valid_document)
if is_valid:
    print("Document is valid")
else:
    print("Document is invalid:")
    for error in errors:
        print(f"  - {error}")
```

### Validating a Document File

```python
from form_builder.validation.form_validator import FormValidator

validator = FormValidator()

is_valid, errors = validator.validate_form_document_file("path/to/form_document.json")
if is_valid:
    print("Document is valid")
else:
    print("Document is invalid:")
    for error in errors:
        print(f"  - {error}")
```

## Error Handling

The FormValidator provides comprehensive error handling for various scenarios:

1. **Validation Errors**: When a document doesn't conform to the schema, detailed error messages are returned.
2. **Schema Errors**: When there are issues with the schema itself, appropriate error messages are returned.
3. **File Not Found**: When a specified document file doesn't exist, an error message is returned.
4. **Invalid JSON**: When a document file contains invalid JSON, an error message is returned.
5. **Unexpected Errors**: Any other unexpected errors are caught and returned as error messages.

## Dependencies

The validation implementation requires the following dependencies:

- `jsonschema`: For JSON schema validation

Install the dependency with:
```
pip install jsonschema
```

## Testing

The validation implementation includes comprehensive tests to ensure correct behavior. The tests cover:

1. Valid form documents
2. Invalid form documents
3. Nonexistent files
4. Invalid JSON files

Run the tests with:
```
python src/core/form_builder/tests/test_form_validation.py
```

## Integration with Django

To integrate the validation system with Django, you can use it in your views or forms:

```python
from django.http import JsonResponse
from form_builder.validation.form_validator import FormValidator

def validate_form_document_view(request):
    if request.method == 'POST':
        # Get the uploaded JSON document
        document = json.loads(request.body)
        
        # Validate the document
        validator = FormValidator()
        is_valid, errors = validator.validate_form_document(document)
        
        # Return the validation result
        return JsonResponse({
            'valid': is_valid,
            'errors': errors
        })
```

## Extending Validation

To extend the validation system, you can:

1. Modify the JSON schema file to add new validation rules
2. Extend the FormValidator class with additional validation methods
3. Create custom validation functions that work with the existing system

When modifying the schema, ensure that any changes maintain backward compatibility or provide a clear migration path for existing form documents.