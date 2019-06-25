from django.urls import path
from . import views

app_name = 'rush'
urlpatterns = [
    path('changenight/', views.changenight, name='changenight'),
    path('interview/', views.interview, name='interview'),
]