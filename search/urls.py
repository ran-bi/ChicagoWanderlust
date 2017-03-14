# Code substantially modified, made reading the documentation at 
# https://docs.djangoproject.com/en/1.10/intro/
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.home, name = 'home'),
]