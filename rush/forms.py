from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from users.models import Profile
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
    username = forms.CharField(max_length=255,
                               label='NetID',
                               widget=forms.TextInput(attrs = {'placeholder': 'NetID'}),)
    first_name = forms.CharField(max_length=50,
                                 widget=forms.TextInput(attrs = {'placeholder': 'First Name'}),)
    last_name = forms.CharField(max_length=50,
                                widget=forms.TextInput(attrs = {'placeholder': 'Last Name'}),)
    email = forms.EmailField(max_length=254,
                             widget=forms.TextInput(attrs = {'placeholder': 'Email'}),)
    password1 = forms.CharField(max_length=255,
                                label='Password',
                                widget=forms.PasswordInput(attrs = {'placeholder': 'Password'}),)
    password2 = forms.CharField(max_length=255,
                                label='Password confirmation',
                                widget=forms.PasswordInput(attrs = {'placeholder': 'Password confirmation'}),)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )

class RusheeProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = (
            'preferred_name',
            'pronouns',
            'gender',
            'race',
        )

class RusheeSigninForm(forms.Form):
    username = forms.CharField(label='NetID',
                               max_length=255,
                               widget=forms.TextInput(attrs = {'placeholder': 'NetID'}),)
    password = forms.CharField(max_length=255,
                               widget=forms.PasswordInput(attrs = {'placeholder': 'Password'}),)
    
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
    
    class Meta:
        widgets = {
            'username': forms.TextInput(attrs = {'placeholder': 'NetID'}),
            'password': forms.PasswordInput(attrs = {'placeholder': 'Password'}),
        }

class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        exclude = ['rushee']
        widgets = {
            'WhyAKPsi': forms.Textarea(attrs={'cols': 80, 'rows': 5}),
            'involvement': forms.Textarea(attrs={'cols': 80, 'rows': 5}),
            'aboutme': forms.Textarea(attrs={'cols': 80, 'rows': 5}),
            'essay': forms.Textarea(attrs={'cols': 80, 'rows': 8}),
        }

class UserModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, user):
        return "%s (%s)" % (user.get_full_name(), user.username)

class RusheeForm(forms.Form):
    rushee = UserModelChoiceField(
        User.objects.filter(profile__isbrother=False, profile__isexec=False, profile__isloa=False).order_by('first_name'),
        # label = 'Please select a Rushee below:',
        required = True,
    )

class MentionForm(forms.ModelForm):
    class Meta:
        model = Mention
        exclude = ['night', 'brother', 'rushee']

class VoteForm(forms.ModelForm):
    class Meta:
        model = Vote
        exclude = ['']
        widgets = {
            'brother': forms.HiddenInput(),
            'rushee': forms.HiddenInput(),
        }