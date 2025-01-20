from django.db import models


class VacStatistics(models.Model):
    """Моделька страницы востребованность"""
    graph_java_vac_sal_yearly = models.ImageField(
        blank=False,
        verbose_name='График зарплат по годам Java-программист'
    )
    data_table_java_vac_sal_yearly = models.TextField(
        blank=False,
        verbose_name='Таблица зарплат по годам Java-программист'
    )

    graph_of_java_vacs_years = models.ImageField(
        blank=False,
        verbose_name='График количества вакансий по годам Java-программист'
    )
    data_table_java_vacs_by_year = models.TextField(
        blank=False,
        verbose_name='Таблица количества вакансий по годам Java-программист'
    )

    class Meta:
        verbose_name = 'Востребованность'
        verbose_name_plural = 'Востребованности'
