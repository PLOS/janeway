"""
Tests for the form builder views.
"""

from django.test import TestCase, override_settings
from django.urls import reverse
from core.models import Account
from utils.testing import helpers


class TestFormBuilderViews(TestCase):
    """Test cases for form builder views."""

    @classmethod
    def setUpTestData(cls):
        """Set up test data."""
        # Create press and journals
        cls.press = helpers.create_press()
        cls.journal_one, cls.journal_two = helpers.create_journals()
        
        # Create a staff user
        cls.user = helpers.create_user(
            "testuser@example.com",
            roles=["admin"],
            journal=cls.journal_one,
        )
        cls.user.is_staff = True
        cls.user.is_active = True
        cls.user.save()

    def setUp(self):
        """Set up test environment."""
        self.client = self.client_class()

    @override_settings(URL_CONFIG="domain")
    def test_list_forms_view(self):
        """Test that the list forms view loads correctly."""
        self.client.force_login(self.user)
        url = reverse('form_builder_list_forms')
        response = self.client.get(url, SERVER_NAME=self.journal_one.domain)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Form Definitions')

    @override_settings(URL_CONFIG="domain")
    def test_upload_form_view_get(self):
        """Test that the upload form view loads correctly for GET requests."""
        self.client.force_login(self.user)
        url = reverse('form_builder_upload_form')
        response = self.client.get(url, SERVER_NAME=self.journal_one.domain)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Upload Form')

    @override_settings(URL_CONFIG="domain")
    def test_render_form_view_get(self):
        """Test that the render form view loads correctly for GET requests."""
        self.client.force_login(self.user)
        # First create a form definition
        from form_builder.models import FormDefinition
        form_def = FormDefinition.objects.create(
            name='Test Form',
            description='A test form'
        )
        
        url = reverse('form_builder_render_form', kwargs={'form_id': form_def.id})
        response = self.client.get(url, SERVER_NAME=self.journal_one.domain)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Form')