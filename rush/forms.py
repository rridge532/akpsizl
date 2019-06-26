from django import forms
from django.contrib.auth.models import User
from .models import RushNight, Interview, RusheeSignin, Mention, Vote, Application

class ChangeNightForm(forms.Form):
    rushnight = forms.ModelChoiceField(
        RushNight.objects.all(),
        to_field_name=None, 
        label='',
        help_text='Only change this right before the event begins.',
        empty_label='None',
        required=False
    )
    
class InterviewForm(forms.ModelForm):
    class Meta:
        model = Interview
        exclude = ['interviewer']
        widgets = {
            'comment': forms.Textarea(attrs={'cols': 80, 'rows': 3}),
        }