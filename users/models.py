from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

def brother_check(user):
    return user.profile.isbrother or user.profile.isexec or user.profile.isloa

def exec_check(user):
    return user.profile.isexec

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    isbrother = models.BooleanField(default=False)
    isexec = models.BooleanField(default=False)
    isloa = models.BooleanField(default=False)
    issenior = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()

class SignupToken(models.Model):
    token = models.CharField(max_length=255, unique=True, blank=False)
    signupallowed = models.BooleanField(default=True)

    def __str__(self):
        return self.token