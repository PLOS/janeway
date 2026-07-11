"""
Form Validator Module

This module provides functionality to validate form documents against a JSON schema.
It uses the jsonschema library to perform validation and returns detailed error messages
when validation fails.
"""

import json
import os
from typing import Dict, Any, List, Tuple
import jsonschema
from jsonschema import ValidationError


class FormValidator:
    """
    A class to validate form documents against a JSON schema.
    
    Attributes:
        schema_path (str): Path to the JSON schema file.
        schema (Dict[str, Any]): The loaded JSON schema.
    """
    
    def __init__(self, schema_path: str = None):
        """
        Initialize the FormValidator with a schema file.
        
        Args:
            schema_path (str, optional): Path to the JSON schema file. 
                                         Defaults to the standard schema location.
        """
        if schema_path is None:
            # Default path to the schema file
            self.schema_path = os.path.join(
                os.path.dirname(__file__), 
                '..', 
                'schema', 
                'form_schema.json'
            )
        else:
            self.schema_path = schema_path
            
        self.schema = self._load_schema()
    
    def _load_schema(self) -> Dict[str, Any]:
        """
        Load the JSON schema from the schema file.
        
        Returns:
            Dict[str, Any]: The loaded JSON schema.
            
        Raises:
            FileNotFoundError: If the schema file is not found.
            json.JSONDecodeError: If the schema file contains invalid JSON.
        """
        try:
            with open(self.schema_path, 'r') as schema_file:
                return json.load(schema_file)
        except FileNotFoundError:
            raise FileNotFoundError(f"Schema file not found at {self.schema_path}")
        except json.JSONDecodeError as e:
            raise json.JSONDecodeError(f"Invalid JSON in schema file: {e.msg}", e.doc, e.pos)
    
    def validate_form_document(self, document: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """
        Validate a form document against the JSON schema.
        
        Args:
            document (Dict[str, Any]): The form document to validate.
            
        Returns:
            Tuple[bool, List[str]]: A tuple containing:
                - bool: True if the document is valid, False otherwise.
                - List[str]: A list of error messages if validation fails, empty list otherwise.
        """
        errors = []
        
        try:
            jsonschema.validate(instance=document, schema=self.schema)
            return True, []
        except jsonschema.ValidationError as e:
            errors.append(f"Validation error: {e.message}")
            return False, errors
        except jsonschema.SchemaError as e:
            errors.append(f"Schema error: {e.message}")
            return False, errors
        except Exception as e:
            errors.append(f"Unexpected error during validation: {str(e)}")
            return False, errors
    
    def validate_form_document_file(self, file_path: str) -> Tuple[bool, List[str]]:
        """
        Validate a form document file against the JSON schema.
        
        Args:
            file_path (str): Path to the form document file (JSON format).
            
        Returns:
            Tuple[bool, List[str]]: A tuple containing:
                - bool: True if the document is valid, False otherwise.
                - List[str]: A list of error messages if validation fails, empty list otherwise.
        """
        try:
            with open(file_path, 'r') as file:
                document = json.load(file)
            return self.validate_form_document(document)
        except FileNotFoundError:
            return False, [f"Form document file not found at {file_path}"]
        except json.JSONDecodeError as e:
            return False, [f"Invalid JSON in form document file: {e.msg}"]
        except Exception as e:
            return False, [f"Unexpected error while reading form document file: {str(e)}"]


def main():
    """
    Main function to demonstrate the usage of FormValidator.
    """
    # Example usage
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
    
    # Example invalid form document (missing required "Type" field)
    invalid_document = {
        "inputs": [
            {
                "Variable To Save As": "article.title",
                "Label": "Title",
                "Required": True
            }
        ]
    }
    
    # Validate documents
    is_valid, errors = validator.validate_form_document(valid_document)
    print(f"Valid document validation result: {is_valid}")
    if errors:
        print("Errors:", errors)
    
    is_valid, errors = validator.validate_form_document(invalid_document)
    print(f"Invalid document validation result: {is_valid}")
    if errors:
        print("Errors:", errors)


if __name__ == "__main__":
    main()