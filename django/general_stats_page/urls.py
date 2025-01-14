from django.urls import path
from . import views


urlpatterns = [
    path('', views.general_stats, name='general_stats'),
]
