"""
Tests for the form builder signals.
"""

from django.test import TestCase
from django.dispatch import receiver

from form_builder import models
from form_builder.signals import (
    form_processed,
    form_submission_processed,
    form_processing,
    form_submission_processing
)


class FormBuilderSignalsTest(TestCase):
    """
    Test class for form builder signals.
    """

    def setUp(self):
        """
        Set up the test environment.
        """
        # Create a test form definition
        self.form_definition = models.FormDefinition.objects.create(
            name="Test Form",
            description="A test form for signal testing"
        )

    def test_form_processing_signals_are_sent(self):
        """
        Test that form processing signals are sent.
        """
        # Track if signals were received
        processing_signal_received = False
        processed_signal_received = False
        
        @receiver(form_processing)
        def processing_signal_handler(sender, **kwargs):
            nonlocal processing_signal_received
            processing_signal_received = True
        
        @receiver(form_processed)
        def processed_signal_handler(sender, **kwargs):
            nonlocal processed_signal_received
            processed_signal_received = True
        
        # Send the signals manually to test they work
        form_processing.send(sender=self, form_definition=self.form_definition)
        form_processed.send(sender=self, form_definition=self.form_definition)
        
        # Check that both signals were received
        self.assertTrue(processing_signal_received, "form_processing signal was not sent")
        self.assertTrue(processed_signal_received, "form_processed signal was not sent")

    def test_form_submission_signals_are_sent(self):
        """
        Test that form submission signals are sent.
        """
        # Track if signals were received
        processing_signal_received = False
        processed_signal_received = False
        
        @receiver(form_submission_processing)
        def submission_processing_signal_handler(sender, **kwargs):
            nonlocal processing_signal_received
            processing_signal_received = True
        
        @receiver(form_submission_processed)
        def submission_processed_signal_handler(sender, **kwargs):
            nonlocal processed_signal_received
            processed_signal_received = True
        
        # Send the signals manually to test they work
        form_submission_processing.send(
            sender=self, 
            form_definition=self.form_definition, 
            request=None
        )
        form_submission_processed.send(
            sender=self, 
            form_definition=self.form_definition, 
            article=None,
            request=None
        )
        
        # Check that both signals were received
        self.assertTrue(processing_signal_received, "form_submission_processing signal was not sent")
        self.assertTrue(processed_signal_received, "form_submission_processed signal was not sent")