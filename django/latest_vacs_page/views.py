import asyncio
from django.shortcuts import render
from django.http import JsonResponse
from .utils import get_vacancies  # Вынесите вашу логику в utils.py

async def fetch_vacancies(request):
    profession = request.GET.get('profession', 'IT')
    vacancies = await get_vacancies(profession)
    return JsonResponse({'vacancies': vacancies})

async def render_vacancies(request):
    vacancies = await get_vacancies('java-программист')
    return render(request, 'lastest_vacs_page.html', {'vacancies': vacancies})