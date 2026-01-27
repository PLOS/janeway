from django.urls import path, re_path
from plugins.customsubmission import views
from .views import FORMS

urlpatterns = [
    path('start/', views.CustomSubmissionWizard.as_view(FORMS), name='custom_submission_wizard'),
    path('manager/', views.ManagerView.as_view(), name='customsubmission_manager'),
]
