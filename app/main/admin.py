from django.contrib import admin
from import_export import resources, fields
from import_export.admin import ExportActionModelAdmin
from .models import (User, Indicator, TeacherReport, AdminReport, MainIndicator, IndicatorSum,
                     Direction, Coauthor, CoauthorScore, Article)
from import_export.formats.base_formats import XLSX
from import_export.widgets import ForeignKeyWidget

# Настройка админки для кастомной модели User
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id','username', 'first_name', 'last_name', 'role')  # Поля для отображения в списке
    list_display_links = ('id', 'username', )
    search_fields = ('username', 'email')  # Поля для поиска
    list_filter = ('role',)  # Фильтрация по роли

    # Если поле role - это свойство или метод, добавьте его так:
    def role(self, obj):
        return obj.get_role_display()  # Например, если role - это выбор из списка
    role.admin_order_field = 'role'  # Это позволит сортировать по этому полю
    role.short_description = 'Роль'

# Настройка админки для модели Indicator
@admin.register(Indicator)
class IndicatorAdmin(admin.ModelAdmin):
    list_display = ('name', 'unit')  # Поля, которые будут отображаться в списке
    search_fields = ('name',)  # Поля, по которым можно искать

# Настройка админки для модели TeacherReport
@admin.register(TeacherReport)
class TeacherReportAdmin(admin.ModelAdmin):
    list_display = ('teacher', 'indicator', 'plan_2022_2023', 'actual_2023_2024', 'plan_2024_2025', 'comment')
    search_fields = ('teacher__username', 'indicator__name')  # Поля, по которым можно искать
    list_filter = ('teacher', 'indicator')  # Фильтрация по полям

# Ресурс для модели AdminReport
class AdminReportResource(resources.ModelResource):
    indicator = fields.Field(
        column_name='Индикатор',
        attribute='indicator',
        widget=ForeignKeyWidget(Indicator, 'name')
    )
    total_plan_2022_2023 = fields.Field(
        column_name='Суммарный план 2022-2023',
        attribute='total_plan_2022_2023'
    )
    total_actual_2023_2024 = fields.Field(
        column_name='Суммарные выполненные показатели 2023-2024',
        attribute='total_actual_2023_2024'
    )
    total_plan_2024_2025 = fields.Field(
        column_name='Суммарный план на 2024-2025',
        attribute='total_plan_2024_2025'
    )

    class Meta:
        model = AdminReport
        fields = ('indicator', 'total_plan_2022_2023', 'total_actual_2023_2024', 'total_plan_2024_2025')

# Определение админки для модели AdminReport
@admin.register(AdminReport)
class AdminReportAdmin(ExportActionModelAdmin):
    resource_class = AdminReportResource
    list_display = ('indicator_name', 'total_plan_2022_2023', 'total_actual_2023_2024', 'total_plan_2024_2025')
    search_fields = ('indicator__name',)
    formats = [XLSX]

    def indicator_name(self, obj):
        return obj.indicator.name
    indicator_name.short_description = 'Индикатор'

# Ресурс для модели IndicatorSum
class IndicatorSumResource(resources.ModelResource):
    main_indicator = fields.Field(
        column_name='Основной Индикатор',
        attribute='main_indicator'
    )
    teacher = fields.Field(
        column_name='Учитель',
        attribute='teacher'
    )
    total_plan_2022_2023 = fields.Field(
        column_name='Суммарный план 2022-2023',
        attribute='total_plan_2022_2023'
    )
    total_actual_2023_2024 = fields.Field(
        column_name='Суммарные выполненные показатели 2023-2024',
        attribute='total_actual_2023_2024'
    )
    total_plan_2024_2025 = fields.Field(
        column_name='Суммарный план на 2024-2025',
        attribute='total_plan_2024_2025'
    )

    class Meta:
        model = IndicatorSum
        fields = ('main_indicator', 'teacher', 'total_plan_2022_2023', 'total_actual_2023_2024', 'total_plan_2024_2025')

# Определение админки для модели IndicatorSum
@admin.register(IndicatorSum)
class AdminIndicatorSum(ExportActionModelAdmin):
    resource_class = IndicatorSumResource
    list_display = ('main_indicator', 'teacher', 'total_plan_2022_2023', 'total_actual_2023_2024', 'total_plan_2024_2025')
    list_display_links = ('main_indicator',)
    formats = [XLSX]  # Добавьте формат XLSX для экспорта

admin.site.register(MainIndicator)
admin.site.register(Direction)

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'indicator', 'teacher', 'get_coauthors', 'created_at', 'start', 'deadline')
    list_display_links = ('title', 'indicator', 'teacher')  # Можно оставить ссылки только на важные поля
    search_fields = ('title', 'indicator__name', 'teacher__username')  # Поиск по названию статьи, индикатору и имени пользователя преподавателя
    list_filter = ('indicator', 'teacher', 'coauthors', 'created_at', 'start', 'deadline')  # Фильтры для административной панели

    # Метод для отображения coauthors в админке
    def get_coauthors(self, obj):
        return ", ".join([str(coauthor) for coauthor in obj.coauthors.all()])
    get_coauthors.short_description = 'Соавторы'  # Название столбца в админке