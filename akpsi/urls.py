"""akpsi URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import TemplateView
from django.contrib.auth import views as auth_views
from base import views as base_views

urlpatterns = [
    path('exec/', admin.site.urls, name='exec'),
    path('attendance/', include('attendance.urls')),
    path('rush/', include('rush.urls')),
    path('', include('base.urls')),
    # path('users/', include('users.urls')),
    path('accounts/login/', auth_views.LoginView.as_view(redirect_authenticated_user=True), name='login'),
    path('accounts/password_change/', base_views.password_change, name='password_change'),
    path('accounts/', include('django.contrib.auth.urls')),
]

handler404 = base_views.handler404
handler500 = base_views.handler500