from django.urls import path
from . import views

urlpatterns = [
    path('', views.main_site, name = 'main_site'),
    path('city/', views.city_site, name = 'city_site'),
]
