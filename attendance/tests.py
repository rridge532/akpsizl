from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.admin import User

from .models import Profile, Event

# Create your tests here.

# Create a user with senior status
def create_user():
    username = 'testuser'
    email = 'testuser@fake.com'
    password = 'testpassword'
    return User.objects.create_user(username, email, password)

def make_user_bool_true(booltotest):
    return setattr(Profile.objects.get(id=1), booltotest, True)
#    Profile.objects.filter(id=1).update(booltotest=1)

# class ProfileModelTest(TestCase):
#     def test_brother(self):
#         create_user()
#         make_user_bool_true('isbrother')
#         self.assertIs(Profile.objects.get(id=1).isbrother, True)