from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import TeacherReport, Indicator, AdminReport, User
from .forms import TeacherReportForm
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import F, Sum

def home(request):
    if not request.user.is_authenticated:
        return redirect('login')
    else:
        if request.user.role == 'teacher':
            return redirect('teacher_report', user_id=request.user.id)
        elif request.user.role == 'admin':
            return redirect('admin_report')
        else:
            # Обработка случая, когда роль не определена
            return redirect('login')  # Или другую подходящую страницу


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            if user.role == 'teacher':
                return redirect('teacher_report', user_id=user.id)
            elif user.role == 'admin':
                return redirect('admin_report')
            else:
                return redirect('login')  # Или другую подходящую страницу
    else:
        form = CustomUserCreationForm()
    return render(request, 'main/user/register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if user.role == 'teacher':
                return redirect('teacher_report', user_id=user.id)
            elif user.role == 'admin':
                return redirect('admin_report')
            else:
                return redirect('login')  # Или другую подходящую страницу
    else:
        form = CustomAuthenticationForm()
    return render(request, 'main/user/login.html', {'form': form})



# Выход пользователя
@login_required
def user_logout(request):
    logout(request)
    return redirect('login')  # Перенаправляем на страницу входа



# Проверка, что пользователь - учитель
def is_teacher(user):
    return user.role == 'teacher'

# Проверка, что пользователь - администратор
def is_admin(user):
    return user.role == 'admin'

# Представление для учителей, где они могут заполнить свои отчеты
@login_required
@user_passes_test(is_teacher)
def teacher_report_view(request, user_id):
    indicators = Indicator.objects.all()  # Получаем все индикаторы
    reports = TeacherReport.objects.filter(teacher=request.user)  # Получаем отчеты для конкретного учителя

    # Создаем список отчетов
    reports_list = list(reports)

    if request.method == 'POST':
        # Для каждого индикатора создаем форму и сохраняем данные
        for indicator in indicators:
            report, created = TeacherReport.objects.get_or_create(
                teacher=request.user, indicator=indicator
            )

            # Получаем данные из POST-запроса
            report.plan_2022_2023 = request.POST.get(f'plan_2022_2023_{indicator.id}', report.plan_2022_2023)
            report.actual_2023_2024 = request.POST.get(f'actual_2023_2024_{indicator.id}', report.actual_2023_2024)
            report.plan_2024_2025 = request.POST.get(f'plan_2024_2025_{indicator.id}', report.plan_2024_2025)
            report.comment = request.POST.get(f'comment_{indicator.id}', report.comment)
            report.save()

        return redirect('teacher_report', user_id=user_id)

    context = {
        'indicators': indicators,
        'reports_list': reports_list,
    }
    return render(request, 'main/teacher_report.html', context)


# Представление для администратора: агрегация данных всех учителей
@login_required
@user_passes_test(is_admin)
def admin_report_view(request):
    # Получаем агрегированные отчеты
    admin_reports = AdminReport.objects.all()

    # Если данных нет, агрегируем
    if not admin_reports:
        AdminReport.aggregate_reports()  # Агрегируем данные с помощью метода модели
        admin_reports = AdminReport.objects.all()

    context = {
        'admin_reports': admin_reports,
    }
    return render(request, 'main/admin_report.html', context)


# Функция для обновления агрегированных данных для администратора (может быть вызвана вручную)
@login_required
@user_passes_test(is_admin)
def update_admin_reports(request):
    AdminReport.aggregate_reports()
    return redirect('admin_report')

from django.http import JsonResponse


@login_required
def report_details(request, indicator_id):
    try:
        # Получаем индикатор по ID
        indicator = get_object_or_404(Indicator, id=indicator_id)

        # Получаем отчеты учителей для данного индикатора
        reports = TeacherReport.objects.filter(indicator=indicator)

        # Получаем суммарные данные из AdminReport для этого индикатора
        admin_report = get_object_or_404(AdminReport, indicator=indicator)

        # Список для хранения данных об отчетах учителей
        teachers = []
        for report in reports:
            # Добавляем учителей и их планы в список
            teachers.append({
                'name': report.teacher.get_full_name(),
                'indicator_name': report.indicator.name,
                'plan_2022_2023': report.plan_2022_2023,
                'actual_2023_2024': report.actual_2023_2024,
                'plan_2024_2025': report.plan_2024_2025,
                'admin_total_plan_2022_2023': admin_report.total_plan_2022_2023,
                'admin_total_actual_2023_2024': admin_report.total_actual_2023_2024,
                'admin_total_plan_2024_2025': admin_report.total_plan_2024_2025,
            })

        return render(request, 'main/report_details.html', {
            'teachers': teachers,
            'indicator_name': indicator.name,
            'admin_report': admin_report
        })

    except ObjectDoesNotExist as e:
        return render(request, 'main/report_details.html', {'error': f'Ошибка: {str(e)}'})
    except Exception as e:
        print(f"Unexpected Error: {e}")
        return render(request, 'main/report_details.html', {'error': 'Произошла непредвиденная ошибка'})




