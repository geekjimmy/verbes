from .models import Attempt
from django import forms
from django.forms import ModelForm

class AttemptForm(ModelForm):
    class Meta:
        model = Attempt
        fields = ['answer', 'conjugation']
        widgets = {
            'conjugation': forms.HiddenInput()
        }

    def clean_answer(self):
        self.cleaned_data['answer'] = self.cleaned_data['answer'].lower()
        return self.cleaned_data['answer']
