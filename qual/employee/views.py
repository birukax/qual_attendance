from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Employee, Department
from django.core.paginator import Paginator
from .forms import ChangeEmployeeShiftForm
from attendance.models import Attendance
from leave.models import Leave
from overtime.models import Overtime
from .filters import EmployeeFilter
from device.forms import AddDeviceUserForm
from device.models import DeviceUser, Device
from django.contrib.auth.decorators import user_passes_test
from .tasks import department_get, employee_get


@login_required
def employees(request):
    if request.GET.get("employees"):
        employees = request.GET.get("employees")
    if request.user.profile.role == "HR" or request.user.profile.role == "ADMIN":
        employees = Employee.objects.all().order_by("-employee_id")
    else:
        employees = Employee.objects.filter(
            department__in=request.user.profile.manages.all()
        ).order_by("-employee_id")
    employee_filter = EmployeeFilter(request.GET, queryset=employees)
    employees = employee_filter.qs
    paginated = Paginator(employees, 30)
    page_number = request.GET.get("page")
    page = paginated.get_page(page_number)
    context = {
        "page": page,
        "filter": employee_filter,
    }
    return render(
        request,
        "employee/list.html",
        context,
    )


@login_required
@user_passes_test(lambda u: u.profile.role == "ADMIN" or u.profile.role == "HR")
def sync_employee(request):
    department_get()
    employee_get()
    return redirect("employee:employees")


@login_required
@user_passes_test(lambda u: u.profile.role != "USER")
def employee_detail(request, id):
    employee = get_object_or_404(Employee, id=id)
    if not (request.user.profile.role == "HR" or request.user.profile.role == "ADMIN"):
        if employee.department not in request.user.profile.manages.all():
            return redirect("employee:employees")
    change_shift_form = ChangeEmployeeShiftForm(instance=employee)
    employee_devices = DeviceUser.objects.filter(employee=employee)
    add_device_user_form = AddDeviceUserForm()
    attendances = Attendance.objects.filter(employee=employee, approved=True).order_by(
        "-check_in_date"
    )
    paginated = Paginator(attendances, 30)
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
@user_passes_test(lambda u: u.profile.role != "USER")
def employee_attendances(request, id):
    employee = get_object_or_404(
        Employee,
        id=id,
    )
    if not (request.user.profile.role == "HR" or request.user.profile.role == "ADMIN"):
        if employee.department not in request.user.profile.manages.all():
            return redirect("employee:employees")
    attendances = Attendance.objects.filter(employee=employee, approved=True).order_by(
        "-check_in_date"
    )
    paginated = Paginator(attendances, 30)
    page_number = request.GET.get("page")

    page = paginated.get_page(page_number)
    context = {"page": page, "employee": employee}
    return render(request, "employee/attendance/list.html", context)


@login_required
@user_passes_test(lambda u: u.profile.role != "USER")
def employee_leaves(request, id):
    employee = get_object_or_404(
        Employee,
        id=id,
    )
    if not (request.user.profile.role == "HR" or request.user.profile.role == "ADMIN"):
        if employee.department not in request.user.profile.manages.all():
            return redirect("employee:employees")
    leaves = Leave.objects.filter(employee=employee).order_by("-start_date")
    paginated = Paginator(leaves, 30)
    page_number = request.GET.get("page")
    page = paginated.get_page(page_number)
    context = {"page": page, "employee": employee}
    return render(request, "employee/leave/list.html", context)


@login_required
@user_passes_test(lambda u: u.profile.role != "USER")
def employee_overtimes(request, id):
    employee = get_object_or_404(
        Employee,
        id=id,
    )
    if not (request.user.profile.role == "HR" or request.user.profile.role == "ADMIN"):
        if employee.department not in request.user.profile.manages.all():
            return redirect("employee:employees")
    overtimes = Overtime.objects.filter(employee=employee).order_by("-start_date")
    paginated = Paginator(overtimes, 30)
    page_number = request.GET.get("page")
    page = paginated.get_page(page_number)
    context = {"page": page, "employee": employee}
    return render(request, "employee/overtime/list.html", context)


@login_required
@user_passes_test(lambda u: u.profile.role == "ADMIN" or u.profile.role == "HR")
def departments(request):
    departments = Department.objects.all().order_by("code")
    paginated = Paginator(departments, 30)
    page_number = request.GET.get("page")
    page = paginated.get_page(page_number)
    context = {
        "departments": departments,
        "page": page,
    }
    return render(request, "department/list.html", context)
