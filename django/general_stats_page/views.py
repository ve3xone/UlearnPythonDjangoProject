from django.shortcuts import render
from .models import Statistics


def general_stats(request):
    """Рендер общей статистики"""
    stats = Statistics.objects.first()

    content = {
        'graph_sal_yearly_url': stats.graph_sal_yearly.url,
        'data_table_sal_yearly': stats.data_table_sal_yearly,

        'graph_of_vacs_years_url': stats.graph_of_vacs_years.url,
        'data_table_vacs_by_year': stats.data_table_vacs_by_year,

        'graph_sal_by_city_url': stats.graph_sal_by_city.url,
        'data_table_sal_by_city': stats.data_table_sal_by_city,

        'graph_vac_share_cities_url': stats.graph_vac_share_cities.url,
        'data_table_vac_share_by_city': stats.data_table_vac_share_by_city,

        'graph_top_sks_2015_url': stats.graph_top_sks_2015.url,
        'data_table_top_sks_2015': stats.data_table_top_sks_2015,

        'graph_top_sks_2016_url': stats.graph_top_sks_2016.url,
        'data_table_top_sks_2016': stats.data_table_top_sks_2016,

        'graph_top_sks_2017_url': stats.graph_top_sks_2017.url,
        'data_table_top_sks_2017': stats.data_table_top_sks_2017,

        'graph_top_sks_2018_url': stats.graph_top_sks_2018.url,
        'data_table_top_sks_2018': stats.data_table_top_sks_2018,

        'graph_top_sks_2019_url': stats.graph_top_sks_2019.url,
        'data_table_top_sks_2019': stats.data_table_top_sks_2019,

        'graph_top_sks_2020_url': stats.graph_top_sks_2020.url,
        'data_table_top_sks_2020': stats.data_table_top_sks_2020,

        'graph_top_sks_2021_url': stats.graph_top_sks_2021.url,
        'data_table_top_sks_2021': stats.data_table_top_sks_2021,

        'graph_top_sks_2022_url': stats.graph_top_sks_2022.url,
        'data_table_top_sks_2022': stats.data_table_top_sks_2022,

        'graph_top_sks_2023_url': stats.graph_top_sks_2023.url,
        'data_table_top_sks_2023': stats.data_table_top_sks_2023,

        'graph_top_sks_2024_url': stats.graph_top_sks_2024.url,
        'data_table_top_sks_2024': stats.data_table_top_sks_2024
    }

    return render(request, 'general_stats.html', content)
