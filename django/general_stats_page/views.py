from django.shortcuts import render
from .models import Statistics


def general_stats(request):
    """Рендер общей статистики"""
    stats = Statistics.objects.first()

    content = {
        'annual_salary_chart': stats.annual_salary_chart.url,
        'annual_salary_data': stats.annual_salary_data,
        'annual_vacancy_chart': stats.annual_vacancy_chart.url,
        'annual_vacancy_data': stats.annual_vacancy_data,
        'city_salary_chart': stats.city_salary_chart.url,
        'city_salary_data': stats.city_salary_data,
        'city_vacancy_share_chart': stats.city_vacancy_share_chart.url,
        'city_vacancy_share_data': stats.city_vacancy_share_data,

        'top_skills_2015_chart': stats.top_skills_2015_chart.url,
        'top_skills_2015_data': stats.top_skills_2015_data,

        'top_skills_2016_chart': stats.top_skills_2016_chart.url,
        'top_skills_2016_data': stats.top_skills_2016_data,

        'top_skills_2017_chart': stats.top_skills_2017_chart.url,
        'top_skills_2017_data': stats.top_skills_2017_data,

        'top_skills_2018_chart': stats.top_skills_2018_chart.url,
        'top_skills_2018_data': stats.top_skills_2018_data,

        'top_skills_2019_chart': stats.top_skills_2019_chart.url,
        'top_skills_2019_data': stats.top_skills_2019_data,

        'top_skills_2020_chart': stats.top_skills_2020_chart.url,
        'top_skills_2020_data': stats.top_skills_2020_data,

        'top_skills_2021_chart': stats.top_skills_2021_chart.url,
        'top_skills_2021_data': stats.top_skills_2021_data,

        'top_skills_2022_chart': stats.top_skills_2022_chart.url,
        'top_skills_2022_data': stats.top_skills_2022_data,

        'top_skills_2023_chart': stats.top_skills_2023_chart.url,
        'top_skills_2023_data': stats.top_skills_2023_data,

        'top_skills_2024_chart': stats.top_skills_2024_chart.url,
        'top_skills_2024_data': stats.top_skills_2024_data
    }

    return render(request, 'general_stats.html', content)
