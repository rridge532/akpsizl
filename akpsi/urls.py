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
    path('admin/', admin.site.urls),
    path('attendance/', include('attendance.urls')),
    # path('rush/', include('rush.urls')),
    # path('base/', include('base.urls')),
    # path('users/', include('users.urls')),
    path('accounts/login/', auth_views.LoginView.as_view(redirect_authenticated_user=True), name='login'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', TemplateView.as_view(template_name='base/index.html', extra_context={'landing': 'landing', 'headerclass': 'alt'}), name='index'),
    path('generic.html', TemplateView.as_view(template_name='generic.html'), name='generic'),
    path('elements.html', TemplateView.as_view(template_name='elements.html'), name='elements'),
    path('contact.html', TemplateView.as_view(template_name='contact.html'), name='contact'),
]

handler404 = base_views.handler404
handler500 = base_views.handler500