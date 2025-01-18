from django.db import models


class Statistics(models.Model):
    """Моделька общей статистики"""
    annual_salary_chart = models.ImageField(blank=False, verbose_name='График зарплат по годам')
    annual_salary_data = models.TextField(blank=False, verbose_name='Таблица зарплат по годам')

    annual_vacancy_chart = models.ImageField(blank=False, verbose_name='График количества вакансий по годам')
    annual_vacancy_data = models.TextField(blank=False, verbose_name='Таблица количества вакансий по годам')

    city_salary_chart = models.ImageField(blank=False, verbose_name='График зарплат по городам')
    city_salary_data = models.TextField(blank=False, verbose_name='Таблица зарплат по городам')

    city_vacancy_share_chart = models.ImageField(blank=False, verbose_name='График долей вакансий по городам')
    city_vacancy_share_data = models.TextField(blank=False, verbose_name='Таблица доли вакансий по городам')

    top_skills_2015_chart = models.ImageField(blank=False, verbose_name='График ТОП-20 навыков за 2015 год')
    top_skills_2015_data = models.TextField(blank=False, verbose_name='Таблица ТОП-20 навыков за 2015 год')

    top_skills_2016_chart = models.ImageField(blank=False, verbose_name='График ТОП-20 навыков за 2016 год')
    top_skills_2016_data = models.TextField(blank=False, verbose_name='Таблица ТОП-20 навыков за 2016 год')

    top_skills_2017_chart = models.ImageField(blank=False, verbose_name='График ТОП-20 навыков за 2017 год')
    top_skills_2017_data = models.TextField(blank=False, verbose_name='Таблица ТОП-20 навыков за 2017 год')

    top_skills_2018_chart = models.ImageField(blank=False, verbose_name='График ТОП-20 навыков за 2018 год')
    top_skills_2018_data = models.TextField(blank=False, verbose_name='Таблица ТОП-20 навыков за 2018 год')

    top_skills_2019_chart = models.ImageField(blank=False, verbose_name='График ТОП-20 навыков за 2019 год')
    top_skills_2019_data = models.TextField(blank=False, verbose_name='Таблица ТОП-20 навыков за 2019 год')
    
    top_skills_2020_chart = models.ImageField(blank=False, verbose_name='График ТОП-20 навыков за 2020 год')
    top_skills_2020_data = models.TextField(blank=False, verbose_name='Таблица ТОП-20 навыков за 2020 год')

    top_skills_2021_chart = models.ImageField(blank=False, verbose_name='График ТОП-20 навыков за 2021 год')
    top_skills_2021_data = models.TextField(blank=False, verbose_name='Таблица ТОП-20 навыков за 2021 год')

    top_skills_2022_chart = models.ImageField(blank=False, verbose_name='График ТОП-20 навыков за 2022 год')
    top_skills_2022_data = models.TextField(blank=False, verbose_name='Таблица ТОП-20 навыков за 2022 год')

    top_skills_2023_chart = models.ImageField(blank=False, verbose_name='График ТОП-20 навыков за 2023 год')
    top_skills_2023_data = models.TextField(blank=False, verbose_name='Таблица ТОП-20 навыков за 2023 год')

    top_skills_2024_chart = models.ImageField(blank=False, verbose_name='График ТОП-20 навыков за 2024 год')
    top_skills_2024_data = models.TextField(blank=False, verbose_name='Таблица ТОП-20 навыков за 2024 год')


    class Meta:
        verbose_name = 'Статистика'
        verbose_name_plural = 'Статистики'
