# Generated by Django 4.2.15 on 2024-09-23 14:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_alter_mainindicator_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='teacherreport',
            name='main_indicator',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='main.mainindicator'),
        ),
    ]
