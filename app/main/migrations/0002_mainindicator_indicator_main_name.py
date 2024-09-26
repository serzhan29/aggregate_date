# Generated by Django 4.2.16 on 2024-09-23 08:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MainIndicator',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True, verbose_name='')),
                ('amount_2022_2023', models.IntegerField(default=0, verbose_name='Суммарный план 2022-2023: ')),
                ('amount_2023_2024', models.IntegerField(default=0, verbose_name='Суммарные выполненные показатели 2023-2024')),
                ('amount_2024_2025', models.IntegerField(default=0, verbose_name='Суммарный план на 2024-2025')),
            ],
            options={
                'verbose_name': 'Главный индикатор',
                'verbose_name_plural': 'Главные индикаторы',
            },
        ),
        migrations.AddField(
            model_name='indicator',
            name='main_name',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='main.mainindicator'),
        ),
    ]