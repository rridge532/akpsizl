from django.urls import path
from django.views.generic.base import TemplateView

urlpatterns = [
    path('', TemplateView.as_view(template_name='base/index.html', extra_context={'landing': 'landing', 'headerclass': 'alt'}), name='index'),
    path('portal', TemplateView.as_view(template_name='base/brotherportal.html'), name='portal'),
    path('generic.html', TemplateView.as_view(template_name='base/generic.html'), name='generic'),
    path('elements.html', TemplateView.as_view(template_name='base/elements.html'), name='elements'),
    path('contact.html', TemplateView.as_view(template_name='base/contact.html'), name='contact'),
]