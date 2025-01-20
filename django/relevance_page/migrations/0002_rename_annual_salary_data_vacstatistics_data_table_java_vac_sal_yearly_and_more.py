# Generated by Django 5.1.4 on 2025-01-20 07:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('relevance_page', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='vacstatistics',
            old_name='annual_salary_data',
            new_name='data_table_java_vac_sal_yearly',
        ),
        migrations.RenameField(
            model_name='vacstatistics',
            old_name='annual_vacancy_data',
            new_name='data_table_java_vacs_by_year',
        ),
        migrations.RenameField(
            model_name='vacstatistics',
            old_name='annual_salary_chart',
            new_name='graph_java_vac_sal_yearly',
        ),
        migrations.RenameField(
            model_name='vacstatistics',
            old_name='annual_vacancy_chart',
            new_name='graph_of_java_vacs_years',
        ),
    ]
