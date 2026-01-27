from django.urls import path
from . import views
from .views import FORMS

urlpatterns = [
    path('submit/custom/', views.CustomSubmissionWizard.as_view(FORMS), name='custom_submission_wizard'),
]
