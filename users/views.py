from django.shortcuts import render, redirect
from django.contrib.auth import update_session_auth_hash, authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import EditProfileForm, BrotherSignupForm, SignupTokenForm
from .models import SignupToken

# Create your views here.

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your profile was successfully updated!')
            return redirect('edit_profile')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = EditProfileForm(instance=request.user)
    return render(request, 'users/edit_profile.html', {'form': form})

def signup(request):
    if request.method == 'POST':
        signupform = BrotherSignupForm(request.POST, prefix='signupform')
        tokenform = SignupTokenForm(request.POST, prefix='tokenform')
        print("tokenform-token")
        if signupform.is_valid() and tokenform.is_valid():
            tokenmatch = SignupToken.objects.filter(token=tokenform.cleaned_data.get('token')).first()
            if tokenmatch:
                if tokenmatch.signupallowed:
                    brother = signupform.save(commit=False)
                    brother.username = brother.username.lower()
                    brother.first_name = brother.first_name.title()
                    brother.last_name = brother.last_name.title()
                    brother.email = brother.email.lower()
                    brother.save()
                    if brother:
                        brother.profile.isbrother = True
                        brother.save()
                    username = signupform.cleaned_data.get('username')
                    raw_password = signupform.cleaned_data.get('password1')
                    user = authenticate(username=username, password=raw_password)
                    login(request, user)
                    return redirect('portal')
    else:
        signupform = BrotherSignupForm(prefix='signupform')
        tokenform = SignupTokenForm(prefix='tokenform')
    context = {
        'signupform': signupform,
        'tokenform': tokenform,
    }
    return render(request, 'registration/signup.html', context)
