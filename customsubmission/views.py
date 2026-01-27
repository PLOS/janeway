from formtools.wizard.views import SessionWizardView
from django.shortcuts import render
from django.views.generic import TemplateView
from .forms import Step1Form, Step2Form, Step3Form, HumanChecklistForm

FORMS = [("step1", Step1Form),
         ("step2", Step2Form),
         ("step3", Step3Form),
         ("human_checklist", HumanChecklistForm)]

TEMPLATES = {"step1": "customsubmission/start_step1.html",
             "step2": "customsubmission/start_step2.html",
             "step3": "customsubmission/start_step3.html",
             "human_checklist": "customsubmission/human_checklist.html"}

def show_human_checklist(wizard):
    cleaned_data = wizard.get_cleaned_data_for_step('step3') or {}
    return cleaned_data.get('human_participants', False) == 'yes'

class CustomSubmissionWizard(SessionWizardView):
    condition_dict = {'human_checklist': show_human_checklist}
    form_list = FORMS

    def get_template_names(self):
        return [TEMPLATES[self.steps.current]]

    def done(self, form_list, **kwargs):
        # Process the data and redirect to a success page
        cleaned_data = [form.cleaned_data for form in form_list]
        return render(self.request, 'customsubmission/start_done.html', {
            'form_data': cleaned_data,
        })

class ManagerView(TemplateView):
    template_name = "customsubmission/manager.html"
