from django.shortcuts import render
from .models import SkillsStatistics


def skills_page(request):
    """Рендер страницы навыки"""
    skills_vac_stats = SkillsStatistics.objects.first()

    content = {
        'graph_top20_sks_java_2015_url': skills_vac_stats.graph_top20_sks_java_2015.url,
        'data_table_top20_sks_java_2015': skills_vac_stats.data_table_top20_sks_java_2015,

        'graph_top20_sks_java_2016_url': skills_vac_stats.graph_top20_sks_java_2016.url,
        'data_table_top20_sks_java_2016': skills_vac_stats.data_table_top20_sks_java_2016,

        'graph_top20_sks_java_2017_url': skills_vac_stats.graph_top20_sks_java_2017.url,
        'data_table_top20_sks_java_2017': skills_vac_stats.data_table_top20_sks_java_2017,

        'graph_top20_sks_java_2018_url': skills_vac_stats.graph_top20_sks_java_2018.url,
        'data_table_top20_sks_java_2018': skills_vac_stats.data_table_top20_sks_java_2018,

        'graph_top20_sks_java_2019_url': skills_vac_stats.graph_top20_sks_java_2019.url,
        'data_table_top20_sks_java_2019': skills_vac_stats.data_table_top20_sks_java_2019,

        'graph_top20_sks_java_2020_url': skills_vac_stats.graph_top20_sks_java_2020.url,
        'data_table_top20_sks_java_2020': skills_vac_stats.data_table_top20_sks_java_2020,

        'graph_top20_sks_java_2021_url': skills_vac_stats.graph_top20_sks_java_2021.url,
        'data_table_top20_sks_java_2021': skills_vac_stats.data_table_top20_sks_java_2021,

        'graph_top20_sks_java_2022_url': skills_vac_stats.graph_top20_sks_java_2022.url,
        'data_table_top20_sks_java_2022': skills_vac_stats.data_table_top20_sks_java_2022,

        'graph_top20_sks_java_2023_url': skills_vac_stats.graph_top20_sks_java_2023.url,
        'data_table_top20_sks_java_2023': skills_vac_stats.data_table_top20_sks_java_2023,

        'graph_top20_sks_java_2024_url': skills_vac_stats.graph_top20_sks_java_2024.url,
        'data_table_top20_sks_java_2024': skills_vac_stats.data_table_top20_sks_java_2024,
    }

    return render(request, 'skills_page.html', content)
