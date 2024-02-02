from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Employee
from django.core.paginator import Paginator
from shift.forms import ChangeEmployeeShiftForm, ChangeEmployeePatternForm
from attendance.forms import SyncEmployeeAttendanceForm
from django.utils.text import slugify
from django.contrib.postgres.search import SearchVector
import threading
from attendance.models import Attendance




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
    return redirect("employee:employees")

@login_required
def employee_detail(request, id):
    employee = get_object_or_404(Employee, id=id)
    attendances = Attendance.objects.filter(employee=employee).order_by('-check_in_date')
    paginated = Paginator(attendances, 15)
    change_shift_form = ChangeEmployeeShiftForm(instance=employee, )
    change_pattern_form = ChangeEmployeePatternForm(instance=employee,)
    sync_employee_attendance_form = SyncEmployeeAttendanceForm()
    page_number = request.GET.get("page")
    page = paginated.get_page(page_number)
    return render(
        request, "employee/employee_detail.html", {"employee": employee, "page": page, 'change_shift_form':change_shift_form, 'change_pattern_form':change_pattern_form, 'sync_employee_attendance_form':sync_employee_attendance_form}
    )