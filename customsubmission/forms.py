from django import forms

class Step1Form(forms.Form):
    name = forms.CharField(max_length=100)

class Step2Form(forms.Form):
    email = forms.EmailField()

class Step3Form(forms.Form):
    human_participants = forms.ChoiceField(
        choices=[('yes', 'Yes'), ('no', 'No')],
        widget=forms.RadioSelect,
        label="Does this study involve human participants?"
    )

class HumanChecklistForm(forms.Form):
    ethics_document_upload_confirmation = forms.BooleanField(
        label="Because you have human participants in your trial, you must upload an ethics document in order to be considered for publication.",
        help_text=(
            "Check this box to confirm you have uploaded your ethics document."
        ),
        required=True,
    )
