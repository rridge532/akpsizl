from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import TemplateView
from django.contrib.auth import views as auth_views
from base import views as base_views
from . import views

app_name = 'users'
urlpatterns = [
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('password_change/', base_views.password_change, name='password_change'),
    path('', include('django.contrib.auth.urls')),
    path('signup', views.signup, name='signup'),
    path('signupqr', views.signupqr, name='signupqr'),
]