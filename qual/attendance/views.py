from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from openpyxl import Workbook
from .models import *
from django.core.paginator import Paginator
from .forms import AttendanceDownloadForm, SyncEmployeeAttendanceForm
from .filters import *
from device.forms import CreateDeviceForm
from .compiler import compile, save_data
import threading
import datetime

@login_required
def dashboard(request):
    attendances = Attendance.objects.all()
    employees = Employee.objects.all()
    devices = Device.objects.all()
    create_device_form = CreateDeviceForm()
    return render(
        request,
        "dashboard.html",
        {
            "attendances": attendances,
            "employees": employees,
            "devices": devices,
            "form": create_device_form,
        },
    )

@login_required
def compile_view(request):
    attendances = Attendance.objects.filter(approved=False).order_by("-check_in_time")
    daily_records = DailyRecord.objects.latest('date')
    no_shift = Employee.objects.filter(shift=None, status='active').count()
    no_pattern = Employee.objects.filter(pattern=None, status='active').count()
    context = {
        "attendances": attendances, 
        'daily_records': daily_records, 
        'no_shift': no_shift, 
        'no_pattern': no_pattern, 
        }
    return render(request, "attendance/compile.html", context  )

@login_required
def compile_attendance(request):
    daily_record = DailyRecord.objects.all()
    if daily_record:
        date = daily_record.latest('date').date + datetime.timedelta(days=1)
    else:
        date = datetime.date.today() - datetime.timedelta(days=1)
    compile(date=date)
    return redirect("attendance:compile_view")

@login_required
def save_compiled_attendance(request):
    daily_record = DailyRecord.objects.all()
    if daily_record:
        date = daily_record.latest('date').date + datetime.timedelta(days=1)
    else:
        date = datetime.date.today() - datetime.timedelta(days=1)
    save_data(date)
    return redirect("attendance:compile_view")


@login_required
def attendance_list(request):
    attendances = Attendance.objects.filter(approved=True).order_by("-check_in_date", "-check_in_time")
    attendance_download_filter = AttendanceDownloadFilter(request.GET, queryset=Attendance.objects.all())
    attendance_filter = AttendanceFilter(request.GET, queryset=attendances)
    attendances = attendance_filter.qs
    paginated = Paginator(attendances, 10)
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
        "attendance/list.html", context,
    )

@login_required
def download_attendance(request):
    form = AttendanceDownloadFilter(data=request.POST, queryset=Attendance.objects.filter(approved=True))
    attendances = form.qs
    response = HttpResponse(content_type="application/ms-excel")
    response["Content-Disposition"] = 'attachment; filename="attendance.xlsx"'
    wb = Workbook()
    ws = wb.active
    ws.title = "Attendance"

    headers = ["employee", "device", "current pattern", "worked_hours", "check in date", "check in time", "check out date", "check out time", "Check in type", "Check out type", "status", "Leave type"]
    ws.append(headers)

    for attendance in attendances.order_by("-check_in_date"):
        
        if attendance.device: 
            device = attendance.device.name 
        else:
            device = ""
        
        ws.append(
            [
                attendance.employee.name,
                device,
                attendance.current_pattern.name,
                attendance.worked_hours,
                attendance.check_in_date,
                attendance.check_in_time,
                attendance.check_out_date,
                attendance.check_out_time,
                attendance.check_in_type,
                attendance.check_out_type,
                attendance.status,
                attendance.leave_type,
            ]
        )
    wb.save(response)
    return response

@login_required
def get_raw_data(request):
    attendance_object = RawAttendance()
    attendance_object.sync_raw_attendance()

    return redirect("attendance:raw_attendance")

@login_required
def raw_attendance_list(request):
    # attendances = RawAttendance.objects.all().order_by("-date", "-time")[:1000]
    attendances = RawAttendance.objects.filter(date__gte=datetime.date(2024,1,1)).order_by("-date", "-time")
    attendance_filter = RawAttendanceFilter(request.GET, queryset=attendances)
    attendances = attendance_filter.qs
    paginated = Paginator(attendances, 10)
    page_number = request.GET.get("page")
    page = paginated.get_page(page_number)
    
    context = {
        'raw_attendance_filter': attendance_filter,
        'page': page
    }
    return render(
        request, "raw_attendance/list.html", context
    ) 
