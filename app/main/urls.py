from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # Главная страница

    # Путь для просмотра и редактирования отчета учителя
    path('teacher-report/<int:user_id>/', views.teacher_report, name='teacher_report'),

    # Путь для просмотра отчета администратора
    path('admin-report/', views.admin_report_view, name='admin_report'),

    # Путь для обновления отчетов администратора
    path('update-admin-reports/', views.update_admin_reports, name='update_admin_reports'),

    # Путь для просмотра детальной информации по отдельному индикатору
    path('reports/report-details/<int:indicator_id>/', views.report_details, name='report_details'),

    path('indicator-sum/<int:user_id>/', views.indicator_sum_view, name='indicator_sum_view'),
    path('plan-2022-2023/<int:user_id>/', views.teacher_report_23, name='23'),
    path('plan-2024-2025/<int:user_id>/', views.teacher_report_25, name='25'),
    path('save_indicator_sum/', views.save_indicator_sum, name='save_indicator_sum'),

    path('report/sum/<int:user_id>/', views.sum_report_data_view, name='sum_report_data'),
    path('report/save/', views.save_report_data, name='save_report_data'),

    # Пути для регистрации, входа и выхода пользователя
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
]
