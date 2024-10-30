from django.db.models import Sum, CASCADE
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.conf import settings


class User(AbstractUser):
    """Пользователи"""
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


class Direction(models.Model):
    """ Направление (Академическое, Научное и т.д.) """
    name = models.CharField('Название: ', max_length=255)


    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Направление'
        verbose_name_plural = 'Направление '


class MainIndicator(models.Model):
    """Название Главного индикатора """
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    direction = models.ForeignKey(Direction, on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField('Главный индикатор: ', max_length=255, unique=True)
    amount_2022_2023 = models.IntegerField('Суммарный план 2022-2023: ', default=0)
    amount_2023_2024 = models.IntegerField('Суммарные выполненные показатели 2023-2024', default=0)
    amount_2024_2025 = models.IntegerField('Суммарный план на 2024-2025', default=0)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Главный индикатор'
        verbose_name_plural = 'Главные индикаторы'


# Модель для индикативных показателей
class Indicator(models.Model):
    """ Под индикатор """
    main_name = models.ForeignKey(MainIndicator, on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField('Название индикатора: ', max_length=255)  # (например, публикации в Scopus)
    unit = models.CharField('Единица измерения:', max_length=50)  # (счет, проценты и т.д.)


    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Индикатор'
        verbose_name_plural = 'Индикаторы'


# Модель для хранения отчетов учителей
class TeacherReport(models.Model):
    """ Отчёт учителей """
    teacher = models.ForeignKey(User, on_delete=models.CASCADE,
                                limit_choices_to={'role': 'teacher'})  # Связь с учителем
    main_indicator = models.ForeignKey(MainIndicator, on_delete=CASCADE, blank=True, null=True)
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
    """ Общая сумма всех индикаторов """
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


class IndicatorSum(models.Model):
    """ Сумма всех индикаторов """
    teacher = models.ForeignKey(User, on_delete=models.CASCADE)
    main_indicator = models.ForeignKey(MainIndicator, on_delete=models.CASCADE)
    total_plan_2022_2023 = models.FloatField(default=0)
    total_actual_2023_2024 = models.FloatField(default=0)
    total_plan_2024_2025 = models.FloatField(default=0)

    def __str__(self):
        return f"{self.teacher.username} - {self.main_indicator.name}"

    class Meta:
        verbose_name = 'Сумма Индикатора'
        verbose_name_plural = 'Сумма Индикаторов'

    def aggregate_reports(self):
        # Получаем все индикаторы, связанные с текущим основным индикатором
        indicators = Indicator.objects.filter(main_name=self.main_indicator)

        # Считаем суммы по отчетам для данного учителя
        total_plan_2022_2023 = TeacherReport.objects.filter(
            indicator__in=indicators,
            teacher=self.teacher
        ).aggregate(total=Sum('plan_2022_2023'))['total'] or 0

        total_actual_2023_2024 = TeacherReport.objects.filter(
            indicator__in=indicators,
            teacher=self.teacher
        ).aggregate(total=Sum('actual_2023_2024'))['total'] or 0

        total_plan_2024_2025 = TeacherReport.objects.filter(
            indicator__in=indicators,
            teacher=self.teacher
        ).aggregate(total=Sum('plan_2024_2025'))['total'] or 0

        # Обновляем значения в текущем объекте
        self.total_plan_2022_2023 = total_plan_2022_2023
        self.total_actual_2023_2024 = total_actual_2023_2024
        self.total_plan_2024_2025 = total_plan_2024_2025
        self.save()
