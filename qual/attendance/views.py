from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from openpyxl import Workbook
from .models import RawAttendance, Attendance, DailyRecord
from employee.models import Employee
from employee.filters import EmployeeFilter
from device.models import Device
from overtime.models import Overtime
from shift.models import Shift
from leave.models import Leave
from holiday.models import Holiday
from django.core.paginator import Paginator
from .filters import (
    CompileFilter,
    AttendanceDownloadFilter,
    CompiledAttendanceDownloadFilter,
    AttendanceFilter,
    RawAttendanceFilter,
)
from device.forms import CreateDeviceForm
import datetime
from .tasks import save_recompiled, sync_raw_attendance, compile
from .forms import RecompileForm, EmployeesForm
from django.db.models import F, Count
from django.contrib.auth.decorators import user_passes_test
import datetime


@login_required
def dashboard(request):
    attendances = Attendance.objects.all()
    employees = Employee.objects.all()
    shifts = Shift.objects.all()
    devices = Device.objects.all()
    overtimes = Overtime.objects.all()
    leaves = Leave.objects.all()
    holidays = Holiday.objects.all()
    approvals = (
        overtimes.filter(approved=False, rejected=False).count()
        + leaves.filter(approved=False, rejected=False).count()
        + holidays.filter(approved=False, rejected=False).count()
    )

    start = datetime.datetime.now().date() - datetime.timedelta(days=30)
    most_absents = (
        employees.filter(
            attendances__status="Absent", attendances__check_in_date__gte=start
        )
        .annotate(absent_count=Count("attendances"))
        .order_by("-absent_count")[:20]
    )

    new_employees = Employee.objects.filter(status="Active").order_by("-employee_id")[
        :5
    ]

    return render(
        request,
        "dashboard.html",
        {
            "attendances": attendances,
            "employees": employees,
            "shifts": shifts,
            "devices": devices,
            "overtimes": overtimes,
            "leaves": leaves,
            "holidays": holidays,
            "approvals": approvals,
            "new_employees": new_employees,
            "most_absents": most_absents,
        },
    )


@login_required
def attendance_list(request):
    user = request.user.profile
    if user.role == "HR" or user.role == "ADMIN":
        # if user.device:
        #     attendances = Attendance.objects.filter(
        #         approved=True, deleted=False, device=user.device
        #     ).order_by("-check_in_date", "check_in_time")
        # else:
        attendances = Attendance.objects.filter(approved=True, deleted=False).order_by(
            "-check_in_date", "check_in_time"
        )
    else:
        attendances = Attendance.objects.filter(
            approved=True, deleted=False, employee__department__in=user.manages.all()
        ).order_by("employee")

    attendance_download_filter = AttendanceDownloadFilter(
        request.GET, queryset=attendances
    )
    attendance_filter = AttendanceFilter(request.GET, queryset=attendances)
    attendances = attendance_filter.qs
    paginated = Paginator(attendances, 30)
    page_number = request.GET.get("page")
    page = paginated.get_page(page_number)
    context = {
        "attendance_download_filter": attendance_download_filter,
        "attendance_filter": attendance_filter,
        "attendances": attendances,
        "page": page,
    }
    return render(
        request,
        "attendance/list.html",
        context,
    )


@login_required
@user_passes_test(lambda u: u.profile.role == "HR" or u.profile.role == "ADMIN")
def compile_view(request):
    request_device = request.user.profile.device
    if not request_device:
        return redirect("attendance:attendances")
    if DailyRecord.objects.filter(device=request_device).exists():
        daily_records = DailyRecord.objects.filter(device=request_device).latest("date")
    else:
        daily_records = []

    no_shift = Employee.objects.filter(
        shift=None, status="Active", device=request_device
    ).count()
    attendances = Attendance.objects.filter(
        approved=False, device=request_device
    ).order_by("check_in_time")
    compile_filter = CompileFilter(request.GET, queryset=attendances)
    attendance_download_filter = CompiledAttendanceDownloadFilter(
        request.GET, queryset=attendances
    )
    attendances = compile_filter.qs

    paginated = Paginator(attendances, 30)
    page_number = request.GET.get("page")
    page = paginated.get_page(page_number)
    context = {
        "page": page,
        "daily_records": daily_records,
        "no_shift": no_shift,
        "compile_filter": compile_filter,
        "attendance_download_filter": attendance_download_filter,
    }
    return render(request, "attendance/compile/list.html", context)


