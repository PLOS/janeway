"""
Test suite for form document validation using Pytest.

This module tests the FormValidator class with sample form documents
to ensure it correctly identifies valid and invalid documents.
"""

import os
import sys
import json
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from validation.form_validator import FormValidator


class TestFormValidation:
    """Test cases for form document validation."""

    @pytest.fixture
    def validator(self):
        """Fixture to provide a FormValidator instance."""
        return FormValidator()

    @pytest.fixture
    def valid_form_path(self):
        """Fixture to provide path to sample valid form document."""
        return os.path.join(os.path.dirname(__file__), 'sample_valid_form.json')

    @pytest.fixture
    def invalid_form_path(self):
        """Fixture to provide path to sample invalid form document."""
        return os.path.join(os.path.dirname(__file__), 'sample_invalid_form.json')

    def test_valid_form(self, validator, valid_form_path):
        """Test validation of a valid form document."""
        is_valid, errors = validator.validate_form_document_file(valid_form_path)
        
        assert is_valid is True
        assert len(errors) == 0

    def test_invalid_form(self, validator, invalid_form_path):
        """Test validation of an invalid form document."""
        is_valid, errors = validator.validate_form_document_file(invalid_form_path)
        
        assert is_valid is False
        assert len(errors) > 0

    def test_nonexistent_file(self, validator):
        """Test validation with a nonexistent file."""
        is_valid, errors = validator.validate_form_document_file("nonexistent.json")
        
        assert is_valid is False
        assert len(errors) > 0
        assert "not found" in errors[0]

    def test_invalid_json(self, validator):
        """Test validation with an invalid JSON file."""
        # Create a temporary file with invalid JSON
        invalid_json_path = os.path.join(os.path.dirname(__file__), 'invalid_json.json')
        
        try:
            with open(invalid_json_path, 'w') as f:
                f.write('{ invalid json }')
            
            is_valid, errors = validator.validate_form_document_file(invalid_json_path)
            
            assert is_valid is False
            assert len(errors) > 0
            assert "Invalid JSON" in errors[0]
        finally:
            # Clean up the temporary file
            if os.path.exists(invalid_json_path):
                os.remove(invalid_json_path)