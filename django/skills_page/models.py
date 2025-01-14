from django.db import models


class SkillsStatistics(models.Model):
    top20_skills_java_2015_graph = models.ImageField(
        blank=False, 
        verbose_name='График навыков за 2015 год для Java-программиста'
    )
    top20_skills_java_2015_data = models.TextField(
        blank=False, 
        verbose_name='Таблица навыков за 2015 год для Java-программиста'
    )

    top20_skills_java_2016_graph = models.ImageField(
        blank=False, 
        verbose_name='График навыков за 2016 год для Java-программиста'
    )
    top20_skills_java_2016_data = models.TextField(
        blank=False, 
        verbose_name='Таблица навыков за 2016 год для Java-программиста'
    )

    top20_skills_java_2017_graph = models.ImageField(
        blank=False, 
        verbose_name='График навыков за 2017 год для Java-программиста'
    )
    top20_skills_java_2017_data = models.TextField(
        blank=False, 
        verbose_name='Таблица навыков за 2017 год для Java-программиста'
    )

    top20_skills_java_2018_graph = models.ImageField(
        blank=False, 
        verbose_name='График навыков за 2018 год для Java-программиста'
    )
    top20_skills_java_2018_data = models.TextField(
        blank=False, 
        verbose_name='Таблица навыков за 2018 год для Java-программиста'
    )

    top20_skills_java_2019_graph = models.ImageField(
        blank=False, 
        verbose_name='График навыков за 2019 год для Java-программиста'
    )
    top20_skills_java_2019_data = models.TextField(
        blank=False, 
        verbose_name='Таблица навыков за 2019 год для Java-программиста'
    )

    top20_skills_java_2020_graph = models.ImageField(
        blank=False, 
        verbose_name='График навыков за 2020 год для Java-программиста'
    )
    top20_skills_java_2020_data = models.TextField(
        blank=False, 
        verbose_name='Таблица навыков за 2020 год для Java-программиста'
    )

    top20_skills_java_2021_graph = models.ImageField(
        blank=False, 
        verbose_name='График навыков за 2021 год для Java-программиста'
    )
    top20_skills_java_2021_data = models.TextField(
        blank=False, 
        verbose_name='Таблица навыков за 2021 год для Java-программиста'
    )

    top20_skills_java_2022_graph = models.ImageField(
        blank=False, 
        verbose_name='График навыков за 2022 год для Java-программиста'
    )
    top20_skills_java_2022_data = models.TextField(
        blank=False, 
        verbose_name='Таблица навыков за 2022 год для Java-программиста'
    )

    top20_skills_java_2023_graph = models.ImageField(
        blank=False, 
        verbose_name='График навыков за 2023 год для Java-программиста'
    )
    top20_skills_java_2023_data = models.TextField(
        blank=False, 
        verbose_name='Таблица навыков за 2023 год для Java-программиста'
    )

    top20_skills_java_2024_graph = models.ImageField(
        blank=False, 
        verbose_name='График навыков за 2024 год для Java-программиста'
    )
    top20_skills_java_2024_data = models.TextField(
        blank=False, 
        verbose_name='Таблица навыков за 2024 год для Java-программиста'
    )
    
    class Meta:
        verbose_name = 'Навыки'
        verbose_name_plural = verbose_name