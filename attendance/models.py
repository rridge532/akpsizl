from datetime import datetime

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.utils.crypto import get_random_string

# Create your models here.

# Brother Profile
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    isbrother = models.BooleanField(default=0)
    isexec = models.BooleanField(default=0)
    isloa = models.BooleanField(default=0)
    issenior = models.BooleanField(default=0)

    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()

def validate_not_negative(value):
    if value < 0:
        raise ValidationError(
            _('%(values)s is not 0 or higher'),
            params={'value': value},
        )

# Event Types
class EventGroup(models.Model):
    name = models.CharField(max_length=100, null=False)
    needed_credits = models.IntegerField(default=0, null=False, validators=[validate_not_negative])
    senior_credits = models.IntegerField(default=0, null=False, validators=[validate_not_negative])

    def __str__(self):
        return self.name

    def get_events(self):
        return Event.objects.filter(group=self).all()

    def credits_available(self):
        return sum(x['credits'] for x in Event.objects.filter(group=self).values('credits'))

class Event(models.Model):
    name = models.CharField(max_length=100, null=False)
    group = models.ForeignKey(EventGroup, on_delete=models.SET_NULL, null=True)
    credits = models.IntegerField(default=1, null=False)
    date = models.DateField(default=datetime.now)
    slug = models.CharField(max_length=32, default='', null=True, blank=True)

    def __str__(self):
        return self.name
#        return str(self.group) + ': ' + self.name + ' (' + str(self.credits) + ')'

    class Meta:
        ordering = ('date','group','name')

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
