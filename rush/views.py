from django.shortcuts import render, HttpResponse, HttpResponseRedirect, get_object_or_404
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
from .forms import ChangeNightForm, InterviewForm

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

def qrcodeimage(request, eventid):
    night = get_object_or_404(RushNight, id=night)
    address = 'https://akpsirush.com/rush/{}/rusheesignin'.format(event.id)
    img = qrcode.make(address)
    response = HttpResponse(content_type="image/png")
    img.save(response, "PNG")
    return response

# Create your views here.
@login_required
@user_passes_test(exec_check, redirect_field_name=None)
def changenight(request):
    if request.method == 'POST':
        form = ChangeNightForm(request.POST)
        if form.is_valid():
            night = form.cleaned_data['rushnight']
            cache.set('night', night, None)
            newnight = get_night()
            message = "You have successfully changed the night to %s." % newnight
            home = ('Home', '/')
            altbuttons = (home, )
            context = {
                'person': request.user,
                'message': message,
                'altbuttons': altbuttons,
            }
            return render(request, 'rush/thanks.html', context)
    else:
        form = ChangeNightForm(initial = {'rushnight': RushNight.objects.filter(date=datetime.today()).first()})
    return render(request, 'rush/changenight.html', {'form': form})

@login_required
@user_passes_test(brother_check, redirect_field_name=None)
def rusheesignin(request):
    night = get_night()
    if night and not night.voting:
        if request.method == 'POST':
            form = ReturnRushee(request.POST)
            if form.is_valid:
                rusheeattendance = form.save(commit=False)
        else:
            form = ReturnRushee()
        context = {
            'form': form,
            'containersize': 'medium',
        }
        return render(request, 'rush/rusheesignin')
    else:
        message = "We are not currently accepting any new rush applications."
    context = {
        'message': message,
    }
    return render(request, 'base/error.html', context=context)

@login_required
@user_passes_test(brother_check, redirect_field_name=None)
def rusheesignup(request):
    if request.method == 'POST':
        form = RusheeSignupForm(request.POST)
        if form.is_valid():
            return HttpResponse('success')
    return HttpResponseRedirect(reverse(rusheesignin))

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