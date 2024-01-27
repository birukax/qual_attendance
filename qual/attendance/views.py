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
from datetime import time
from .forms import CreateDeviceForm, AttendanceFilterForm, CreateShiftForm, ChangeEmployeeStatusForm
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
def employees(request):
    employees = (
        Employee.objects.all()
        .select_related()
        .order_by("employee_id")
        .order_by("-employee_id")
    )

    paginated = Paginator(employees, 15)
    page_number = request.GET.get("page")

    page = paginated.get_page(page_number)
    return render(
        request,
        "employee/employee_list.html",
        {"employees": employees, "page": page},
    )

@login_required
def sync_employee(request):
    employee_object = Employee()
    employee_object.sync_employee()
    return redirect("attendance:dashboard")

@login_required
def employee_detail(request, id):
    employee = get_object_or_404(Employee, id=id)
    attendances = Attendance.objects.filter(employee=employee).order_by('-check_in_date')
    paginated = Paginator(attendances, 15)
    change_status_form = ChangeEmployeeStatusForm(instance=employee, )
    page_number = request.GET.get("page")

    page = paginated.get_page(page_number)
    return render(
        request, "employee/employee_detail.html", {"employee": employee, "page": page, 'change_status_form':change_status_form}
    )

@login_required
def attendance_list(request):
    attendance_filter_form = AttendanceFilterForm()
    attendances = Attendance.objects.all().order_by("-check_in_date", "-check_in_time")
    paginated = Paginator(attendances, 15)
    page_number = request.GET.get("page")

    page = paginated.get_page(page_number)

    return render(
        request,
        "attendance/attendance_list.html",
        {"form": attendance_filter_form, "attendances": attendances, "page": page},
    )

@login_required
def get_latest_attendance(request):
    attendance_object = Attendance()
    attendance_object.sync_attendance()
    return redirect("attendance:attendances")

@login_required
def download_attendance(request):
    form = AttendanceFilterForm(data=request.POST)
    if form.is_valid():
        employee_id = form.cleaned_data["employee_id"]
        device_id = int(form.cleaned_data["device_id"])
        if employee_id != 0:
            employee_id = str(employee_id).rjust(4, "0")
        try:
            device = Device.objects.get(id=device_id)
        except:
            pass
        try:
            employee = Employee.objects.get(employee_id=employee_id)
        except:
            pass

        # date = form.cleaned_data["date"]
        # if date != None & employee_id != None & device_id != None:
        #     attendances = Attendance.object.filter(
        #         date=date, device_id=device_id, employee_id=employee_id
        #     )
        # elif date != None & employee_id != None:
        #     attendances = Attendance.object.filter(
        #         date=date, employee_id=employee_id
        #     )
        # elif date != None & device_id != None:
        #     attendances = Attendance.object.filter(date=date, device_id=device_id)

    # elif date != 0:
    #     attendances = Attendance.object.filter(date=date)
    if employee_id != 0 and device_id == 0:
        attendances = Attendance.objects.filter(employee=employee)
        print("employee not null")
        print(attendances)
    elif device_id != 0 and employee_id == 0:
        attendances = Attendance.objects.filter(device=device)
        print("device not null")
    elif employee_id == 0 and device_id == 0:
        attendances = Attendance.objects.all()
        print("both null.")
    else:
        print("both not null")
        attendances = Attendance.objects.filter(device=device, employee=employee)
    print(attendances)

    response = HttpResponse(content_type="application/ms-excel")
    response["Content-Disposition"] = 'attachment; filename="attendance.xlsx"'
    wb = Workbook()
    ws = wb.active
    ws.title = "Attendance"

    headers = ["name", "device", "date", "check in", "status", "punch"]
    ws.append(headers)

    for attendance in attendances.order_by("-date", "-check_in_time"):
        # if attendance.punch:
        #     punch = "IN"
        # else:
        #     punch = "OUT"
        ws.append(
            [
                attendance.employee.name,
                attendance.device.name,
                attendance.date,
                attendance.time,
                attendance.status,
                attendance.punch,
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

    return redirect("attendance:dashboard")

@login_required
def raw_attendance(request):
    attendances = RawAttendance.objects.all().order_by("-date", "-time")[:1000]
    return render(
        request, "raw_attendance/raw_attendance.html", {"attendances": attendances}
    ) 

@login_required
def devices(request):
    devices = Device.objects.all()
    create_device_form = CreateDeviceForm()
    return render(
        request,
        "device/device_list.html",
        {"devices": devices, "form": create_device_form},
    )

@login_required
def create_device(request):
    if request.method == "POST":
        form = CreateDeviceForm(data=request.POST)
        if form.is_valid():
            name = form.cleaned_data["name"]
            ip = form.cleaned_data["ip"]
            slug = slugify(name)
            Device.objects.create(name=name, ip=ip, slug=slug)

    return redirect("attendance:dashboard")

@login_required
def shifts(request):
    create_shift_form = CreateShiftForm(data=request.GET)
    shifts = Shift.objects.all()
    paginated = Paginator(shifts, 15)
    page_number = request.GET.get("page")
    
    page = paginated.get_page(page_number)
    return render(
        request, "shift/shift_list.html", {"form": create_shift_form, "shifts": shifts, "page": page}   
    )

@login_required
def shift_detail(request, id):
    shift = get_object_or_404(Shift, id=id)
    patterns = Pattern.objects.filter(shift=shift)
    employees = Employee.objects.filter(shift=shift)
    paginated = Paginator(employees, 15)
    page_number = request.GET.get("page")

    page = paginated.get_page(page_number)
    return render(
        request, "shift/shift_detail.html", {"shift": shift, "page": page, 'patterns':patterns}
    )

@login_required
def create_shift(request):
    if request.method == "POST":
        form = CreateShiftForm(data=request.POST)
        if form.is_valid():
            name = form.cleaned_data["name"]
            tolerance = form.cleaned_data["tolerance"]
            day_span = form.cleaned_data["day_span"]
            start_time = form.cleaned_data["start_time"]
            end_time = form.cleaned_data["end_time"]
            # previous_shift = form.cleaned_data["previous_shift"]
            # next_shift = form.cleaned_data["next_shift"]
            shft, created = Shift.objects.get_or_create(
                name=name,
                tolerance=tolerance,
                day_span=day_span,
                start_time=start_time,
                end_time=end_time,
            )
            return redirect("attendance:shifts")
