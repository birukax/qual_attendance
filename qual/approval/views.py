from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from attendance.models import Attendance, OnField
from leave.models import Leave
from holiday.models import Holiday
from overtime.models import Overtime

from django.core.paginator import Paginator
from attendance.tasks import save_data

# import datetime
# from overtime.tasks import create_ots
from django.contrib.auth.decorators import user_passes_test
from .filters import LeaveFilter, OvertimeFilter
from leave.tasks import calculate_total_leave_days


@login_required
# @user_passes_test(lambda u: u.profile.role == "HR")
@user_passes_test(lambda u: u.has_perm("account.can_approve"))
def approval(request):
    leaves = Leave.objects.filter(approved=False, rejected=False)
    holidays = Holiday.objects.filter(approved=False, rejected=False)
    overtimes = Overtime.objects.filter(approved=False, rejected=False)
    on_fields = OnField.objects.filter(approved=False, rejected=False)

    context = {
        "on_fields": on_fields,
        "leaves": leaves,
        "holidays": holidays,
        "overtimes": overtimes,
    }
    return render(request, "approval/list.html", context)


@login_required
@user_passes_test(lambda u: u.profile.role == "ADMIN")
@user_passes_test(lambda u: u.has_perm("account.can_approve"))
def attendance_approval(request):
    attendances = Attendance.objects.filter(approved=False, rejected=False).order_by(
        "check_in_time"
    )
    paginated = Paginator(attendances, 30)
    page_number = request.GET.get("page")
    page = paginated.get_page(page_number)
    context = {
        "page": page,
    }
    return render(request, "approval/attendance/list.html", context)


@login_required
# @user_passes_test(lambda u: u.profile.role == "HR")
# @user_passes_test(lambda u: u.has_perm("account.can_approve"))
def approve_attendance(request):
    # daily_record = DailyRecord.objects.all()
    request_device = request.user.profile.device
    attendance = Attendance.objects.filter(
        approved=False,
        deleted=False,
        recompiled=False,
        device=request_device,
    )
    if attendance:
        date = attendance.first().check_in_date
        if attendance.first().compile_date == date:
            return redirect("attendance:compile_view")
        try:
            save_data(request, date)
        except Exception as e:
            print(e)
    return redirect("attendance:compile_view")


@login_required
# @user_passes_test(lambda u: u.profile.role == "HR")
@user_passes_test(lambda u: u.has_perm("account.can_approve"))
def reject_attendance(request):
    pass
    # attendances = Attendance.objects.filter(approved=False, rejected=False)
    # for attendance in attendances:
    #     attendance.rejected = True
    #     attendance.save()


@login_required
# @user_passes_test(lambda u: u.profile.role == "HR")
@user_passes_test(lambda u: u.has_perm("account.can_approve"))
def leave_approval(request):
    leaves = Leave.objects.filter(approved=False, rejected=False).order_by("start_date")
    for l in leaves:
        calculate_total_leave_days(l.id)
    leave_filter = LeaveFilter(request.GET, queryset=leaves)
    leaves = leave_filter.qs

    paginated = Paginator(leaves, 30)
    page_number = request.GET.get("page")
    page = paginated.get_page(page_number)
    context = {
        "page": page,
        "leave_filter": leave_filter,
    }
    return render(request, "approval/leave/list.html", context)


@login_required
# @user_passes_test(lambda u: u.profile.role == "HR")
@user_passes_test(lambda u: u.has_perm("account.can_approve"))
def approve_leave(request, id):
    user = request.user
    leave = get_object_or_404(Leave, id=id)
    if user.profile.employee == leave.employee:
        return redirect("approval:leave_approval")
    leave.approved = True
    leave.active = True
    leave.approved_by = user
    leave.save()
    attendances = Attendance.objects.filter(
        employee=leave.employee,
        check_in_date__gte=leave.start_date,
        check_in_date__lte=leave.end_date,
        status__in=("Absent", "Day Off"),
    )
    if attendances:
        for attendance in attendances:
            print(attendance.check_in_date)
            attendance.status = "On Leave"
            attendance.leave_type = leave.leave_type
            attendance.save()
    return redirect("approval:leave_approval")


@login_required
# @user_passes_test(lambda u: u.profile.role == "HR")
@user_passes_test(lambda u: u.has_perm("account.can_approve"))
def reject_leave(request, id):
    user = request.user
    leave = get_object_or_404(Leave, id=id)
    if user.profile.employee == leave.employee:
        return redirect("approval:leave_approval")
    leave.rejected = True
    leave.rejected_by = request.user
    leave.save()
    return redirect("approval:leave_approval")