@login_required
@user_passes_test(lambda u: u.profile.role == "HR" or u.profile.role == "ADMIN")
def compile_attendance(request):
    request_device = request.user.profile.device
    if DailyRecord.objects.filter(device=request_device).exists():
        date = DailyRecord.objects.filter(device=request_device).latest(
            "date"
        ).date + datetime.timedelta(days=1)
    else:
        date = datetime.date.today() - datetime.timedelta(days=1)
    try:
        if date > datetime.date.today():
            pass
        else:
            compile(
                date=date,
                employees=None,
                pattern=None,
                recompiled=False,
                request_device=request_device,
            )
    except Exception as e:
        print(e)
    return redirect("attendance:compile_view")


@login_required
def download_compiled_attendance(request):
    user = request.user.profile
    attendances = Attendance.objects.filter(
        approved=False, deleted=False, recompiled=False, device=user.device
    ).order_by("-check_in_time")
    form = CompiledAttendanceDownloadFilter(
        data=request.POST,
        queryset=attendances,
    )
    attendances = form.qs
    response = HttpResponse(content_type="application/ms-excel")
    response["Content-Disposition"] = 'attachment; filename="compiled.xlsx"'
    wb = Workbook()
    ws = wb.active
    ws.title = "Attendance"

    headers = [
        "employee",
        "device",
        "current pattern",
        "check in date",
        "check out date",
        "check in time",
        "check out time",
        "worked_hours",
        "Check in type",
        "Check out type",
        "status",
        "Leave type",
    ]
    ws.append(headers)

    for attendance in attendances.order_by("-check_in_date"):

        if attendance.device:
            device = attendance.device.name
        else:
            device = ""
        if attendance.leave_type:
            leave_type = attendance.leave_type.name
        else:
            leave_type = ""

        ws.append(
            [
                attendance.employee.name,
                device,
                attendance.current_pattern.name,
                attendance.check_in_date,
                attendance.check_out_date,
                attendance.check_in_time,
                attendance.check_out_time,
                attendance.worked_hours,
                attendance.check_in_type,
                attendance.check_out_type,
                attendance.status,
                leave_type,
            ]
        )
    wb.save(response)
    return response


@login_required
@user_passes_test(lambda u: u.profile.role == "HR" or u.profile.role == "ADMIN")
def delete_compiled_attendance(request):
    request_device = request.user.profile.device
    attendances = Attendance.objects.filter(
        device=request_device,
        approved=False,
        recompiled=False,
    )
    if attendances:
        for attendance in attendances:
            attendance.delete()
    return redirect("attendance:compile_view")


@login_required
def download_attendance(request):
    user = request.user.profile
    if user.role == "HR" or user.role == "ADMIN":
        attendances = Attendance.objects.filter(approved=True, deleted=False).order_by(
            "-check_in_date", "-check_in_time"
        )
    else:
        attendances = Attendance.objects.filter(
            approved=True, deleted=False, employee__department__in=user.manages.all()
        ).order_by("-check_in_date", "-check_in_time")
    form = AttendanceDownloadFilter(
        data=request.POST,
        queryset=attendances,
    )
    attendances = form.qs
    response = HttpResponse(content_type="application/ms-excel")
    response["Content-Disposition"] = 'attachment; filename="attendance.xlsx"'
    wb = Workbook()
    ws = wb.active
    ws.title = "Attendance"

    headers = [
        "employee",
        "device",
        "current pattern",
        "check in date",
        "check out date",
        "check in time",
        "check out time",
        "worked_hours",
        "Check in type",
        "Check out type",
        "status",
        "Leave type",
    ]
    ws.append(headers)

    for attendance in attendances.order_by("-check_in_date"):

        if attendance.device:
            device = attendance.device.name
        else:
            device = ""
        if attendance.leave_type:
            leave_type = attendance.leave_type.name
        else:
            leave_type = ""

        ws.append(
            [
                attendance.employee.name,
                device,
                attendance.current_pattern.name,
                attendance.check_in_date,
                attendance.check_out_date,
                attendance.check_in_time,
                attendance.check_out_time,
                attendance.worked_hours,
                attendance.check_in_type,
                attendance.check_out_type,
                attendance.status,
                leave_type,
            ]
        )
    wb.save(response)
    return response


