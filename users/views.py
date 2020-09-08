from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth import update_session_auth_hash, authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
import qrcode

from .forms import EditUserForm, EditProfileForm, GenderForm, PronounsForm, RaceForm, BrotherSignupForm, SignupTokenForm
from .models import Gender, Pronouns, Race, Profile, SignupToken

# Create your views here.

@login_required
def edit_profile(request):
    if request.method == 'POST':
        userform = EditUserForm(request.POST, instance=request.user)
        profileform = EditProfileForm(request.POST, instance=request.user.profile)
        if userform.is_valid() and profileform.is_valid():
            user = userform.save()
            profile = profileform.save(commit=False)
            profile.user = user

            if 'profileform-image' in request.FILES:
                profile.image = request.FILES['profileform-image']
            profile.save()

            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your profile was successfully updated!')
            return redirect('users:edit_profile')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        userform = EditUserForm(instance=request.user)
        profileform = EditProfileForm(instance=request.user.profile)
    context = {
        'userform': userform,
        'profileform': profileform,
        'containersize': 'medium',
    }
    return render(request, 'users/edit_profile.html', context)

def signup(request):
    if request.method == 'POST':
        signupform = BrotherSignupForm(request.POST, prefix='signupform')
        profileform = EditProfileForm(request.POST, prefix='profileform')
        tokenform = SignupTokenForm(request.POST, prefix='tokenform')
        print("tokenform-token")
        if signupform.is_valid() and profileform.is_valid() and tokenform.is_valid():
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
                    
                    profileform = EditProfileForm(request.POST, prefix='profileform', instance=brother.profile)
                    profile = profileform.save(commit=False)
                    profile.user = brother
                    if 'profileform-image' in request.FILES:
                        profile.image = request.FILES['profileform-image']
                    profile.save()

                    username = signupform.cleaned_data.get('username')
                    raw_password = signupform.cleaned_data.get('password1')
                    user = authenticate(username=username, password=raw_password)
                    login(request, user)
                    return redirect('portal')
    else:
        signupform = BrotherSignupForm(prefix='signupform')
        profileform = EditProfileForm(prefix='profileform')
        tokenform = SignupTokenForm(prefix='tokenform')
    context = {
        'signupform': signupform,
        'profileform': profileform,
        'tokenform': tokenform,
    }
    return render(request, 'registration/signup.html', context)

@login_required
def signupqr(request):
    # address = "https://akpsizl.com/%s" % reverse('users:signup')
    address = request.build_absolute_uri(reverse('users:signup'))
    img = qrcode.make(address)
    response = HttpResponse(content_type="image/png")
    img.save(response, "PNG")
    return response

@login_required
def CreatePopup(request, forminstance, title):
    form = forminstance(request.POST or None)
    if form.is_valid():
        instance = form.save()
        ## Change the value of the "#id_author". This is the element id in the form
        return HttpResponse('<script>opener.closePopup(window, "%s", "%s", "#id_%s");</script>' % (instance.pk, instance, title))

    context = {
        'title': title,
        'form': form,
    }
    return render(request, "users/create_popup.html", context)

def GenderCreatePopup(request):
    return CreatePopup(request, GenderForm, 'gender')

def PronounsCreatePopup(request):
    return CreatePopup(request, PronounsForm, 'pronouns')

def RaceCreatePopup(request):
    return CreatePopup(request, RaceForm, 'race')
