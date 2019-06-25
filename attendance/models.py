from datetime import datetime
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.utils.crypto import get_random_string

# Create your models here.

def validate_not_negative(value):
    if value < 0:
        raise ValidationError(
            _('%(values)s is not 0 or higher'),
            params={'value': value},
        )

def make_iterator(s):
    try:
        len(s)
        return s
    except TypeError:
        return [s]

# Event Types
class EventGroup(models.Model):
    name = models.CharField(max_length=100, null=False, unique=True)
    needed_credits = models.IntegerField(default=0, null=False, validators=[validate_not_negative])
    senior_credits = models.IntegerField(default=0, null=False, validators=[validate_not_negative])

    def __str__(self):
        return self.name

    def get_events(self):
        return Event.objects.filter(group=self).all()

    def credits_available(self):
        return sum(x['credits'] for x in Event.objects.filter(group=self).values('credits'))

# Events
class Event(models.Model):
    name = models.CharField(max_length=100, null=False)
    group = models.ForeignKey(EventGroup, on_delete=models.SET_NULL, null=True)
    credits = models.IntegerField(default=1, null=False)
    date = models.DateField(default=datetime.now)
    slug = models.CharField(max_length=32, default='', null=True, blank=True)

    def __str__(self):
        return self.name
#        return str(self.group) + ': ' + self.name + ' (' + str(self.credits) + ')'

    def short_date(self):
        short_date = self.date.strftime("%m/%d")
        return short_date

@receiver(post_save, sender=Event)
def generate_random_slug(sender, instance, created, **kwargs):
    if created:
        randomstring = get_random_string(length=10)
        instance.slug = randomstring
        instance.save()

class Signin(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    time = models.DateTimeField(default=datetime.now, null=True, blank=True)
    comment = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return str(self.user) + ' signed in to ' + str(self.event)
    #    if self.signin:
    #        return str(self.user) + ' signed in to ' + str(self.event) + ' at ' + str(self.time)
    #    else:
    #        return str(self.user) + ' signed out of ' + str(self.event) + ' at ' + str(self.time)

    class Meta:
        unique_together = ('event', 'user')

# Define extra user attributes to make views easier
class UserFunctions:
    def __init__(self):
        self.signins = Signin.objects.filter(user=self)
        self.totalcredits = sum(signin.event.credits for signin in self.signins)

    # def get_activebrother(self):
    #     if self.profile.isbrother and not self.profile.isloa and not self.profile.isexec:
    #         return True
    #     return False

    # isactivebrother = property(get_activebrother)
    
    def eventgroupsignins(self, eventgroup):
        evgsignins = self.signins.filter(event__group=eventgroup)
        return evgsignins
    
    def eventgroupcredits(self, eventgroup):
        evgsignins = self.eventgroupsignins(eventgroup)
        evgcredits = sum(signin.event.credits for signin in evgsignins)
        return evgcredits

    def neededcredits(self, eventgroups):
        if self.profile.issenior:
            neededcredits = sum(evg.senior_credits for evg in make_iterator(eventgroups))
        else:
            neededcredits = sum(evg.needed_credits for evg in make_iterator(eventgroups))
        return neededcredits

    def missingcredits(self):
        eventgroups = EventGroup.objects.all()
        if self.totalcredits < self.neededcredits(eventgroups):
            return True
        for eventgroup in eventgroups:
            evgcredits = self.eventgroupcredits(eventgroup)
            if evgcredits < self.neededcredits(eventgroup):
                return True
        return False
    
    missingcredits = property(missingcredits)

User.__bases__ += (UserFunctions,)