# Generated by Django 4.2.16 on 2024-09-23 08:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_mainindicator_indicator_main_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mainindicator',
            name='name',
            field=models.CharField(max_length=255, unique=True, verbose_name='Главный индикатор: '),
        ),
    ]
