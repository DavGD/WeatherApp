from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
    path('', views.main_site, name = 'main_site'),
    path('city/', views.city_site, name = 'city_site'),
    url(r'^city/(\d+)/$', views.city_site, name = 'city_site'),
]
