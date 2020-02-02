from django.db import models
from django.contrib.auth.models import User,AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from PIL import Image, ExifTags
import os

# Create your models here.

def brother_check(user):
    return user.profile.isbrother or user.profile.isexec or user.profile.isloa

def exec_check(user):
    return user.profile.isexec

def user_image_path(instance, filename):
    return 'images/user_{0}/{1}'.format(instance.id, filename)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    isbrother = models.BooleanField(default=False)
    isexec = models.BooleanField(default=False)
    isloa = models.BooleanField(default=False)
    issenior = models.BooleanField(default=False)
    image = models.ImageField(upload_to=user_image_path, null=True, blank=True)

    # TODO: Confirm changing this string doesn't cause unexpected behavior
    def __str__(self):
        return "%s (%s)" % (self.user.get_full_name(), self.user.username)

def rotate_image(filepath):
    try:
        image = Image.open(filepath)
        for orientation in ExifTags.TAGS.keys():
            if ExifTags.TAGS[orientation] == 'Orientation':
                break
        exif = dict(image._getexif().items())

        if exif[orientation] == 3:
            image = image.rotate(180, expand=True)
        elif exif[orientation] == 6:
            image = image.rotate(270, expand=True)
        elif exif[orientation] == 8:
            image = image.rotate(90, expand=True)
        image.save(filepath)
        image.close()
    except (AttributeError, KeyError, IndexError):
        # cases: image don't have getexif
        pass

@receiver(post_save, sender=Profile, dispatch_uid="update_image_profile")
def update_image(sender, instance, **kwargs):
    if instance.image:
        fullpath = os.path.join(os.path.dirname(settings.MEDIA_ROOT), instance.image.name)
        rotate_image(fullpath)

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
