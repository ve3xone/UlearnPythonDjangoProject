from django.urls import path
from . import views


urlpatterns = [
    path('', views.relevance_page, name='relevance'),
]