@login_required
@user_passes_test(lambda u: u.profile.role == "HR" or u.profile.role == "ADMIN")
def raw_attendance_list(request):
    # attendances = RawAttendance.objects.all().order_by("-date", "-time")[:1000]
    request_device = request.user.profile.device

    attendances = RawAttendance.objects.all().order_by("-date", "-time")
    attendance_filter = RawAttendanceFilter(request.GET, queryset=attendances)
    attendances = attendance_filter.qs
    paginated = Paginator(attendances, 30)
    page_number = request.GET.get("page")
    page = paginated.get_page(page_number)
    context = {"raw_attendance_filter": attendance_filter, "page": page}
    return render(request, "attendance/raw_attendance/list.html", context)


@login_required
@user_passes_test(lambda u: u.profile.role == "HR" or u.profile.role == "ADMIN")
def get_raw_data(request):
    request_device = request.user.profile.device
    if request_device:
        sync_raw_attendance.delay(request_device=request_device.id)
    else:
        sync_raw_attendance.delay()
    return redirect("attendance:raw_attendance")


@login_required
@user_passes_test(lambda u: u.profile.role == "HR" or u.profile.role == "ADMIN")
def recompile_view(request):
    request_device = request.user.profile.device
    if not request_device:
        return redirect("attendance:attendances")
    recompile_form = RecompileForm()
    qt = request.POST.getlist("employees")
    print(qt)
    employees = Employee.objects.filter(
        employee_id__in=qt, device=request_device
    ).order_by("name")
    attendances = Attendance.objects.filter(
        recompiled=True, approved=False, deleted=False, device=request_device
    ).order_by("-check_in_date", "-check_in_time")
    paginated = Paginator(attendances, 30)
    page_number = request.GET.get("page")
    page = paginated.get_page(page_number)
    context = {
        "recompile_form": recompile_form,
        "attendances": attendances,
        "page": page,
        "employees": employees,
    }
    return render(request, "attendance/recompile/list.html", context)


@login_required
@user_passes_test(lambda u: u.profile.role == "HR" or u.profile.role == "ADMIN")
def recompile(request):
    request_device = request.user.profile.device

    employees = Employee.objects.filter(
        id__in=request.POST.getlist("employees"), device=request_device
    ).values_list("employee_id", flat=True)
    recompile_form = RecompileForm(request.POST)
    if recompile_form.is_valid():
        pattern = recompile_form.cleaned_data["pattern"]
        date = recompile_form.cleaned_data["date"]
        if pattern:
            id = pattern.id
        else:
            id = None
        compile(
            date=date,
            employees=employees,
            pattern=id,
            recompiled=True,
            request_device=request_device,
        )
    return redirect("attendance:recompile_view")


@login_required
@user_passes_test(lambda u: u.profile.role == "HR" or u.profile.role == "ADMIN")
def select_for_recompile(request):
    request_device = request.user.profile.device

    employees = Employee.objects.filter(
        status="Active", shift__isnull=False, device=request_device
    ).order_by("name")
    employee_filter = EmployeeFilter(request.GET, queryset=employees)
    employees = employee_filter.qs

    context = {
        "employees": employees,
        "employee_filter": employee_filter,
    }
    return render(request, "attendance/recompile/select.html", context)


@login_required
@user_passes_test(lambda u: u.profile.role == "HR" or u.profile.role == "ADMIN")
def save_recompile(request):
    save_recompiled(request)
    return redirect("attendance:recompile_view")


@login_required
@user_passes_test(lambda u: u.profile.role == "HR" or u.profile.role == "ADMIN")
def cancel_recompile(request):
    request_device = request.user.profile.device
    attendances = Attendance.objects.filter(
        recompiled=True, approved=False, deleted=False, device=request_device
    )

    for attendance in attendances:
        try:
            deleted_attendance = Attendance.objects.filter(
                check_in_date=attendance.check_in_date,
                employee=attendance.employee,
                deleted=True,
            )
            deleted_attendance.deleted = False
            deleted_attendance.save()
        except:
            pass
        attendance.delete()
    return redirect("attendance:recompile_view")
