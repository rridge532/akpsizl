from django.shortcuts import render, HttpResponse, HttpResponseRedirect, get_object_or_404
from django.utils.crypto import get_random_string
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.utils.decorators import method_decorator
from django.template import Context, loader
from django.urls import reverse
from datetime import datetime
from django.utils import timezone
from django.views import View
# from django.contrib import messages
# from random import randint
import qrcode

from .models import Event, EventGroup, Signin, TeamMembership
from users.models import Profile, brother_check, exec_check
# Helper functions

# From qrcodeimage and getqrimage with removal of signout
def qrcodeimage(request, eventid, inorout):
    if not inorout == 'sign-in' and not inorout == 'sign-out':
        raise Exception('QR code is malformed. Must be sign-in or sign-out')
    event = get_object_or_404(Event, id=eventid)
    address = reverse('attendance:signinapi', args=(event.id, event.slug, inorout))
    # oldaddress = 'https://akpsizl.com/attendance/{}/{}/{}/api'.format(event.id, event.slug, inorout)
    qr = qrcode.QRCode()
    qr.add_data(address)
    qr.make(fit=True)
    img = qr.make_image(fill_color="#2D68C4", back_color="#FFD700")
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
@user_passes_test(brother_check, redirect_field_name=None)
def signinqr(request, eventid, inorout):
    event = get_object_or_404(Event, id=eventid)
    if request.user.memberofgroup(event.group) or request.user.profile.isexec:
        signins = Signin.objects.filter(event=event)
        signouts = signins.filter(signouttime__isnull=False)
        attendancecount = signins.count() - signouts.count()
        if inorout == 'sign-in':
            recent = signins.order_by('-signintime')[:5][::-1]
        elif inorout == 'sign-out':
            recent = signouts.order_by('-signouttime')[:5][::-1]
        else:
            return HttpResponseRedirect(reverse('attendance:eventattendance', args=(eventid,)))
        context = {
            'event': event,
            'attendancecount': attendancecount,
            'signincount': signins.count,
            'signoutcount': signouts.count,
            'recent': recent,
            'inorout': inorout,
        }
    else:
        raise Exception('Not so fast')
    return render(request, 'attendance/signinqr.html', context=context)

# From signinapi
# Takes event and user info to create a signin with basic manual signin prevention
@login_required
@user_passes_test(brother_check, redirect_field_name=None)
def signinapi(request, eventid, eventslug, inorout):
    event = get_object_or_404(Event, id=eventid)
    # Check the slug to prevent manual typing of the URL
    if event.slug == eventslug:
        signin, created = Signin.objects.get_or_create(user=request.user, event=event)
        # Only try to save the signin if it is newly created
        if inorout == 'sign-in':
            if created:
                signin.save()
        elif inorout == 'sign-out':
            if not created:
                if not signin.signouttime:
                    signin.signouttime = datetime.now()
                    signin.save()
            else:
                raise Exception('You must sign in first.')
        else:
            raise Exception('Only sign-in or sign-out are allowed.')
    # Slug doesn't match, possibly somebody faking a signin, raise an exception
    else:
        raise Exception('Not so fast')
    return HttpResponseRedirect(reverse('attendance:success', args=(eventid,inorout)))

# Adapted from thank
# Returns signinsuccess if signin exists for that user for that event. Throws an error otherwise.
@login_required
@user_passes_test(brother_check, redirect_field_name=None)
def success(request, eventid, inorout):
    event = get_object_or_404(Event, id=eventid)
    signin = get_object_or_404(Signin, user=request.user, event=event)
    if inorout == 'sign-in':
        time = signin.signintime
    elif inorout == 'sign-out':
        time = signin.signouttime
    else:
        return HttpResponseRedirect(reverse('attendance:userattendance'))
    context = {
        'signin': signin,
        'inorout': inorout,
        'time': time,
    }
    return render(request, 'attendance/success.html', context=context)

# Adapted from getsimpleattendance
@login_required
@user_passes_test(brother_check, redirect_field_name=None)
def eventattendance(request, eventid):
    event = get_object_or_404(Event, id=eventid)
    if request.user.memberofgroup(event.group) or request.user.profile.isexec:
        signins = Signin.objects.filter(event=event).order_by('user__last_name')
        context = {
            'event': event,
            'signins': signins,
            'containersize': 'medium',
        }
    else:
        raise Exception('Not so fast')
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
    evgsignins = {eventgroupsignins(user, eventgroup, user.signins) for eventgroup in eventgroups}
    evgsignins = sorted(evgsignins, key=lambda x: x.eventgroup.name)
    context = {
        'evgsignins': evgsignins,
    }
    return render(request, 'attendance/userattendance.html', context=context)

# Adapted from brothercredits
# This could be bettter
@login_required
@user_passes_test(exec_check, redirect_field_name=None)
def brothercredits(request):
    notcredits = {}
    hascredits = {}
    activebrothers = User.objects.filter(profile__isbrother=1, profile__isloa=0, profile__isexec=0).all()
    eventgroups = EventGroup.objects.filter(needed_credits__gt=0).all() | EventGroup.objects.filter(senior_credits__gt=0).all()
    for bro in activebrothers:
        creditsdict = {}
        for eventgroup in eventgroups:
            creditsdict[eventgroup.name] = bro.eventgroupcredits(eventgroup)
        creditsdict['Total'] = bro.totalcredits
        if bro.missingcredits:
            notcredits[bro] = creditsdict
        else:
            hascredits[bro] = creditsdict

    context = {
        'notcredits': notcredits,
        'hascredits': hascredits,
        'eventgroups': eventgroups,
        'containersize': 'large',
    }

    return render(request, 'attendance/brothercredits.html', context=context)

@login_required
@user_passes_test(exec_check, redirect_field_name=None)
def events(request):
    eventgroups = EventGroup.objects.all()
    context = {
        'eventgroups': eventgroups,
    }
    return render(request, 'attendance/events.html', context=context)

def creditscsv(request):
    brothercredits = {}
    activebrothers = User.objects.filter(profile__isbrother=1, profile__isloa=0, profile__isexec=0).all()
    eventgroups = EventGroup.objects.filter(needed_credits__gt=0).all() | EventGroup.objects.filter(senior_credits__gt=0).all()
    for bro in activebrothers:
        creditsdict = {}
        for eventgroup in eventgroups:
            creditsdict[eventgroup.name] = bro.eventgroupcredits(eventgroup)
        creditsdict['Total'] = bro.totalcredits
        brothercredits[bro] = creditsdict

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="brothercredits_%s.csv"' % timezone.now().strftime('%m-%d-%y_%H%M%S')
    
    template = loader.get_template('attendance/creditscsv.txt')
    context = {
        'brothercredits': brothercredits,
        'eventgroups': eventgroups,
    }
    response.write(template.render(context))
    return response

def meetingscsv(request):
    brothercredits = {}
    activebrothers = User.objects.filter(profile__isbrother=1, profile__isloa=0, profile__isexec=0).all()
    eventgroups = EventGroup.objects.filter(name='Brother Meeting').all()
    for bro in activebrothers:
        creditsdict = {}
        for eventgroup in eventgroups:
            creditsdict[eventgroup.name] = bro.eventgroupcredits(eventgroup)
        brothercredits[bro] = creditsdict

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="meetingattendance_%s.csv"' % timezone.now().strftime('%m-%d-%y_%H%M%S')
    
    template = loader.get_template('attendance/creditscsv.txt')
    context = {
        'brothercredits': brothercredits,
        'eventgroups': eventgroups,
    }
    response.write(template.render(context))
    return response