from django.urls import path
from . import views

urlpatterns = [
    path('', views.general_page, name='general_page'),
]
