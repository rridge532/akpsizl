from django.shortcuts import render, redirect, HttpResponse, HttpResponseRedirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.urls import reverse
from datetime import datetime
from django.utils import timezone, http
from django.core.cache import cache
import statistics
import qrcode

from users.models import Profile, brother_check, exec_check
from .models import RushNight, RusheeSignin, Interview, Application, Mention, Vote
from .forms import ChangeNightForm, InterviewForm, RusheeSigninForm, RusheeSignupForm, ApplicationForm

# REMOVE THIS, THIS IS JUST FOR TESTING TO CONSISTENTLY SET NIGHT
if cache.get('night') is None:
    cache.set('night', RushNight.objects.first(), None)

def get_night():
    night = cache.get('night')
    try:
        night= get_object_or_404(RushNight, id=night.id)
    except:
        night = None
    return night

def rushee_check(user):
    return not user.profile.isbrother and not user.profile.isloa and not user.profile.isexec

def qrcodeimage(request, nightid):
    night = get_object_or_404(RushNight, id=nightid)
    address = 'https://akpsirush.com/rush/{}/rusheesignin'.format(night.id)
    img = qrcode.make(address)
    response = HttpResponse(content_type="image/png")
    img.save(response, "PNG")
    return response

# Create your views here.

def thanks(request):
    context = request.session['context']
    return render(request, 'rush/thanks.html', context)

@login_required
@user_passes_test(exec_check, redirect_field_name=None)
def changenight(request):
    form = ChangeNightForm(request.POST or None,
                           initial = {'rushnight': RushNight.objects.filter(date=datetime.today()).first()})
    if request.POST and form.is_valid():
        night = form.cleaned_data['rushnight']
        cache.set('night', night, None)
        newnight = get_night()
        message = "You have successfully changed the night to %s." % newnight
        buttons = (('Home', '/'), )
        context = {
            'person': request.user.first_name,
            'message': message,
            'buttons': buttons,
        }
        request.session['context'] = context
        return redirect('rush:thanks')
    else:
        form = ChangeNightForm(initial = {'rushnight': RushNight.objects.filter(date=datetime.today()).first()})
    return render(request, 'rush/changenight.html', {'form': form})

@login_required
@user_passes_test(brother_check, redirect_field_name=None)  # Just to be extra sure only let brothers access this view.
def createsignin(request, rushee, night):
    signin, created = RusheeSignin.objects.get_or_create(rushee=rushee, night=night)
    if created:
        signin.save()
    message = "You successfully signed in to %s." % night.name
    buttons = (('New Signin', '/rush/signin'), )
    altbuttons = (('Home', '/'), )
    context = {
        'person': rushee.first_name,
        'message': message,
        'buttons': buttons,
        'altbuttons': altbuttons,
    }
    request.session['context'] = context
    return redirect('rush:thanks')

@login_required
@user_passes_test(brother_check, redirect_field_name=None) # Only let brothers use this view
# TODO: Check if the brother is authorized to sign rushees in? Maybe restrict to rush team members?
# This would required pulling in EventGroup and/or TeamMembership
def rusheesignin(request):
    night = get_night()
    if night:
        if not night.voting:
            signinform = RusheeSigninForm(request.POST or None)
            signupform = RusheeSignupForm()
            if request.POST and signinform.is_valid():
                rushee = signinform.login(request)
                if rushee:
                    return createsignin(request, rushee, night)
            context = {
                'signinform': signinform,
                'signupform': signupform,
                'night': night,
            }
            return render(request, 'rush/rusheesignin.html', context)
    message = "We are not currently accepting any new rush signins."
    context = {
        'message': message,
    }
    return render(request, 'base/error.html', context=context)

