from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import TeacherReport, Indicator, AdminReport, User, MainIndicator, IndicatorSum
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
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

""" Main PAGE """
@login_required
@user_passes_test(is_teacher)
def teacher_report(request, user_id):
    # Получаем главные индикаторы и отчеты учителя
    main_indicators = MainIndicator.objects.prefetch_related('indicator_set').all()
    reports = TeacherReport.objects.filter(teacher=request.user)

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
    }
    return render(request, 'main/teacher_report.html', context)





@login_required
@user_passes_test(is_teacher)
def teacher_report_23(request, user_id):
    main_indicators = MainIndicator.objects.prefetch_related('indicator_set').all()
    reports = TeacherReport.objects.filter(teacher=request.user)
    sum_indicators = IndicatorSum.objects.filter(teacher=request.user)
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
    }
    return render(request, 'main/plan-22/23.html', context)


@login_required
@user_passes_test(is_teacher)
def teacher_report_25(request, user_id):
    main_indicators = MainIndicator.objects.prefetch_related('indicator_set').all()
    reports = TeacherReport.objects.filter(teacher=request.user)
    sum_indicators = IndicatorSum.objects.filter(teacher=request.user)
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
    }
    return render(request, 'main/plan-22/25.html', context)


#=========================Summa Indicators============================
@login_required
@user_passes_test(is_teacher)
def indicator_sum_view(request, user_id):
    main_indicators = MainIndicator.objects.prefetch_related('indicator_set').all()
    total_indicators = []

    # Суммируем значения по каждому главному индикатору
    for main_indicator in main_indicators:
        total_plan_2022_2023 = TeacherReport.objects.filter(
            teacher=request.user,
            main_indicator=main_indicator
        ).aggregate(Sum('plan_2022_2023'))['plan_2022_2023__sum'] or 0

        total_actual_2023_2024 = TeacherReport.objects.filter(
            teacher=request.user,
            main_indicator=main_indicator
        ).aggregate(Sum('actual_2023_2024'))['actual_2023_2024__sum'] or 0

        total_plan_2024_2025 = TeacherReport.objects.filter(
            teacher=request.user,
            main_indicator=main_indicator
        ).aggregate(Sum('plan_2024_2025'))['plan_2024_2025__sum'] or 0

        total_indicators.append({
            'main_indicator': main_indicator,
            'total_plan_2022_2023': total_plan_2022_2023,
            'total_actual_2023_2024': total_actual_2023_2024,
            'total_plan_2024_2025': total_plan_2024_2025,
        })

    context = {
        'total_indicators': total_indicators,
    }
    return render(request, 'main/indicator_sum.html', context)

@login_required
@user_passes_test(is_teacher)
def save_indicator_sum(request):
    if request.method == 'POST':
        main_indicator_ids = request.POST.getlist('main_indicator_ids')
        total_plan_2022_2023 = request.POST.getlist('total_plan_2022_2023')
        total_actual_2023_2024 = request.POST.getlist('total_actual_2023_2024')
        total_plan_2024_2025 = request.POST.getlist('total_plan_2024_2025')

        for main_indicator_id, plan_2022_2023, actual_2023_2024, plan_2024_2025 in zip(main_indicator_ids, total_plan_2022_2023, total_actual_2023_2024, total_plan_2024_2025):
            IndicatorSum.objects.update_or_create(
                teacher=request.user,
                main_indicator_id=main_indicator_id,
                defaults={
                    'total_plan_2022_2023': float(plan_2022_2023),
                    'total_actual_2023_2024': float(actual_2023_2024),
                    'total_plan_2024_2025': float(plan_2024_2025),
                }
            )

        # Перенаправление после сохранения
        return redirect('teacher_report', user_id=request.user.id)

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
#====================================================================
@login_required
@user_passes_test(is_teacher)
def sum_report_data_view(request, user_id):
    # Получаем все главные индикаторы
    main_indicators = MainIndicator.objects.prefetch_related('indicator_set').all()
    total_indicators = []

    # Суммируем значения по каждому главному индикатору
    for main_indicator in main_indicators:
        total_plan_2022_2023 = 0
        total_actual_2023_2024 = 0
        total_plan_2024_2025 = 0

        # Суммируем значения, полученные из формы
        for indicator in main_indicator.indicator_set.all():
            # Получаем значения из формы
            plan_2022_2023 = request.POST.get(f'plan_2022_2023_{indicator.id}', 0)
            actual_2023_2024 = request.POST.get(f'actual_2023_2024_{indicator.id}', 0)
            plan_2024_2025 = request.POST.get(f'plan_2024_2025_{indicator.id}', 0)

            total_plan_2022_2023 += float(plan_2022_2023)
            total_actual_2023_2024 += float(actual_2023_2024)
            total_plan_2024_2025 += float(plan_2024_2025)

        total_indicators.append({
            'main_indicator': main_indicator,
            'total_plan_2022_2023': total_plan_2022_2023,
            'total_actual_2023_2024': total_actual_2023_2024,
            'total_plan_2024_2025': total_plan_2024_2025,
        })

    context = {
        'total_indicators': total_indicators,
    }
    return render(request, 'main/new_sum.html', context)

@login_required
@user_passes_test(is_teacher)
def save_report_data(request):
    if request.method == 'POST':
        main_indicator_ids = request.POST.getlist('main_indicator_ids')
        total_indicators_data = []

        # Получаем и суммируем значения для сохранения
        for main_indicator_id in main_indicator_ids:
            total_plan_2022_2023 = 0
            total_actual_2023_2024 = 0
            total_plan_2024_2025 = 0

            for indicator_id in Indicator.objects.filter(main_indicator_id=main_indicator_id).values_list('id', flat=True):
                plan_2022_2023 = request.POST.get(f'plan_2022_2023_{indicator_id}', 0)
                actual_2023_2024 = request.POST.get(f'actual_2023_2024_{indicator_id}', 0)
                plan_2024_2025 = request.POST.get(f'plan_2024_2025_{indicator_id}', 0)

                total_plan_2022_2023 += float(plan_2022_2023)
                total_actual_2023_2024 += float(actual_2023_2024)
                total_plan_2024_2025 += float(plan_2024_2025)

            total_indicators_data.append((main_indicator_id, total_plan_2022_2023, total_actual_2023_2024, total_plan_2024_2025))

        # Сохраняем в базу данных
        for main_indicator_id, plan_2022_2023, actual_2023_2024, plan_2024_2025 in total_indicators_data:
            IndicatorSum.objects.update_or_create(
                teacher=request.user,
                main_indicator_id=main_indicator_id,
                defaults={
                    'total_plan_2022_2023': plan_2022_2023,
                    'total_actual_2023_2024': actual_2023_2024,
                    'total_plan_2024_2025': plan_2024_2025,
                }
            )

        # Перенаправление после сохранения
        return redirect('teacher_report', user_id=request.user.id)

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


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



