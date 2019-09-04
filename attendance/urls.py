from django.urls import path
from . import views

app_name = 'attendance'
urlpatterns = [
    path('events/', views.events, name='events'),
    path('<int:eventid>/qrcode', views.qrcodeimage, name='qrcodeimage'),
    path('<int:eventid>/signinqr', views.signinqr, name='signinqr'),
    path('<int:eventid>/<str:eventslug>/signin/', views.signinapi, name='signinapi'),
    path('<int:eventid>/signinsuccess/', views.signinsuccess, name='signinsuccess'),
    path('<int:eventid>/eventattendance/', views.eventattendance, name='eventattendance'),
    path('userattendance/', views.userattendance, name='userattendance'),
    path('brothercredits/', views.brothercredits, name='brothercredits'),
    path('brothercredits/csv', views.creditscsv, name='creditscsv'),
]