from django.shortcuts import render
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