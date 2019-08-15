from django.shortcuts import render, redirect, HttpResponse, HttpResponseRedirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.urls import reverse
from django.db.models import Avg
from datetime import datetime
from django.utils import timezone, http
from django.core.cache import cache
import statistics
import qrcode

from users.models import Profile, brother_check, exec_check
from .models import RushNight, RusheeSignin, Interview, Application, Mention, Vote
from .forms import ChangeNightForm, InterviewForm, RusheeSigninForm, RusheeSignupForm, ApplicationForm, RusheeForm, MentionForm, VoteForm

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

def get_InterviewScores(rushee):
    qs = Interview.objects.filter(rushee=rushee).aggregate(Avg('interest'), Avg('energy'), Avg('friendliness'))
    returndict = {}
    for key, val in qs.items():
        returndict[key.split('__')[0]] = val
    return returndict

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
                message = "Thanks for submitting a rush application."
                buttons = (('Edit Application', '/rush/application'), )
                altbuttons = (('Home', '/'), )
                context = {
                    'person': rushee.first_name,
                    'message': message,
                    'buttons': buttons,
                    'altbuttons': altbuttons,
                }
                request.session['context'] = context
                return redirect('rush:thanks')
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

@login_required
@user_passes_test(brother_check, redirect_field_name=None)
def mention(request):
    night = get_night()
    if night:
        if not night.voting:
            # rushee = rusheeform.cleaned_data['rushee']
            rusheeform = RusheeForm(request.GET or None)
            mentionform = MentionForm(request.POST or None)
            if request.method == 'POST':
                if mentionform.is_valid():
                    rushee = User.objects.filter(id=request.session['rushee']).first()
                    previousmention = Mention.objects.filter(rushee=rushee, brother=request.user).first()
                    mentionform = MentionForm(request.POST or None, instance=previousmention)
                    mention = mentionform.save(commit=False)
                    mention.rushee = rushee
                    mention.brother = request.user
                    mention.night = night
                    mention.save()
                    message = "Thanks for submitting a mention for %s." % mention.rushee.get_full_name()
                    buttons = (('New Mention', '/rush/mention/'), )
                    altbuttons = (('Home', '/'), )
                    context = {
                        'person': request.user.first_name,
                        'message': message,
                        'buttons': buttons,
                        'altbuttons': altbuttons,
                    }
                    request.session['context'] = context
                    return redirect('rush:thanks')
            if request.method == 'GET':
                rusheeform = RusheeForm(request.GET or None)
                if rusheeform.is_valid():
                    rushee = rusheeform.cleaned_data['rushee']
                    request.session['rushee'] = rushee.id
                    rushee = User.objects.get(id=request.session['rushee'])
                    previousmention = Mention.objects.filter(rushee=rushee, brother=request.user).first()
                    mentionform = MentionForm(instance=previousmention)
                    context = {
                        'form': mentionform,
                        'containersize': 'medium',
                        'rushee': rushee,
                        'night': night,
                    }
                    return render(request, 'rush/mention.html', context)
            context = {
                'title': 'Make a Mention',
                'message': 'Select a Rushee to make a mention.',
                'parentview': '',
                'form': rusheeform,
            }
            return render(request, 'rush/rushee.html', context)
    message = "We are not currently accepting any new rush mentions."
    context = {
        'message': message,
    }
    return render(request, 'base/error.html', context=context)

