from django.shortcuts import render
from .models import VacGeoStats


def geography(request):
    """Рендер страницы география"""
    vac_geo_stats = VacGeoStats.objects.first()

    content = {
        'graph_sal_by_city_url': vac_geo_stats.graph_sal_by_city.url,
        'data_table_java_sal_by_city': vac_geo_stats.data_table_java_sal_by_city,

        'graph_java_vac_share_by_city_url': vac_geo_stats.graph_java_vac_share_by_city.url,
        'data_table_java_vac_share_by_city': vac_geo_stats.data_table_java_vac_share_by_city,
    }

    return render(request, 'geography_page.html', content)
