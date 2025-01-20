from django.db import models


class SkillsStatistics(models.Model):
    """"Модель страницы навыки"""
    graph_top20_sks_java_2015 = models.ImageField(
        blank=False,
        verbose_name='График навыков за 2015 год для Java-программиста'
    )
    data_table_top20_sks_java_2015 = models.TextField(
        blank=False,
        verbose_name='Таблица навыков за 2015 год для Java-программиста'
    )

    graph_top20_sks_java_2016 = models.ImageField(
        blank=False,
        verbose_name='График навыков за 2016 год для Java-программиста'
    )
    data_table_top20_sks_java_2016 = models.TextField(
        blank=False,
        verbose_name='Таблица навыков за 2016 год для Java-программиста'
    )

    graph_top20_sks_java_2017 = models.ImageField(
        blank=False,
        verbose_name='График навыков за 2017 год для Java-программиста'
    )
    data_table_top20_sks_java_2017 = models.TextField(
        blank=False,
        verbose_name='Таблица навыков за 2017 год для Java-программиста'
    )

    graph_top20_sks_java_2018 = models.ImageField(
        blank=False,
        verbose_name='График навыков за 2018 год для Java-программиста'
    )
    data_table_top20_sks_java_2018 = models.TextField(
        blank=False,
        verbose_name='Таблица навыков за 2018 год для Java-программиста'
    )

    graph_top20_sks_java_2019 = models.ImageField(
        blank=False,
        verbose_name='График навыков за 2019 год для Java-программиста'
    )
    data_table_top20_sks_java_2019 = models.TextField(
        blank=False,
        verbose_name='Таблица навыков за 2019 год для Java-программиста'
    )

    graph_top20_sks_java_2020 = models.ImageField(
        blank=False,
        verbose_name='График навыков за 2020 год для Java-программиста'
    )
    data_table_top20_sks_java_2020 = models.TextField(
        blank=False,
        verbose_name='Таблица навыков за 2020 год для Java-программиста'
    )

    graph_top20_sks_java_2021 = models.ImageField(
        blank=False,
        verbose_name='График навыков за 2021 год для Java-программиста'
    )
    data_table_top20_sks_java_2021 = models.TextField(
        blank=False,
        verbose_name='Таблица навыков за 2021 год для Java-программиста'
    )

    graph_top20_sks_java_2022 = models.ImageField(
        blank=False,
        verbose_name='График навыков за 2022 год для Java-программиста'
    )
    data_table_top20_sks_java_2022 = models.TextField(
        blank=False,
        verbose_name='Таблица навыков за 2022 год для Java-программиста'
    )

    graph_top20_sks_java_2023 = models.ImageField(
        blank=False,
        verbose_name='График навыков за 2023 год для Java-программиста'
    )
    data_table_top20_sks_java_2023 = models.TextField(
        blank=False,
        verbose_name='Таблица навыков за 2023 год для Java-программиста'
    )

    graph_top20_sks_java_2024 = models.ImageField(
        blank=False,
        verbose_name='График навыков за 2024 год для Java-программиста'
    )
    data_table_top20_sks_java_2024 = models.TextField(
        blank=False,
        verbose_name='Таблица навыков за 2024 год для Java-программиста'
    )


    class Meta:
        verbose_name = 'Навыки'
        verbose_name_plural = verbose_name
