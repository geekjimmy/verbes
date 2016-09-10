from .models import Attempt, MoodTense, UserMoodTense
from django import forms
from django.db import transaction
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


class UserMoodTenseForm(forms.Form):
    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)

        user_mood_tenses = UserMoodTense.objects.get_mood_tenses_for_user(user)
        all_mood_tenses = MoodTense.objects.all()

        for mood_tense in all_mood_tenses:
            field = forms.BooleanField(initial=mood_tense in user_mood_tenses,
                                       label=mood_tense.mood.name + ' ' + mood_tense.tense.name,
                                       required=False)
            field.widget.attrs.update({
                'mood_tense_id': mood_tense.id
            })
            self.fields[str(mood_tense.id)] = field

    @transaction.atomic
    def save(self, user):
        UserMoodTense.objects.filter(user=user).delete()

        user_mood_tenses = []
        for mood_tense_id, checked in self.cleaned_data.items():
            if checked:
                user_mood_tenses.append(UserMoodTense(user=user, mood_tense_id=mood_tense_id))

        UserMoodTense.objects.bulk_create(user_mood_tenses)
