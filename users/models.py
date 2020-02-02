from django.db import models
from django.contrib.auth.models import User,AbstractUser
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

    # TODO: Confirm changing this string doesn't cause unexpected behavior
    def __str__(self):
        return "%s (%s)" % (self.user.get_full_name(), self.user.username)

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

# TODO: Validate this doesn't break existing templates
def get_user_string(self):
    return "%s (%s)" % (self.get_full_name(), self.username)

User.add_to_class("__str__", get_user_string)


# TODO: Test converting to the new user model. Can this be done gracefully? Can it be scripted?
# def user_avatar_path(instance, filename):
#     return 'user_{0}/avatar/{1}'.format(instance.id, filename)

# class User(AbstractUser):
#     avatar = models.ImageField(upload_to=user_avatar_path)

#     def __str__(self):
#         return "%s (%s)" % (self.get_full_name(), self.username)
