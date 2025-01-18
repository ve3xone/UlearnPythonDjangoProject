from django.shortcuts import render
from .models import VacGeoStats


def geography(request):
    """Рендер страницы география"""
    vac_geo_stats = VacGeoStats.objects.first()

    content = {
        'salary_graph_by_city': vac_geo_stats.salary_graph_by_city.url,
        'salary_table_by_city': vac_geo_stats.salary_table_by_city,
        'vac_share_graph_by_city': vac_geo_stats.vac_share_graph_by_city.url,
        'vac_share_table_by_city': vac_geo_stats.vac_share_table_by_city,
    }

    return render(request, 'geography_page.html', content)