from django import forms
from django.contrib.auth.models import User
from .models import RushNight, Interview, RusheeAttendance, Mention, Vote, Application

class ChangeNightForm(forms.Form):
    rushnight = forms.ModelChoiceField(RushNight.objects.all(),
    to_field_name=None)
    