@login_required
# @user_passes_test(lambda u: u.profile.role == "HR")
@user_passes_test(lambda u: u.has_perm("account.can_approve"))
def overtime_approval(request):
    overtimes = Overtime.objects.filter(approved=False, rejected=False).order_by(
        "start_date"
    )
    overtime_filter = OvertimeFilter(request.GET, queryset=overtimes)
    overtimes = overtime_filter.qs
    paginated = Paginator(overtimes, 30)
    page_number = request.GET.get("page")
    page = paginated.get_page(page_number)
    context = {
        "page": page,
        "overtime_filter": overtime_filter,
    }
    return render(request, "approval/overtime/list.html", context)


@login_required
# @user_passes_test(lambda u: u.profile.role == "HR")
@user_passes_test(lambda u: u.has_perm("account.can_approve"))
def approve_overtime(request, id):
    overtime = get_object_or_404(Overtime, id=id)
    overtime.approved = True
    overtime.approved_by = request.user
    overtime.save()
    # create_ots(overtime.id)
    return redirect("approval:overtime_approval")


@login_required
# @user_passes_test(lambda u: u.profile.role == "HR")
@user_passes_test(lambda u: u.has_perm("account.can_approve"))
def reject_overtime(request, id):
    overtime = get_object_or_404(Overtime, id=id)
    overtime.rejected = True
    overtime.save()
    return redirect("approval:overtime_approval")


@login_required
# @user_passes_test(lambda u: u.profile.role == "HR")
@user_passes_test(lambda u: u.has_perm("account.can_approve"))
def holiday_approval(request):
    holidays = Holiday.objects.filter(approved=False, rejected=False).order_by("date")
    paginated = Paginator(holidays, 30)
    page_number = request.GET.get("page")
    page = paginated.get_page(page_number)
    context = {"page": page}
    return render(request, "approval/holiday/list.html", context)


@login_required
# @user_passes_test(lambda u: u.profile.role == "HR")
@user_passes_test(lambda u: u.has_perm("account.can_approve"))
def approve_holiday(request, id):
    holiday = get_object_or_404(Holiday, id=id)
    holiday.approved = True
    holiday.approved_by = request.user
    holiday.save()
    return redirect("approval:holiday_approval")


# @user_passes_test(lambda u: u.profile.role == "HR")
@login_required
@user_passes_test(lambda u: u.has_perm("account.can_approve"))
def reject_holiday(request, id):
    holiday = get_object_or_404(Holiday, id=id)
    holiday.rejected = True
    holiday.save()
    return redirect("approval:holiday_approval")


@login_required
# @user_passes_test(lambda u: u.profile.role == "HR")
@user_passes_test(lambda u: u.has_perm("account.can_approve"))
def on_field_approval(request):
    on_fields = OnField.objects.filter(approved=False, rejected=False).order_by(
        "start_date"
    )
    # for l in on_fields:
    #     calculate_total_on_field_days(l.id)
    # on_field_filter = On_fieldFilter(request.GET, queryset=on_fields)
    # on_fields = on_field_filter.qs

    paginated = Paginator(on_fields, 30)
    page_number = request.GET.get("page")
    page = paginated.get_page(page_number)
    context = {
        "page": page,
        # "on_field_filter": on_field_filter,
    }
    return render(request, "approval/on_field/list.html", context)


@login_required
# @user_passes_test(lambda u: u.profile.role == "HR")
@user_passes_test(lambda u: u.has_perm("account.can_approve"))
def approve_on_field(request, id):
    on_field = get_object_or_404(OnField, id=id)
    on_field.approved = True
    on_field.approved_by = request.user
    on_field.save()
    attendances = Attendance.objects.filter(
        employee=on_field.employee,
        check_in_date__gte=on_field.start_date,
        check_in_date__lte=on_field.end_date,
        status="Absent",
    )
    if attendances:
        for attendance in attendances:
            # print(attendance.check_in_date)
            attendance.status = "On Field"
            attendance.save()
    return redirect("approval:on_field_approval")


@login_required
# @user_passes_test(lambda u: u.profile.role == "HR")
@user_passes_test(lambda u: u.has_perm("account.can_approve"))
def reject_on_field(request, id):
    on_field = get_object_or_404(OnField, id=id)
    on_field.rejected = True
    on_field.rejected_by = request.user
    on_field.save()
    return redirect("approval:on_field_approval")
