from django.db.models import Sum
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models


class User(AbstractUser):
    # Поле для роли пользователя (учитель или администратор)
    ROLE_CHOICES = [
        ('teacher', 'Учитель'),
        ('admin', 'Управляющий'),
    ]
    role = models.CharField('Роль: ', max_length=10, choices=ROLE_CHOICES, default='teacher')

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        # Избегаем конфликта имен
        permissions = (
            ('can_view_reports', 'Can view reports'),
        )

    # Переопределяем related_name для групп и разрешений
    groups = models.ManyToManyField(
        Group,
        related_name='custom_user_set',
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups'
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='custom_user_permissions_set',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions'
    )



# Модель для индикативных показателей
class Indicator(models.Model):
    name = models.CharField('Название индикатора: ', max_length=255)  # (например, публикации в Scopus)
    unit = models.CharField('Единица измерения:', max_length=50)  # (счет, проценты и т.д.)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Индикатор'
        verbose_name_plural = 'Индикаторы'


# Модель для хранения отчетов учителей
class TeacherReport(models.Model):
    teacher = models.ForeignKey(User, on_delete=models.CASCADE,
                                limit_choices_to={'role': 'teacher'})  # Связь с учителем
    indicator = models.ForeignKey(Indicator, on_delete=models.CASCADE)  # Связь с индикатором
    plan_2022_2023 = models.IntegerField('План 2022-2023', default=0)  # План 2022-2023
    actual_2023_2024 = models.IntegerField('Выполнено за 2023-2024', default=0)  # Выполнено за 2023-2024
    plan_2024_2025 = models.IntegerField('План 2024-2025', default=0)  # План 2024-2025
    comment = models.TextField('Комментарий', blank=True, null=True)  # Комментарий

    def __str__(self):
        return f"Отчёт: {self.teacher.username} - {self.indicator.name}"

    @property
    def next_year_plan(self):
        # Рассчитываем план на 2024-2025 (+20% к фактическому показателю 2023-2024)
        return int(self.actual_2023_2024 * 1.2)

    class Meta:
        verbose_name = 'Отчёт учителя'
        verbose_name_plural = 'Отчёты учителей'


# Агрегация данных для администратора
class AdminReport(models.Model):
    indicator = models.ForeignKey(Indicator, on_delete=models.CASCADE)
    total_plan_2022_2023 = models.IntegerField('Суммарный план 2022-2023: ', default=0)
    total_actual_2023_2024 = models.IntegerField('Суммарные выполненные показатели 2023-2024', default=0)
    total_plan_2024_2025 = models.IntegerField('Суммарный план на 2024-2025', default=0)

    def __str__(self):
        return f"Admin Report for {self.indicator.name}"

    @classmethod
    def aggregate_reports(cls):
        indicators = Indicator.objects.all()
        for indicator in indicators:
            report_data = TeacherReport.objects.filter(indicator=indicator).aggregate(
                total_plan_2022_2023=Sum('plan_2022_2023'),
                total_actual_2023_2024=Sum('actual_2023_2024'),
                total_plan_2024_2025=Sum('plan_2024_2025'),
            )

            total_plan_2022_2023 = report_data.get('total_plan_2022_2023', 0)
            total_actual_2023_2024 = report_data.get('total_actual_2023_2024', 0)
            total_plan_2024_2025 = report_data.get('total_plan_2024_2025', 0)

            # Обновляем или создаем новый отчет для администратора
            cls.objects.update_or_create(
                indicator=indicator,
                defaults={
                    'total_plan_2022_2023': total_plan_2022_2023,
                    'total_actual_2023_2024': total_actual_2023_2024,
                    'total_plan_2024_2025': total_plan_2024_2025,
                }
            )

    class Meta:
        verbose_name = 'Агрегированные данные'
        verbose_name_plural = 'Агрегированные данные'


