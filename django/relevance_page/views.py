from django.shortcuts import render
from .models import VacStatistics


def relevance_page(request):
    """Рендер страницы востребованность"""
    vacstats = VacStatistics.objects.first()

    content = {
        'graph_java_vac_sal_yearly_url': vacstats.graph_java_vac_sal_yearly.url,
        'data_table_java_vac_sal_yearly': vacstats.data_table_java_vac_sal_yearly,

        'graph_of_java_vacs_years_url': vacstats.graph_of_java_vacs_years.url,
        'data_table_java_vacs_by_year': vacstats.data_table_java_vacs_by_year,
    }

    return render(request, 'relevance_page.html', content)
