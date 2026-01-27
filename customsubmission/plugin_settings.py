from django.conf import settings
from utils import plugins

PLUGIN_NAME = 'Custom Submission Wizard'
DISPLAY_NAME = 'Custom Submission'
DESCRIPTION = 'Multi-step submission form using django-formtools'
AUTHOR = 'Your Name'
VERSION = '1.0.0'
SHORT_NAME = 'customsubmission'
MANAGER_URL = 'customsubmission_manager'

# Plugin lifecycle hooks
def install():
    """Called when plugin is installed"""
    plugins.install_plugin(
        short_name=SHORT_NAME,
        name=PLUGIN_NAME,
        version=VERSION
    )


def hook_registry():
    """Register plugin hooks"""
    return {
        'yield_homepage_element': {
            'module': 'plugins.customsubmission.hooks',
            'function': 'yield_homepage_element',
        }
    }


def is_workflow_plugin():
    """This plugin modifies workflow"""
    return False