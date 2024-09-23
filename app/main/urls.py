from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # Главная страница
    path('teacher-report/<int:user_id>/', views.teacher_report_view, name='teacher_report'),
    path('admin-report/', views.admin_report_view, name='admin_report'),
    path('update-admin-reports/', views.update_admin_reports, name='update_admin_reports'),
    path('reports/report-details/<int:indicator_id>/', views.report_details, name='report_details'),

    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
]