@login_required
@user_passes_test(brother_check, redirect_field_name=None)
def rusheesignup(request):
    night = get_night()
    if night:                                                       # only allow if it's during rush
        if not night.voting:                                        # only allow if it's not voting night (throws error if done with night check)
            if request.method == 'POST':                            # check that the user is trying to submit
                signupform = RusheeSignupForm(request.POST)               # pull the POST form data into an object
                if signupform.is_valid():                                 # check that form data is valid
                    rushee = signupform.save(commit=False)                # save the form to an object but don't write it to the db yet
                    rushee.username = rushee.username.lower()       # username should be lowercase
                    rushee.first_name = rushee.first_name.title()   # first letter should be capitalized
                    rushee.last_name = rushee.last_name.title()     # first letter should be capitalized
                    rushee.email = rushee.email.lower()             # email should be lowercase
                    rushee.save()
                    if rushee:
                        return createsignin(request, rushee, night)
                context = {
                    'signinform': RusheeSigninForm(),
                    'signupform': signupform,
                    'night': night,
                }
                return render(request, 'rush/rusheesignin.html', context)   # if submitted but form is not valid, reload with errors
    return HttpResponseRedirect(reverse('rush:rusheesignin'))               # if not submission, redirect to signin view (helps with consistency)

@login_required
@user_passes_test(brother_check, redirect_field_name=None)
def interview(request):
    night = get_night()
    if night:
    # night = get_object_or_404(RushNight, pk=night)
        if night.interviews: 
            if request.method == 'POST':
                form = InterviewForm(request.POST)
                if form.is_valid():
                    newinterview = form.save(commit=False)
                    oldinterview = Interview.objects.get(interviewer=request.user, rushee=newinterview.rushee)
                    if oldinterview:
                        form = InterviewForm(request.POST, instance=oldinterview)
                        newinterview = form.save(commit=False)
                    newinterview.interviewer = request.user
                    newinterview.save
                    message = "Your interview with %s has been recorded." % (form.cleaned_data['rushee'])
                    interview = ('New Interview', '/rush/interview')
                    home = ('Home', '/')
                    buttons = (interview, )
                    altbuttons = (home, )
                    context = {
                        'person': request.user,
                        'message': message,
                        'buttons': buttons,
                        'altbuttons': altbuttons,
                    }
                    return render(request, 'rush/thanks.html', context)
            else:
                form = InterviewForm()
            context = {
                'form': form,
                'containersize': 'medium',
            }
            return render(request, 'rush/interview.html', context)
        else:
            message = "Interviews are not allowed for this night of Rush."
    else:
        message = "Tonight is not a night of Rush. Please come back later."
    context = {
        'message': message,
    }
    return render(request, 'base/error.html', context=context)

@login_required
@user_passes_test(rushee_check, redirect_field_name=None)
def application(request):
    rushee = request.user
    night = get_night()
    if night:
        if not night.voting:
            previousapp = Application.objects.filter(rushee=rushee).first()
            form = ApplicationForm(request.POST or None, instance=previousapp)
            if request.POST and form.is_valid():
                application = form.save(commit=False)
                application.rushee = rushee
                application.save()
                return HttpResponse(application)
            context = {
                'form': form,
                'containersize': 'medium',
            }
            return render(request, 'rush/application.html', context)
    message = "We are not currently accepting any new rush applications."
    context = {
        'message': message,
    }
    return render(request, 'base/error.html', context=context)

"""
@login_required
@user_passes_test(exec_check, redirect_field_name=None)
def interviewstats(requrest):
    num = Interview.objects.count()
    interviews = Interview.objects.all()

    if(num == 0):
        return HttpResponse("No scores")
    
    # sums
    suminterest = sum(interview.interest for interview in Interview.objects.iterator())
    sumenergy = sum(interview.energy for interview in Interview.objects.iterator())
    sumfriend = sum(interview.friendliness for interview in Interview.objects.iterator())

    # averages
    avginterest = suminterest / num
    avgenergy = sumenergy / num
    avgfriend = sumfriend / num
    
    # maximums
    maxinterest = max(interviews, key = lambda x: x.interest)
    maxenergy = max(interviews, key = lambda x: x.energy)
    maxfriend = max(interviews, key = lambda x: x.friendliness)
    
    # minimums
    mininterest = min(interviews, key = lambda x: x.interest)
    minenergy = min(interviews, key = lambda x: x.energy)
    minfriend = min(interviews, key = lambda x: x.friendliness)
"""