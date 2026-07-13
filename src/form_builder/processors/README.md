# Form Processor

The Form Processor module handles parsing, validation, and conversion of uploaded JSON form documents to Django models.

## Overview

The Form Processor provides functionality to:
1. Parse uploaded JSON form documents
2. Validate documents against the form schema
3. Convert validated JSON data to Django models
4. Persist the data to the database
5. Handle updates to existing forms

## Usage

### Processing a Form Document

```python
from form_builder.processors.form_processor import FormProcessor

# Initialize the processor
processor = FormProcessor()

# Process a form document
document = {
    "name": "Sample Form",
    "description": "A sample form for testing",
    "inputs": [
        {
            "Type": "text",
            "Variable To Save As": "article.title",
            "Label": "Title",
            "Required": True
        }
    ]
}

result = processor.process_form_document(document)

if result.success:
    print(f"Successfully processed form: {result.form_definition.name}")
else:
    print("Failed to process form:")
    for error in result.errors:
        print(f"- {error}")
```

### Processing a Form Document from a File

```python
from form_builder.processors.form_processor import FormProcessor

# Initialize the processor
processor = FormProcessor()

# Process a form document from a file
result = processor.process_form_document_file("/path/to/form.json")

if result.success:
    print(f"Successfully processed form: {result.form_definition.name}")
else:
    print("Failed to process form:")
    for error in result.errors:
        print(f"- {error}")
```

## API

### FormProcessor

#### `__init__(self, schema_path: str = None)`

Initialize the FormProcessor with an optional schema path.

#### `process_form_document(self, document: Dict[str, Any]) -> FormProcessorResult`

Process a form document by parsing, validating, and converting to Django models.

#### `process_form_document_file(self, file_path: str) -> FormProcessorResult`

Process a form document file by parsing, validating, and converting to Django models.

### FormProcessorResult

#### `__init__(self, success: bool, form_definition: Optional[FormDefinition] = None, errors: List[str] = None)`

Initialize the result object with success status, form definition, and errors.

## Error Handling

The Form Processor defines custom exceptions for different error types:

- `FormValidationError`: Raised for schema validation errors
- `FormProcessingError`: Raised for general processing errors
- `FormPersistenceError`: Raised for database operation errors

All exceptions are caught and converted to a `FormProcessorResult` with appropriate error messages.