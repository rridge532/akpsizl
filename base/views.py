from django.shortcuts import render
from random import randint
from django.contrib.auth.decorators import login_required

# Create your views here.
# Handles 404 errors to show a custom page
def handler404(request, exception):
    message = [
        "Whoops, looks like the page you're looking for doesn't exist.",
    ]
    context = {
        'message': message[randint(0,1)]
    }
    return render(request, 'base/error.html', context, status=404)

# Handles 500 errors to show a custom page
def handler500(request):
    message = [
        "Oh no, we couldn't find what it is that you're looking for.",
    ]
    context = {
        'message': message[randint(0,1)]
    }
    return render(request, 'base/error.html', context, status=500)

@login_required
def portal(request):
    return render(request, 'base/brotherportal.html')