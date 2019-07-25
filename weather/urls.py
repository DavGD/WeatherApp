from django.urls import path
from . import views

urlpatterns = [
    path('', views.main_site, name = 'main_site'),
]
