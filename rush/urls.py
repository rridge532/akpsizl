from django.urls import path
from . import views

app_name = 'rush'
urlpatterns = [
    path('thanks/', views.thanks, name='thanks'),
    path('changenight/', views.changenight, name='changenight'),
    path('interview/', views.interview, name='interview'),
    path('signin/', views.rusheesignin, name='rusheesignin'),
    path('signup/', views.rusheesignup, name='rusheesignup'),
    path('application/', views.application, name='application'),
    path('mention/', views.mention, name='mention'),
    path('vote/', views.vote, name='vote'),
    path('vote/<int:page>/', views.vote, name='vote'),
]