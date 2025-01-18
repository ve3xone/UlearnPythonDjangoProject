from django.db import models


class VacStatistics(models.Model):
    """Моделька страницы востребованность"""
    annual_salary_chart = models.ImageField(
        blank=False, 
        verbose_name='График зарплат по годам Java-программист'
    )
    annual_salary_data = models.TextField(
        blank=False, 
        verbose_name='Таблица зарплат по годам Java-программист'
    )

    annual_vacancy_chart = models.ImageField(
        blank=False, 
        verbose_name='График количества вакансий по годам Java-программист'
    )
    annual_vacancy_data = models.TextField(
        blank=False, 
        verbose_name='Таблица количества вакансий по годам Java-программист'
    )

    class Meta:
        verbose_name = 'Востребованность'
        verbose_name_plural = 'Востребованности'
    