from django.db import models


class VacGeoStats(models.Model):
    """Моделька страницы география"""
    graph_sal_by_city = models.ImageField(
        blank=False,
        verbose_name='График зарплат по городам для Java-разработчиков'
    )
    data_table_java_sal_by_city = models.TextField(
        blank=False,
        verbose_name='Таблица зарплат по городам для Java-разработчиков'
    )

    graph_java_vac_share_by_city = models.ImageField(
        blank=False,
        verbose_name='График долей вакансий по городам для Java-разработчиков'
    )
    data_table_java_vac_share_by_city = models.TextField(
        blank=False,
        verbose_name='Таблица долей вакансий по городам для Java-разработчиков'
    )

    class Meta:
        verbose_name = 'Статистика по городам'
        verbose_name_plural = 'Статистики по городам'
