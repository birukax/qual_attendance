from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from attendance.models import Attendance, DailyRecord
from leave.models import Leave
from holiday.models import Holiday
from overtime.models import Overtime
from django.core.paginator import Paginator
from attendance.compiler import save_data
from django.contrib.auth.decorators import permission_required
import datetime


@login_required
@permission_required("account.can_approve")
def approval(request):
    attendances = Attendance.objects.filter(approved=False, rejected=False)
    approved_attendances = Attendance.objects.filter(approved=True)
    rejected_attendances = Attendance.objects.filter(rejected=True)
    leaves = Leave.objects.filter(approved=False, rejected=False)
    approved_leaves = Leave.objects.filter(approved=True)
    rejected_leaves = Leave.objects.filter(rejected=True)
    holidays = Holiday.objects.filter(approved=False, rejected=False)
    approved_holidays = Holiday.objects.filter(approved=True)
    rejected_holidays = Holiday.objects.filter(rejected=True)
    overtimes = Overtime.objects.filter(approved=False, rejected=False)
    approved_overtimes = Overtime.objects.filter(approved=True)
    rejected_overtimes = Overtime.objects.filter(rejected=True)

    context = {
        "attendances": attendances,
        "approved_attendances": approved_attendances,
        "rejected_attendances": rejected_attendances,
        "leaves": leaves,
        "approved_leaves": approved_leaves,
        "rejected_leaves": rejected_leaves,
        "holidays": holidays,
        "approved_holidays": approved_holidays,
        "rejected_holidays": rejected_holidays,
        "overtimes": overtimes,
        "approved_overtimes": approved_overtimes,
        "rejected_overtimes": rejected_overtimes,
    }
    return render(request, "approval/list.html", context)


@login_required
@permission_required("account.can_approve")
def attendance_approval(request):
    attendances = Attendance.objects.filter(approved=False, rejected=False)
    paginated = Paginator(attendances, 10)
    page_number = request.GET.get("page")
    page = paginated.get_page(page_number)
    context = {
        "page": page,
    }
    return render(request, "approval/attendance_approval.html", context)


@login_required
@permission_required("account.can_approve")
def approve_attendance(request):
    # attendances = Attendance.objects.filter(approved=False, rejected=False)
    # for attendance in attendances:
    #     attendance.approved = True
    #     attendance.save()
    daily_record = DailyRecord.objects.all()
    if daily_record:
        date = daily_record.latest("date").date + datetime.timedelta(days=1)
    else:
        date = datetime.date.today() - datetime.timedelta(days=1)
    save_data(request, date)
    return redirect("approval:attendance_approval")


@login_required
@permission_required("account.can_approve")
def reject_attendance(request):
    pass
    # attendances = Attendance.objects.filter(approved=False, rejected=False)
    # for attendance in attendances:
    #     attendance.rejected = True
    #     attendance.save()


@login_required
@permission_required("account.can_approve")
def leave_approval(request):
    leaves = Leave.objects.filter(approved=False, rejected=False)
    paginated = Paginator(leaves, 10)
    page_number = request.GET.get("page")
    page = paginated.get_page(page_number)
    context = {"page": page}
    return render(request, "approval/leave_approval.html", context)


@login_required
@permission_required("account.can_approve")
def approve_leave(request, id):
    leave = get_object_or_404(Leave, id=id)
    leave.approved = True
    leave.approved_by = request.user
    leave.save()
    return redirect("approval:leave_approval")


@login_required
@permission_required("account.can_approve")
def reject_leave(request, id):
    leave = get_object_or_404(Leave, id=id)
    leave.rejected = True
    leave.save()
    return redirect("approval:leave_approval")


@login_required
@permission_required("account.can_approve")
def overtime_approval(request):
    overtimes = Overtime.objects.filter(approved=False, rejected=False)
    paginated = Paginator(overtimes, 10)
    page_number = request.GET.get("page")
    page = paginated.get_page(page_number)
    context = {"page": page}
    return render(request, "approval/overtime_approval.html", context)


@login_required
@permission_required("account.can_approve")
def approve_overtime(request, id):
    overtime = get_object_or_404(Overtime, id=id)
    overtime.approved = True
    overtime.approved_by = request.user
    overtime.save()
    return redirect("approval:overtime_approval")


@login_required
@permission_required("account.can_approve")
def reject_overtime(request, id):
    overtime = get_object_or_404(Overtime, id=id)
    overtime.rejected = True
    overtime.save()
    return redirect("approval:overtime_approval")


@login_required
@permission_required("account.can_approve")
def holiday_approval(request):
    holidays = Holiday.objects.filter(approved=False, rejected=False)
    paginated = Paginator(holidays, 10)
    page_number = request.GET.get("page")
    page = paginated.get_page(page_number)
    context = {"page": page}
    return render(request, "approval/holiday_approval.html", context)


@login_required
@permission_required("account.can_approve")
def approve_holiday(request, id):
    holiday = get_object_or_404(Holiday, id=id)
    holiday.approved = True
    holiday.approved_by = request.user
    holiday.save()
    return redirect("approval:holiday_approval")


@login_required
@permission_required("account.can_approve")
def reject_holiday(request, id):
    holiday = get_object_or_404(Holiday, id=id)
    holiday.rejected = True
    holiday.save()
    return redirect("approval:holiday_approval")
