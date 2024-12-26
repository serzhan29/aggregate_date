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

    path('plan-2022-2023/<int:user_id>/', views.teacher_report_23, name='23'),
    path('plan-2024-2025/<int:user_id>/', views.teacher_report_25, name='25'),


    path('teacher-report-summary/<int:user_id>/', views.teacher_report_summary, name='teacher-report-summary'),

    path('indicator/<int:indicator_id>/articles/', views.indicator_articles, name='indicator_articles'),
    path('indicator/<int:indicator_id>/articles/<int:deadline_year>/', views.indicator_articles,
         name='indicator_articles_by_year'),
    path('article/edit/<int:article_id>/', views.edit_article, name='edit_article'),
    path('article/delete/<int:article_id>/', views.delete_article, name='delete_article'),

    path('teachers/', views.teacher_list, name='teacher_list'),
    path('teachers/<int:teacher_id>/', views.teacher_reports, name='teacher_reports'),

    # Пути для регистрации, входа и выхода пользователя
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
]
