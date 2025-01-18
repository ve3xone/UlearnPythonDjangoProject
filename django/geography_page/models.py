from django.db import models


class VacGeoStats(models.Model):
    """Моделька страницы география"""
    salary_graph_by_city = models.ImageField(
        blank=False,
        verbose_name='График зарплат по городам для Java-разработчиков'
    )
    salary_table_by_city = models.TextField(
        blank=False,
        verbose_name='Таблица зарплат по городам для Java-разработчиков'
    )

    vac_share_graph_by_city = models.ImageField(
        blank=False,
        verbose_name='График долей вакансий по городам для Java-разработчиков'
    )
    vac_share_table_by_city = models.TextField(
        blank=False,
        verbose_name='Таблица долей вакансий по городам для Java-разработчиков'
    )

    class Meta:
        verbose_name = 'Статистика по городам'
        verbose_name_plural = 'Статистики по городам'
