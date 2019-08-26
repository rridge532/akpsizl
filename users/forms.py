from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.forms import ModelForm
from .models import SignupToken


class EditProfileForm(ModelForm):
    class Meta:
        model = User
        fields = (
            'email',
            'first_name',
            'last_name',
        )

class BrotherSignupForm(UserCreationForm):
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
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2',)

class SignupTokenForm(forms.Form):
    token = forms.CharField(max_length=255,
                            label='Signup Token',
                            widget=forms.TextInput(attrs = {'placeholder': 'Signup Token'}),)
                            
    def clean(self):
        token = self.cleaned_data['token']
        tokenmatch = SignupToken.objects.filter(token=token).first()
        if tokenmatch:
            if not tokenmatch.signupallowed:
                raise forms.ValidationError("Your signup token has expired.")
        else:
            raise forms.ValidationError("Your signup token is invalid.")
        return self.cleaned_data