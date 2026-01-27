from django.apps import AppConfig
from django.conf import settings
import os

class CustomSubmissionConfig(AppConfig):
    name = 'plugins.customsubmission'

    def ready(self):
        override_dir = os.path.join(
            os.path.dirname(__file__),
            'templates', 'overrides'
        )
        settings.TEMPLATES[0]['DIRS'].insert(0, override_dir)
