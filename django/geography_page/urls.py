from django.urls import path
from . import views


urlpatterns = [
    path('', views.geography, name='geography'),
]
