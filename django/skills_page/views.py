from django.shortcuts import render

from .models import SkillsStatistics

def skills_page(request):
    skills_vac_stats = SkillsStatistics.objects.first()

    content = {
        'top20_skills_java_2015_graph': skills_vac_stats.top20_skills_java_2015_graph.url,
        'top20_skills_java_2015_data': skills_vac_stats.top20_skills_java_2015_data,
        'top20_skills_java_2016_graph': skills_vac_stats.top20_skills_java_2016_graph.url,
        'top20_skills_java_2016_data': skills_vac_stats.top20_skills_java_2016_data,
        'top20_skills_java_2017_graph': skills_vac_stats.top20_skills_java_2017_graph.url,
        'top20_skills_java_2017_data': skills_vac_stats.top20_skills_java_2017_data,
        'top20_skills_java_2018_graph': skills_vac_stats.top20_skills_java_2018_graph.url,
        'top20_skills_java_2018_data': skills_vac_stats.top20_skills_java_2018_data,
        'top20_skills_java_2019_graph': skills_vac_stats.top20_skills_java_2019_graph.url,
        'top20_skills_java_2019_data': skills_vac_stats.top20_skills_java_2019_data,
        'top20_skills_java_2020_graph': skills_vac_stats.top20_skills_java_2020_graph.url,
        'top20_skills_java_2020_data': skills_vac_stats.top20_skills_java_2020_data,
        'top20_skills_java_2021_graph': skills_vac_stats.top20_skills_java_2021_graph.url,
        'top20_skills_java_2021_data': skills_vac_stats.top20_skills_java_2021_data,
        'top20_skills_java_2022_graph': skills_vac_stats.top20_skills_java_2022_graph.url,
        'top20_skills_java_2022_data': skills_vac_stats.top20_skills_java_2022_data,
        'top20_skills_java_2023_graph': skills_vac_stats.top20_skills_java_2023_graph.url,
        'top20_skills_java_2023_data': skills_vac_stats.top20_skills_java_2023_data,
        'top20_skills_java_2024_graph': skills_vac_stats.top20_skills_java_2024_graph.url,
        'top20_skills_java_2024_data': skills_vac_stats.top20_skills_java_2024_data,
    }

    return render(request, 'skills_page.html', content)