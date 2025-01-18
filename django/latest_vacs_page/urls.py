from django.urls import path
from .views import *


urlpatterns = [
    path('/api', fetch_vacancies, name='fetch_vacancies'),
    path('', render_vacancies, name='render_vacancies'),
]
