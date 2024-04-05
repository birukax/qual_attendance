from multiprocessing import context
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Employee
from django.core.paginator import Paginator
from shift.forms import ChangeEmployeeShiftForm
from attendance.models import Attendance
from leave.models import Leave
from overtime.models import Overtime
from .filters import *
from device.forms import AddDeviceUserForm
from device.models import DeviceUser, Device


@login_required
def employees(request):
    nav = "employee"
    if request.user.profile.role == "MANAGER":
        employees = Employee.objects.filter(
            department__in=request.user.profile.manages.all()
        )
    else:
        employees = Employee.objects.all().order_by("-employee_id")
    employee_filter = EmployeeFilter(request.GET, queryset=employees)
    employees = employee_filter.qs

    paginated = Paginator(employees, 10)
    page_number = request.GET.get("page")

    page = paginated.get_page(page_number)
    context = {"page": page, "employee_filter": employee_filter, "nav": nav}
    return render(
        request,
        "employee/list.html",
        context,
    )


@login_required
def sync_employee(request):
    department_object = Department()
    department_object.sync_department()
    employee_object = Employee()
    employee_object.sync_employee()
    return redirect("employee:employees")


# @login_required
# def update_salary(request):
#     salary_object = Salary()
#     salary_object.update_salary()
#     return redirect("employee:employees")


@login_required
def employee_detail(request, id):
    employee = get_object_or_404(
        Employee,
        id=id,
    )
    employee_devices = DeviceUser.objects.filter(employee=employee)
    add_device_user_form = AddDeviceUserForm()
    attendances = Attendance.objects.filter(employee=employee, approved=True).order_by(
        "-check_in_date"
    )
    paginated = Paginator(attendances, 10)
    change_shift_form = ChangeEmployeeShiftForm(
        instance=employee,
    )

    page_number = request.GET.get("page")
    page = paginated.get_page(page_number)
    return render(
        request,
        "employee/detail.html",
        {
            "employee": employee,
            "page": page,
            "employee_devices": employee_devices,
            "change_shift_form": change_shift_form,
            "add_device_user_form": add_device_user_form,
        },
    )


@login_required
def employee_attendances(request, id):
    employee = get_object_or_404(
        Employee,
        id=id,
    )
    attendances = Attendance.objects.filter(employee=employee, approved=True).order_by(
        "-check_in_date"
    )
    paginated = Paginator(attendances, 10)
    page_number = request.GET.get("page")

    page = paginated.get_page(page_number)
    context = {"page": page, "employee": employee}
    return render(request, "employee/attendance/list.html", context)


@login_required
def employee_leaves(request, id):
    employee = get_object_or_404(
        Employee,
        id=id,
    )
    leaves = Leave.objects.filter(employee=employee).order_by("-start_date")
    paginated = Paginator(leaves, 10)
    page_number = request.GET.get("page")
    page = paginated.get_page(page_number)
    context = {"page": page, "employee": employee}
    return render(request, "employee/leave/list.html", context)


@login_required
def employee_overtimes(request, id):
    employee = get_object_or_404(
        Employee,
        id=id,
    )
    overtimes = Overtime.objects.filter(employee=employee).order_by("-start_date")
    paginated = Paginator(overtimes, 10)
    page_number = request.GET.get("page")
    page = paginated.get_page(page_number)
    context = {"page": page, "employee": employee}
    return render(request, "employee/overtime/list.html", context)


# @login_required
# def sync_department(request):
#     return redirect("employee:employees")


@login_required
def departments(request):
    nav = "employee"

    departments = Department.objects.all().order_by("code")

    paginated = Paginator(departments, 10)
    page_number = request.GET.get("page")

    page = paginated.get_page(page_number)
    context = {"departments": departments, "page": page, "nav": nav}
    return render(request, "department/list.html", context)
