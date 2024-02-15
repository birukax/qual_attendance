from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from openpyxl import Workbook
from .models import *
from django.core.paginator import Paginator
from .forms import AttendanceDownloadForm, SyncEmployeeAttendanceForm
from .filters import AttendanceDownloadFilter, AttendanceFilter
from device.forms import CreateDeviceForm
import threading

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
def attendance_list(request):
    attendances = Attendance.objects.all().order_by("-check_in_date", "-check_in_time")
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
def get_latest_attendance(request):
    attendance_object = Attendance()
    employees=Employee.objects.all().values('id')
    attendance_object.sync_attendance()
    
    return redirect("attendance:attendances")

@login_required
def sync_employee_attendance(request, id):
    attendance_object = Attendance()
    if request.method == "POST":
        attendance_form = SyncEmployeeAttendanceForm(request.POST)
        if attendance_form.is_valid():
            end_date = attendance_form.cleaned_data['end_date']
            attendance_object.sync_attendance(id=id,end_date=end_date)
            return redirect("employee:employee_detail", id=id )

@login_required
def download_attendance(request):
    form = AttendanceDownloadFilter(data=request.POST, queryset=Attendance.objects.all())
    attendances = form.qs
    response = HttpResponse(content_type="application/ms-excel")
    response["Content-Disposition"] = 'attachment; filename="attendance.xlsx"'
    wb = Workbook()
    ws = wb.active
    ws.title = "Attendance"

    headers = ["employee", "device", "current pattern", "leave type", "check in date", "check in time", "check out date", "check out time"]
    ws.append(headers)

    for attendance in attendances.order_by("-check_in_date"):
        
        if attendance.device: 
            device = attendance.device.name 
        else:
            device = ""
        if attendance.current_pattern:
            current_pattern = attendance.current_pattern.name
        else:
            current_pattern = ""
        if attendance.leave:
            leave = attendance.leave.name
        else:
            leave = ""
        ws.append(
            [
                attendance.employee.name,
                device,
                current_pattern,
                leave,
                attendance.check_in_date,
                attendance.check_in_time,
                attendance.check_out_date,
                attendance.check_out_time,
            ]
        )
    wb.save(response)
    return response

@login_required
def sync_attendance(request):
    attendance_object = RawAttendance()
    attendance_object.sync_raw_attendance()

    return redirect("attendance:attendances")

@login_required
def raw_attendance_list(request):
    # attendances = RawAttendance.objects.all().order_by("-date", "-time")[:1000]
    attendances = RawAttendance.objects.filter(date__gte=datetime(2024,1,1)).order_by("-date", "-time")
    paginated = Paginator(attendances, 15)
    page_number = request.GET.get("page")
    page = paginated.get_page(page_number)
    return render(
        request, "raw_attendance/list.html", {"page": page,}
    ) 
