from django.db import models
from django.conf import settings


class General(models.Model):
    """Моделька главной страницы"""
    vac_pic = models.ImageField(
        blank=True,
        null=True,
        default='/General_JvmSpec7.png',
        verbose_name='Картинка вакансии'
    )
    vac_text = models.TextField(
        blank=True,
        null=True,
        default=settings.DEFAULT_VAC_TEXT,
        verbose_name='Текст вакансии (HTML)'
    )


    class Meta:
        verbose_name = 'Главная'
        verbose_name_plural = verbose_name
