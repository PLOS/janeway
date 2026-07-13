from django.apps import AppConfig


class FormBuilderConfig(AppConfig):
    """Configures the form builder app."""

    name = "form_builder"

    def ready(self):
        # Import signals to register them
        from . import signals  # noqa: F401