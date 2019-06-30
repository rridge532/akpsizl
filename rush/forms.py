from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import RushNight, Interview, RusheeSignin, Mention, Vote, Application

class ChangeNightForm(forms.Form):
    rushnight = forms.ModelChoiceField(
        RushNight.objects.all(),
        to_field_name = None, 
        label = '',
        help_text = 'Only change this right before the event begins.',
        empty_label = 'None',
        required = False,
    )
    
class InterviewForm(forms.ModelForm):
    class Meta:
        model = Interview
        exclude = ['interviewer']
        widgets = {
            'comment': forms.Textarea(attrs={'cols': 80, 'rows': 3}),
        }

class RusheeSignupForm(UserCreationForm):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    email = forms.EmailField(max_length=254)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'password1', 'password2', )

class RusheeSigninForm(forms.Form):
    username = forms.CharField(label='NetID', max_length=30)
    password = forms.CharField(widget=forms.PasswordInput(), max_length=50)
    # class Meta:
    #     model = User