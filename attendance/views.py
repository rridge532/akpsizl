from django.shortcuts import render, HttpResponse, HttpResponseRedirect, get_object_or_404
from django.utils.crypto import get_random_string
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.urls import reverse
from datetime import datetime
from django.utils import timezone
from django.views import View
# from django.contrib import messages
# from random import randint
import qrcode

from .models import Event, EventGroup, Signin
from users.models import Profile
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

# Create your views here.

# From signinqr
# Take event id and display the signin qrcode for that event
@login_required
def signinqr(request, eventid):
    if request.user.profile.isexec:
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

# Adapted from getsimpleattendance
@login_required
def eventattendance(request, eventid):
    event = get_object_or_404(Event, id=eventid)
    signincount = Signin.objects.filter(event=event).count()
    signins = Signin.objects.filter(event=event).order_by('user__last_name')
    context = {
        'event': event,
        'signincount': signincount,
        'signins': signins,
        'containersize': 'medium',
    }
    return render(request, 'attendance/eventattendance.html', context=context)

# Takes eventgroup object and signins object and provides signins for that group
class eventgroupsignins(object):
    def __init__(self, user, eventgroup, signins):
        self.user = user
        self.eventgroup = eventgroup
        self.signins = signins.filter(event__group=eventgroup, user=user)

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(eventgroupsignins, self).dispatch(*args, **kwargs)

    def count(self):
        return sum(signin.event.credits for signin in self.signins)

# Take userid as input otherwise use request.user
# Provide attendance broken down by event group. Include the count of attendance for that group
@login_required
def userattendance(request, userid=None):
    if request.user.profile.isexec and userid is not None:
        user=userid
    else:
        user=request.user
    signins = Signin.objects.filter(user=user)
    eventgroups = EventGroup.objects.all().order_by('name')
    evgsignins = {eventgroupsignins(user, eventgroup, signins) for eventgroup in eventgroups}
    evgsignins = sorted(evgsignins, key=lambda x: x.eventgroup.name)
    context = {
        'evgsignins': evgsignins,
    }
    return render(request, 'attendance/userattendance.html', context=context)

# Adapted from brothercredits
# This could be bettter
def brothercredits(request):
    notcredits = {}
    hascredits = {}
    userevgsignins = {}
    activebrothers = User.objects.filter(profile__isbrother=1, profile__isloa=0, profile__isexec=0).all()
    eventgroups = EventGroup.objects.all()
    activesignins = Signin.objects.filter(user__in=activebrothers)
    usersignins = {eventgroupsignins(activebro, eventgroup, activesignins) for eventgroup in eventgroups for activebro in activebrothers}
    for bro in activebrothers:
        evgsignins = {}
        for eventgroup in eventgroups:
            evgsignins[eventgroup] = eventgroupsignins(bro, eventgroup, activesignins)
        totalcredits = 0
        seniorscredits = 0
        normalcredits = 0
        creditsdict = {}
        missingcreds = False
        for eventgroup in eventgroups:
            userevgsignins = Signin.objects.filter(user=bro, event__group=eventgroup).all()
            creditsdict[eventgroup.name] = sum(signin.event.credits for signin in userevgsignins)
            totalcredits = totalcredits + sum(creditsdict.values())
            if bro.profile.issenior:
                if creditsdict[eventgroup.name] < eventgroup.senior_credits:
                    missingcreds = True
            else:
                if creditsdict[eventgroup.name] < eventgroup.needed_credits:
                    missingcreds = True
        totalcredits = sum(creditsdict.values())
        creditsdict['Total'] = totalcredits
        if missingcreds:
            notcredits[bro] = creditsdict
        else:
            hascredits[bro] = creditsdict

    context = {
        'notcredits': notcredits,
        'hascredits': hascredits,
        'eventgroups': eventgroups,
    }

    return render(request, 'attendance/brothercredits.html', context=context)
