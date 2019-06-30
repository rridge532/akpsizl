from django import forms
from django.contrib.auth import authenticate
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
    username = forms.CharField(label='NetID', max_length=255, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)
    
    def clean(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        user = authenticate(username=username, password=password)
        if not user or not user.is_active:
            raise forms.ValidationError("Whoops, it looks like we don't have your info yet. Please sign up below or try again.")
        elif user.profile.isbrother or user.profile.isexec or user.profile.isloa:
            raise forms.ValidationError("Oops, it looks like you're already a brother!")
        return self.cleaned_data

    def login(self,request):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        user = authenticate(username=username, password=password)
        return user