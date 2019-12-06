from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="summoner-home"),
    path('about/', views.about, name="summoner-about"),
]