from django.urls import path
from . import views

app_name = 'attendance'
urlpatterns = [
    path('events/', views.events, name='events'),
    path('<int:eventid>/<str:inorout>/qrcode', views.qrcodeimage, name='qrcodeimage'),
    path('<int:eventid>/<str:inorout>/qr', views.signinqr, name='signinqr'),
    path('<int:eventid>/<str:eventslug>/<str:inorout>/api/', views.signinapi, name='signinapi'),
    path('<int:eventid>/<str:inorout>/success/', views.success, name='success'),
    path('<int:eventid>/eventattendance/', views.eventattendance, name='eventattendance'),
    path('userattendance/', views.userattendance, name='userattendance'),
    path('brothercredits/', views.brothercredits, name='brothercredits'),
    path('brothercredits/csv', views.creditscsv, name='creditscsv'),
    path('brothercredits/meetingscsv', views.meetingscsv, name='meetingscsv'),
]