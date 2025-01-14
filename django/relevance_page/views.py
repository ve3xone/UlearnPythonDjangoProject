from django.shortcuts import render

from .models import VacStatistics

def relevance_page(request):
    vacstats = VacStatistics.objects.first()

    content = {
        'annual_salary_chart': vacstats.annual_salary_chart.url,
        'annual_salary_data': vacstats.annual_salary_data,
        'annual_vacancy_chart': vacstats.annual_vacancy_chart.url,
        'annual_vacancy_data': vacstats.annual_vacancy_data,
    }

    return render(request, 'relevance_page.html', content)
