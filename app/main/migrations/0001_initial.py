# Generated by Django 4.2.16 on 2024-09-16 16:55

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('role', models.CharField(choices=[('teacher', 'Учитель'), ('admin', 'Управляющий')], default='teacher', max_length=10, verbose_name='Роль: ')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to.', related_name='custom_user_set', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='custom_user_permissions_set', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'Пользователь',
                'verbose_name_plural': 'Пользователи',
                'permissions': (('can_view_reports', 'Can view reports'),),
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Indicator',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Название индикатора: ')),
                ('unit', models.CharField(max_length=50, verbose_name='Единица измерения:')),
            ],
            options={
                'verbose_name': 'Индикатор',
                'verbose_name_plural': 'Индикаторы',
            },
        ),
        migrations.CreateModel(
            name='TeacherReport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('plan_2022_2023', models.IntegerField(default=0, verbose_name='План 2022-2023')),
                ('actual_2023_2024', models.IntegerField(default=0, verbose_name='Выполнено за 2023-2024')),
                ('plan_2024_2025', models.IntegerField(default=0, verbose_name='План 2024-2025')),
                ('comment', models.TextField(blank=True, null=True, verbose_name='Комментарий')),
                ('indicator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.indicator')),
                ('teacher', models.ForeignKey(limit_choices_to={'role': 'teacher'}, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Отчёт учителя',
                'verbose_name_plural': 'Отчёты учителей',
            },
        ),
        migrations.CreateModel(
            name='AdminReport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_plan_2022_2023', models.IntegerField(default=0, verbose_name='Суммарный план 2022-2023: ')),
                ('total_actual_2023_2024', models.IntegerField(default=0, verbose_name='Суммарные выполненные показатели 2023-2024')),
                ('total_plan_2024_2025', models.IntegerField(default=0, verbose_name='Суммарный план на 2024-2025')),
                ('indicator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.indicator')),
            ],
            options={
                'verbose_name': 'Агрегированные данные',
                'verbose_name_plural': 'Агрегированные данные',
            },
        ),
    ]
