from django.shortcuts import render
from django.http import JsonResponse
from .utils import get_vacancies


async def fetch_vacancies(request):
    """Ответ API"""
    profession = request.GET.get('profession', 'Java')
    vacancies = await get_vacancies(profession)
    return JsonResponse({'vacancies': vacancies})


async def render_vacancies(request):
    """Рендер страницы последних вакансий"""
    vacancies = await get_vacancies('java-программист')
    return render(request, 'lastest_vacs_page.html', {'vacancies': vacancies})
