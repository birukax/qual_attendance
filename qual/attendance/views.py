from ast import And
from asyncio.windows_events import NULL
from traceback import format_list
from tracemalloc import start
from turtle import back
from django import forms
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from zk import ZK
from django.http import HttpResponse
from openpyxl import Workbook
from .models import Device, Employee, RawAttendance, Attendance, Shift, Pattern
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
import datetime
from datetime import time, date
from .forms import AttendanceDownloadForm, SyncEmployeeAttendanceForm
from .filters import AttendanceDownloadFilter, AttendanceFilter
from device.forms import CreateDeviceForm
from django.utils.text import slugify
from django.contrib.postgres.search import SearchVector
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
    paginated = Paginator(attendances, 15)
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
        "attendance/attendance_list.html", context,
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
            return redirect("employee:employee_detail", id=id, )

@login_required
def download_attendance(request):
    form = AttendanceDownloadFilter(data=request.POST, queryset=Attendance.objects.all())
    attendances = form.qs
    response = HttpResponse(content_type="application/ms-excel")
    response["Content-Disposition"] = 'attachment; filename="attendance.xlsx"'
    wb = Workbook()
    ws = wb.active
    ws.title = "Attendance"

    headers = ["employee", "device", "check in date", "check in time", "check out date", "check out time"]
    ws.append(headers)

    for attendance in attendances.order_by("-check_in_date"):
        ws.append(
            [
                attendance.employee.name,
                attendance.device.name,
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
    # attendance = Attendance()
    # attendance.sync_a()

    return redirect("attendance:attendances")

@login_required
def raw_attendance(request):
    attendances = RawAttendance.objects.all().order_by("-date", "-time")[:1000]
    return render(
        request, "raw_attendance/raw_attendance.html", {"attendances": attendances}
    ) 
