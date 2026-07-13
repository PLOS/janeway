"""
Signals for the form builder app.

This module defines signals that are sent during form processing events.
"""

from django.dispatch import Signal

# Signal sent when a form is successfully processed
form_processed = Signal()

# Signal sent when a form submission is successfully processed
form_submission_processed = Signal()

# Signal sent when a form is about to be processed
form_processing = Signal()

# Signal sent when a form submission is about to be processed
form_submission_processing = Signal()