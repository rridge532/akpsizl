from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'attendance'
urlpatterns = [
    # path('', views.portal, name='portal'),
    path('<int:eventid>/qrcode', views.qrcodeimage, name='qrcodeimage'),
    path('<int:eventid>/signinqr', views.signinqr, name='signinqr'),
    path('<int:eventid>/<str:eventslug>/signin/', views.signinapi, name='signinapi'),
    path('<int:eventid>/signinsuccess/', views.signinsuccess, name='signinsuccess'),
    path('<int:eventid>/eventattendance/', views.eventattendance, name='eventattendance'),
    path('userattendance/', views.userattendance, name='userattendance'),
    path('brothercredits/', views.brothercredits, name='brothercredits'),
]