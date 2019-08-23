from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from random import randint
from django.contrib.auth.decorators import login_required

# Create your views here.
# Handles 404 errors to show a custom page
def handler404(request, exception):
    message = [
        "Whoops, looks like the page you're looking for doesn't exist.",
        "Oh my, the Oompa Loompas seem to have lost the page you're looking for.",
        "On Wednesdays we wear pink, and on this page we tell you the page you're looking for doesn't exist.",
        "These aren't the droids, I mean pages, you are looking for."
    ]
    context = {
        'message': message[randint(0,3)]
    }
    return render(request, 'base/error.html', context, status=404)

# Handles 500 errors to show a custom page
def handler500(request):
    message = [
        "Oh no, we couldn't find what it is that you're looking for.",
        "The Oompa Loompas are confused. They couldn't find what you're looking for.",
        "We couldn't find the content you were looking for. So not fetch.",
    ]
    context = {
        'message': message[randint(0,2)]
    }
    return render(request, 'base/error.html', context, status=500)

@login_required
def portal(request):
    return render(request, 'base/brotherportal.html')

def password_change(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('password_change')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'registration/password_change.html', {'form': form})