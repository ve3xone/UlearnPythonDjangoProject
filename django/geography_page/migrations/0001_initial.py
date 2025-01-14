# Generated by Django 5.1.4 on 2025-01-14 07:13

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='VacGeoStats',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('salary_graph_by_city', models.ImageField(upload_to='', verbose_name='График зарплат по городам для Java-разработчиков')),
                ('salary_table_by_city', models.TextField(verbose_name='Таблица зарплат по городам для Java-разработчиков')),
                ('vac_share_graph_by_city', models.ImageField(upload_to='', verbose_name='График долей вакансий по городам для Java-разработчиков')),
                ('vac_share_table_by_city', models.TextField(verbose_name='Таблица долей вакансий по городам для Java-разработчиков')),
            ],
            options={
                'verbose_name': 'Статистика по городам',
                'verbose_name_plural': 'Статистики по городам',
            },
        ),
    ]
