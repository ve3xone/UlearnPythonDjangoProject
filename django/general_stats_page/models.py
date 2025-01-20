from django.db import models


class Statistics(models.Model):
    """Моделька общей статистики"""
    graph_sal_yearly = models.ImageField(blank=False, verbose_name='График зарплат по годам')
    data_table_sal_yearly = models.TextField(blank=False, verbose_name='Таблица зарплат по годам')

    graph_of_vacs_years = models.ImageField(blank=False, verbose_name='График количества вакансий по годам')
    data_table_vacs_by_year = models.TextField(blank=False, verbose_name='Таблица количества вакансий по годам')

    graph_sal_by_city = models.ImageField(blank=False, verbose_name='График зарплат по городам')
    data_table_sal_by_city = models.TextField(blank=False, verbose_name='Таблица зарплат по городам')

    graph_vac_share_cities = models.ImageField(blank=False, verbose_name='График долей вакансий по городам')
    data_table_vac_share_by_city = models.TextField(blank=False, verbose_name='Таблица доли вакансий по городам')

    graph_top_sks_2015 = models.ImageField(blank=False, verbose_name='График ТОП-20 навыков за 2015 год')
    data_table_top_sks_2015 = models.TextField(blank=False, verbose_name='Таблица ТОП-20 навыков за 2015 год')

    graph_top_sks_2016 = models.ImageField(blank=False, verbose_name='График ТОП-20 навыков за 2016 год')
    data_table_top_sks_2016 = models.TextField(blank=False, verbose_name='Таблица ТОП-20 навыков за 2016 год')

    graph_top_sks_2017 = models.ImageField(blank=False, verbose_name='График ТОП-20 навыков за 2017 год')
    data_table_top_sks_2017 = models.TextField(blank=False, verbose_name='Таблица ТОП-20 навыков за 2017 год')

    graph_top_sks_2018 = models.ImageField(blank=False, verbose_name='График ТОП-20 навыков за 2018 год')
    data_table_top_sks_2018 = models.TextField(blank=False, verbose_name='Таблица ТОП-20 навыков за 2018 год')

    graph_top_sks_2019 = models.ImageField(blank=False, verbose_name='График ТОП-20 навыков за 2019 год')
    data_table_top_sks_2019 = models.TextField(blank=False, verbose_name='Таблица ТОП-20 навыков за 2019 год')

    graph_top_sks_2020 = models.ImageField(blank=False, verbose_name='График ТОП-20 навыков за 2020 год')
    data_table_top_sks_2020 = models.TextField(blank=False, verbose_name='Таблица ТОП-20 навыков за 2020 год')

    graph_top_sks_2021 = models.ImageField(blank=False, verbose_name='График ТОП-20 навыков за 2021 год')
    data_table_top_sks_2021 = models.TextField(blank=False, verbose_name='Таблица ТОП-20 навыков за 2021 год')

    graph_top_sks_2022 = models.ImageField(blank=False, verbose_name='График ТОП-20 навыков за 2022 год')
    data_table_top_sks_2022 = models.TextField(blank=False, verbose_name='Таблица ТОП-20 навыков за 2022 год')

    graph_top_sks_2023 = models.ImageField(blank=False, verbose_name='График ТОП-20 навыков за 2023 год')
    data_table_top_sks_2023 = models.TextField(blank=False, verbose_name='Таблица ТОП-20 навыков за 2023 год')

    graph_top_sks_2024 = models.ImageField(blank=False, verbose_name='График ТОП-20 навыков за 2024 год')
    data_table_top_sks_2024 = models.TextField(blank=False, verbose_name='Таблица ТОП-20 навыков за 2024 год')


    class Meta:
        verbose_name = 'Статистика'
        verbose_name_plural = 'Статистики'
