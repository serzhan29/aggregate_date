from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import TeacherReport, Indicator, AdminReport, User, MainIndicator, IndicatorSum, Direction
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist




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

""" Main PAGE """
@login_required
@user_passes_test(is_teacher)
def teacher_report(request, user_id):
    # Получаем главные индикаторы и отчеты учителя
    main_indicators = MainIndicator.objects.prefetch_related('indicator_set').all()
    reports = TeacherReport.objects.filter(teacher=request.user)
    direction = Direction.objects.filter(mainindicator__in=main_indicators).distinct()


    # Получаем суммарные индикаторы для текущего учителя
    sum_indicators = IndicatorSum.objects.filter(teacher=request.user)

    # Если у учителя нет отчетов, создаем их с нулевыми значениями
    if not reports:
        for indicator in Indicator.objects.all():
            TeacherReport.objects.create(
                teacher=request.user,
                indicator=indicator,
                plan_2022_2023=0,
                actual_2023_2024=0,
                plan_2024_2025=0,
                comment=''
            )

    # Обновляем отчеты после создания, чтобы получить актуальные данные
    reports = TeacherReport.objects.filter(teacher=request.user)
    report_data = {report.indicator.id: report for report in reports}

    if request.method == 'POST':
        for indicator in Indicator.objects.all():
            report, created = TeacherReport.objects.get_or_create(
                teacher=request.user, indicator=indicator
            )
            actual_2023_2024 = request.POST.get(f'actual_2023_2024_{indicator.id}')
            if actual_2023_2024:
                report.actual_2023_2024 = actual_2023_2024
            report.save()

        return redirect('teacher_report', user_id=user_id)

    context = {
        'main_indicators': main_indicators,
        'sum': sum_indicators,  # Добавляем суммарные индикаторы
        'report_data': reports,
        'direction': direction
    }
    return render(request, 'main/teacher_report.html', context)





@login_required
@user_passes_test(is_teacher)
def teacher_report_23(request, user_id):
    main_indicators = MainIndicator.objects.prefetch_related('indicator_set').all()
    reports = TeacherReport.objects.filter(teacher=request.user)
    sum_indicators = IndicatorSum.objects.filter(teacher=request.user)
    direction = Direction.objects.filter(mainindicator__in=main_indicators).distinct()
    # Создаем словарь для хранения отчетов по индикаторам
    report_data = {}
    for report in reports:
        report_data[report.indicator.id] = {
            'plan_2022_2023': report.plan_2022_2023,
            'comment': report.comment,
        }

    if request.method == 'POST':
        # Проходим по каждому индикатору и сохраняем данные
        for indicator in Indicator.objects.all():
            report, created = TeacherReport.objects.get_or_create(
                teacher=request.user, indicator=indicator
            )

            # Обновляем поля только если данные есть в POST и они не пустые
            plan_2022_2023 = request.POST.get(f'plan_2022_2023_{indicator.id}')
            if plan_2022_2023:
                report.plan_2022_2023 = plan_2022_2023

            comment = request.POST.get(f'comment_{indicator.id}')
            if comment:
                report.comment = comment

            report.save()

        return redirect('23', user_id=user_id)

    context = {
        'main_indicators': main_indicators,
        'sum': sum_indicators,  # Добавляем суммарные индикаторы
        'report_data': reports,  # Передаем существующие данные отчета
        'direction': direction
    }
    return render(request, 'main/plan-22/23.html', context)


@login_required
@user_passes_test(is_teacher)
def teacher_report_25(request, user_id):
    main_indicators = MainIndicator.objects.prefetch_related('indicator_set').all()
    reports = TeacherReport.objects.filter(teacher=request.user)
    sum_indicators = IndicatorSum.objects.filter(teacher=request.user)
    direction = Direction.objects.filter(mainindicator__in=main_indicators).distinct()
    # Создаем словарь для хранения отчетов по индикаторам
    report_data = {}
    for report in reports:
        report_data[report.indicator.id] = {
            'plan_2024_2025': report.plan_2024_2025,
            'comment': report.comment,
        }

    if request.method == 'POST':
        # Проходим по каждому индикатору и сохраняем данные
        for indicator in Indicator.objects.all():
            report, created = TeacherReport.objects.get_or_create(
                teacher=request.user, indicator=indicator
            )

            # Обновляем поля только если данные есть в POST и они не пустые
            plan_2024_2025 = request.POST.get(f'plan_2024_2025_{indicator.id}')
            if plan_2024_2025:
                report.plan_2024_2025 = plan_2024_2025

            comment = request.POST.get(f'comment_{indicator.id}')
            if comment:
                report.comment = comment

            report.save()

        return redirect('25', user_id=user_id)

    context = {
        'main_indicators': main_indicators,
        'sum': sum_indicators,  # Добавляем суммарные индикаторы
        'report_data': reports,  # Передаем существующие данные отчета
        'direction': direction
    }
    return render(request, 'main/plan-22/25.html', context)


#=========================Summa Indicators============================
#====================================================================
def teacher_report_summary(request, user_id):
    # Получаем объект User (учителя)
    teacher = get_object_or_404(User, id=user_id)

    # Определите основной индикатор, который должен быть связан с учителем.
    main_indicators = MainIndicator.objects.all()  # Допустим, вы хотите для всех индикаторов создать записи.

    # Цикл по всем индикаторам и создание записей, если их нет.
    indicator_sums = []
    for main_indicator in main_indicators:
        indicator_sum, created = IndicatorSum.objects.get_or_create(
            teacher=teacher,
            main_indicator=main_indicator,  # Замените это на правильное поле
            defaults={
                'total_plan_2022_2023': 0,  # Установите значения по умолчанию
                'total_actual_2023_2024': 0,
                'total_plan_2024_2025': 0,
            }
        )
        # Вызываем метод aggregate_reports для каждого объекта
        indicator_sum.aggregate_reports()
        indicator_sums.append(indicator_sum)

    context = {
        'teacher': teacher,
        'indicator_sums': indicator_sums,
    }

    return render(request, 'main/new_sum2.html', context)




#====================================================================
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



