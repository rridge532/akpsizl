from django.shortcuts import render, HttpResponse, HttpResponseRedirect, get_object_or_404
from django.utils.crypto import get_random_string
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from datetime import datetime
from django.utils import timezone
from django.views import View
from django.contrib import messages
from random import randint
import qrcode

from .models import Event, EventGroup, Profile, Signin
# Helper functions

# From qrcodeimage and getqrimage with removal of signout
def qrcodeimage(request, eventid):
    event = get_object_or_404(Event, id=eventid)
    address = 'https://akpsirush.com/attendance/{}/{}/signin'.format(event.id, event.slug)
    img = qrcode.make(address)
    response = HttpResponse(content_type="image/png")
    img.save(response, "PNG")
    return response

# From getprettynowtimestring and makeadatetimepretty
def get_prettydatetime(datetimeobj=''):
    if datetimeobj == '': datetimeobj = timezone.now()
    return datetimeobj.strftime('%X on %a %b %d ')

# Get the user object from a profile's pk; useful for building lists off profile attributes
def get_userfromprofile(profile):
    user = User.objects.get(pk=profile.pk)
    return user

# Get the profile object from a profile's pk; useful for grabbing a user's profile attributes
def get_profilefromuser(user):
    profile = Profile.objects.get(pk=user.pk)
    return profile

# Create your views here.

# From signinqr
# Take event id and display the signin qrcode for that event
@login_required
def signinqr(request, eventid):
    profile = get_profilefromuser(request.user)
    if profile.isexec:
        event = get_object_or_404(Event, id=eventid)
        signincount = Signin.objects.filter(event=event).count()
        recentsignin = Signin.objects.filter(event=event).order_by('-time')[:5][::-1]
        context = {
            'event': event,
            'signincount': signincount,
            'recentsignin': recentsignin,
        }
    return render(request, 'attendance/signinqr.html', context=context)

# From signinapi
# Takes event and user info to create a signin with basic manual signin prevention
@login_required
def signinapi(request, eventid, eventslug):
    user = request.user
    event = get_object_or_404(Event, id=eventid)
    # Check the slug to prevent manual typing of the URL
    if event.slug == eventslug:
        signin, created = Signin.objects.get_or_create(user=user, event=event)
        # Only try to save the signin if it is newly created
        if created:
            signin.save()
    # Slug doesn't match, possibly somebody faking a signin, raise an exception
    else:
        raise Exception('Not so fast')
        
    return HttpResponseRedirect(reverse('attendance:signinsuccess', args=(eventid,)))

# Adapted from thank
# Returns signinsuccess if signin exists for that user for that event. Throws an error otherwise.
@login_required
def signinsuccess(request, eventid):
    user = request.user
    event = Event.objects.get(id=eventid)
    signin = get_object_or_404(Signin, user=user, event=event)
    context = {
        'signin': signin,
    }
    return render(request, 'attendance/signinsuccess.html', context=context)

@login_required
def index(request):
    return HttpResponse('Hello world')    

# Handles 404 errors to show a custom page
def handler404(request, exception):
    message = [
        "Whoops, looks like the page you're looking for doesn't exist.",
    ]
    context = {
        'message': message[randint(0,1)]
    }
    return render(request, '404.html', context, status=404)

# Handles 500 errors to show a custom page
def handler500(request):
    message = [
        "Whoops, looks like the page you're looking for doesn't exist.",
    ]
    context = {
        'message': message[randint(0,1)]
    }
    return render(request, '500.html', context, status=500)

# From getattendance; 
def attendancedraft(request, eventid):
    event = get_object_or_404(Event, id=eventid)
    brotherlist = 'Name \n'
    brothers = Profile.objects.filter(isbrother=1).all()
    for brother in brothers:
        user = get_userfromprofile(brother)
        attendeelist += str() + '\n'
    return HttpResponse(brotherlist, content_type='text/plain')
