from django.urls import path
from django.views.generic.base import TemplateView

urlpatterns = [
    path('', TemplateView.as_view(template_name='base/index.html', extra_context={'landing': 'landing', 'headerclass': 'alt'}), name='index'),
    path('generic.html', TemplateView.as_view(template_name='generic.html'), name='generic'),
    path('elements.html', TemplateView.as_view(template_name='elements.html'), name='elements'),
    path('contact.html', TemplateView.as_view(template_name='contact.html'), name='contact'),
]