@login_required
@user_passes_test(brother_check, redirect_field_name=None)
def vote(request, page = 1):
    night = get_night()
    if night:
        if night.voting:
            applications = Application.objects.order_by('rushee__first_name').all()
            paginator = Paginator(applications, 1)
            try:
                page = paginator.page(page)
            except (EmptyPage, PageNotAnInteger):
                return HttpResponseRedirect(reverse('rush:vote', kwargs={'page': 1}))
            application = page.object_list[0]
            rushee = application.rushee
            previousvote = Vote.objects.filter(rushee=rushee, brother=request.user).first()
            form = VoteForm(request.POST, instance=previousvote)
            if request.method == 'POST' and form.is_valid():
                vote = form.save(commit=False)
                vote.save()
                if page.has_next():
                    nextpage = page.next_page_number()
                    page = paginator.page(nextpage)
                    # Note that this only works since there is a single object on each page, i.e. index is identical to page
                    nexturl = '/rush/vote/%s/' % page.number
                    buttons = (('Next Vote', nexturl), )
                else:
                    buttons = None
                message = "Thanks for submitting a vote for %s." % rushee.get_full_name()
                editurl = '/rush/vote/%s/' % page.number
                altbuttons = (('Change Vote', editurl), ('Home', '/'), )
                context = {
                    'person': request.user.first_name,
                    'message': message,
                    'buttons': buttons,
                    'altbuttons': altbuttons,
                }
                request.session['context'] = context
                return redirect('rush:thanks')
            mentions = Mention.objects.filter(rushee=rushee).all()
            positivementions = mentions.filter(mentiontype='P').all()
            negativementions = mentions.filter(mentiontype='N').all()
            context = {
                'page': page,
                'form': form,
                'containersize': 'large',
                'application': application,
                'positivementions': positivementions,
                'negativementions': negativementions,
                'rushee': rushee,
                'brother': request.user,

            }
            return render(request, 'rush/vote.html', context)
    message = "Rush voting is not open at this time."
    context = {
        'message': message,
    }
    return render(request, 'base/error.html', context=context)

@login_required
@user_passes_test(exec_check, redirect_field_name=None)
def powerpoint(request, page = 1):
    night = get_night()
    if night:
        if night.voting:
            applications = Application.objects.order_by('rushee__first_name').all()
            paginator = Paginator(applications, 1)
            try:
                page = paginator.page(page)
            except (EmptyPage, PageNotAnInteger):
                return HttpResponseRedirect(reverse('rush:powerpoint', kwargs={'page': 1}))
            application = page.object_list[0]
            rushee = application.rushee
            mentions = Mention.objects.filter(rushee=rushee).all()
            positivementions = mentions.filter(mentiontype='P').all()
            negativementions = mentions.filter(mentiontype='N').all()
            interviews = Interview.objects.filter(rushee=rushee).all()
            nightsattended = RusheeSignin.objects.filter(rushee=rushee).all()
            scores = get_InterviewScores(rushee)
            context = {
                'page': page,
                'containersize': 'large',
                'application': application,
                'positivementions': positivementions,
                'negativementions': negativementions,
                'interviews': interviews,
                'scores': scores,
                'nightsattended': nightsattended,
                'rushee': rushee,

            }
            return render(request, 'rush/powerpoint.html', context)
    message = "Rush voting is not open at this time."
    context = {
        'message': message,
    }
    return render(request, 'base/error.html', context=context)

"""
@login_required
@user_passes_test(exec_check, redirect_field_name=None)
def interviewstats(request):
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
@login_required
@user_passes_test(exec_check, redirect_field_name=None)
def biddisplay(request):
    if Vote.objects.count() == 0:
        context = {
            'message': "There are no votes for rush.",
        }
        return render(request, 'base/error.html', context=context)
    
    nobids = []
    bids = []
    votes = Vote.objects.all()
    applications = Application.objects.all()
    activebrothers = User.objects.filter(profile__isbrother=True, profile__isloa=False).count()

    for application in applications:
        rushee = application.rushee
        novotes = votes.filter(rushee=rushee, choice='N').count()
        totalvotes = votes.filter(rushee=rushee).count()
        # CHANGE THIS AFTER FINISHED TESTING
        # if rusheevotes <= 20 or novotes >= (0.25 * activebrothers):
        if totalvotes <= 2 or novotes >= (0.25 * 20):
            nobids.append((rushee, novotes, totalvotes))
        else:
            bids.append((rushee, novotes, totalvotes))
    
    context = {
        'activebrothers': activebrothers,
        'nobids': nobids,
        'bids': bids,
        'containersize': 'large',
    }
    return render(request, 'rush/biddisplay.html', context=context)

# Helpful extra views for rushees, these should be replaced or improved on
@login_required
@user_passes_test(exec_check, redirect_field_name=None)
def rusheeemails(request):
    return HttpResponse('emails')

@login_required
@user_passes_test(exec_check, redirect_field_name=None)
def rusheeaddresses(request):
    return HttpResponse('addresses')

print(Vote.objects.count())