"""
Tests for the form builder data mapping functionality.
"""

from django.test import TestCase

from form_builder import models


class FormBuilderDataMappingTest(TestCase):
    """
    Test class for form builder data mapping functionality.
    """

    def setUp(self):
        """
        Set up the test environment.
        """
        # Create a test form definition
        self.form_definition = models.FormDefinition.objects.create(
            name="Test Form",
            description="A test form for data mapping testing"
        )
        
        # Create test form inputs
        self.title_input = models.FormInput.objects.create(
            form_definition=self.form_definition,
            name="title",
            label="Title",
            input_type="text",
            variable_to_save_as="article.title"
        )
        
        self.abstract_input = models.FormInput.objects.create(
            form_definition=self.form_definition,
            name="abstract",
            label="Abstract",
            input_type="paragraph",
            variable_to_save_as="article.abstract"
        )

    def test_nested_attribute_setter(self):
        """
        Test the nested attribute setter function.
        """
        # Create a simple test object
        class TestObject:
            def __init__(self):
                self.article = TestArticle()
        
        class TestArticle:
            def __init__(self):
                self.title = ""
                self.abstract = ""
        
        # Create test object
        obj = TestObject()
        
        # Define the nested attribute setter function
        def set_nested_attribute(obj, attr_path, value):
            """
            Set a nested attribute on an object using dot notation.
            Example: set_nested_attribute(article, 'section.name', 'Test Section')
            """
            attrs = attr_path.split('.')
            for attr in attrs[:-1]:
                obj = getattr(obj, attr)
            setattr(obj, attrs[-1], value)
        
        # Set the title and abstract
        set_nested_attribute(obj, "article.title", "Test Article Title")
        set_nested_attribute(obj, "article.abstract", "This is a test abstract.")
        
        # Check that the attributes were set correctly
        self.assertEqual(obj.article.title, "Test Article Title")
        self.assertEqual(obj.article.abstract, "This is a test abstract.")