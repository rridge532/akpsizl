from django.urls import path
from django.views.generic.base import TemplateView

from . import views

app_name = 'rush'
urlpatterns = [
    path('', TemplateView.as_view(template_name='rush/portal.html'), name='portal'),
    path('changenight/', views.changenight, name='changenight'),
    path('signin/', views.rusheesignin, name='rusheesignin'),
    path('signup/', views.rusheesignup, name='rusheesignup'),
    path('powerpoint/', views.powerpoint, name='powerpoint'),
    path('powerpoint/<int:page>/', views.powerpoint, name='powerpoint'),
    path('bids/', views.biddisplay, name='biddisplay'),
    path('application/', views.application, name='application'),
    path('mention/', views.mention, name='mention'),
    path('interview/', views.interview, name='interview'),
    path('prevote/', views.prevote, name='prevote'),
    path('prevote/<int:page>/', views.prevote, name='prevote'),
    path('vote/', views.vote, name='vote'),
    path('vote/<int:page>/', views.vote, name='vote'),
    path('thanks/', views.thanks, name='thanks'),
    path('emails/', views.emails, name='emails'),
    path('addresses/', views.addresses, name='addresses'),
]