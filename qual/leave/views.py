from tracemalloc import start
from django.forms import ValidationError
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Leave, LeaveType
from .forms import (
    CreateLeaveForm,
    CreateLeaveTypeForm,
    EditLeaveTypeForm,
    ALCalculateDateForm,
)
from django.core.paginator import Paginator
from django.http import HttpResponse
from .tasks import calculate_annual_leaves, calculate_total_leave_days
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from employee.models import Employee
from employee.filters import EmployeeFilter
from .filters import AnnualLeaveDownloadFilter, LeaveDownloadFilter, LeaveFilter
from openpyxl import Workbook
import datetime


@login_required
def leaves(request):
    context = {}
    user = request.user.profile
    if user.role == "ADMIN" or user.role == "HR":
        leaves = Leave.objects.all().order_by("-start_date")
    else:
        leaves = Leave.objects.filter(
            employee__department__in=user.manages.all()
        ).order_by("-start_date")
    for l in leaves:
        calculate_total_leave_days(l.id)
    leave_filter = LeaveFilter(request.GET, queryset=leaves)
    leaves = leave_filter.qs

    paginated = Paginator(leaves, 30)
    page_number = request.GET.get("page")
    page = paginated.get_page(page_number)
    context["page"] = page
    context["leave_filter"] = leave_filter

    return render(request, "leave/list.html", context)


@login_required
def leave_detail(request, id):
    leave = get_object_or_404(Leave, id=id)
    calculate_total_leave_days(leave.id)

    if not (request.user.profile.role == "HR" or request.user.profile.role == "ADMIN"):
        if leave.employee.department not in request.user.profile.manages.all():
            return redirect("leave:leaves")
    return render(request, "leave/detail.html", {"leave": leave})


@login_required
def create_leave(request):
    if request.method == "POST":
        form = CreateLeaveForm(request.POST, user=request.user)
        if form.is_valid():
            form.save()
            return redirect("leave:leaves")
        # return redirect("leave:leaves")
    else:
        form = CreateLeaveForm(request.GET, user=request.user)
    return render(request, "leave/create.html", {"form": form})
    # return redirect("leave:create_leave")


@login_required
def cancel_leave(request, id):
    leave = Leave.objects.get(id=id)
    if leave.approved == False:
        leave.rejected = True
        leave.rejected_by = request.user
        leave.save()
    return redirect("leave:leave_detail", id=id)


@login_required
def edit_leave(request, id):
    return render(request, "leave/edit.html")


@login_required
@user_passes_test(lambda u: u.profile.role == "ADMIN" or u.profile.role == "HR")
def annual_leave_list(request):
    # request_device = request.user.profile.device
    # if request_device:
    #     employees = Employee.objects.filter(device=request_device).order_by("name")
    # else:
    employees = Employee.objects.filter(status="Active").order_by("name")
    download_filter = AnnualLeaveDownloadFilter(queryset=employees)
    employee_filter = EmployeeFilter(request.GET, queryset=employees)
    employees = employee_filter.qs
    paginated = Paginator(employees, 30)
    page_number = request.GET.get("page")
    calculate_date_form = ALCalculateDateForm()
    page = paginated.get_page(page_number)
    context = {
        "page": page,
        "employee_filter": employee_filter,
        "download_filter": download_filter,
        "form": calculate_date_form,
    }
    return render(request, "leave/annual_leave/list.html", context)


@login_required
@user_passes_test(lambda u: u.profile.role == "ADMIN" or u.profile.role == "HR")
def calculate_leave_balance(request):
    date = datetime.date.today()
    if request.method == "POST":
        form = ALCalculateDateForm(request.POST)
        if form.is_valid():
            date = form.cleaned_data["date"]
    print(date)
    print("calculating")
    calculate_annual_leaves(end_date=date)
    return redirect("leave:annual_leaves")


@login_required
def download_annual_leave(request):
    user = request.user.profile
    if user.role == "HR" or user.role == "ADMIN":
        employees = Employee.objects.all().order_by("name")
    else:
        employees = Employee.objects.filter(department__in=user.manages.all()).order_by(
            "name"
        )
    form = AnnualLeaveDownloadFilter(
        data=request.POST,
        queryset=employees,
    )
    employees = form.qs
    response = HttpResponse(content_type="application/ms-excel")
    response["Content-Disposition"] = 'attachment; filename="annual_leave.xlsx"'
    wb = Workbook()
    ws = wb.active
    ws.title = "annual leave"

    headers = [
        "ID",
        "Name",
        "Department",
        "Employment date",
        "Last calculated",
        "Total",
        "Taken",
        # "Difference",
        "remaining",
    ]
    ws.append(headers)

    for employee in employees:

        ws.append(
            [
                employee.employee_id,
                employee.name,
                employee.department.name,
                employee.employment_date,
                employee.calculate_date,
                employee.annual_leave_balance,
                employee.annual_leave_taken,
                # employee.annual_leave_difference,
                employee.annual_leave_remaining,
            ]
        )
    wb.save(response)
    return response


@login_required
@user_passes_test(lambda u: u.profile.role == "ADMIN" or u.profile.role == "HR")
def leave_type_list(request):
    leave_types = LeaveType.objects.all().order_by("name")
    create_leave_type_form = CreateLeaveTypeForm()
    paginated = Paginator(leave_types, 30)
    page_number = request.GET.get("page")
    page = paginated.get_page(page_number)
    return render(
        request,
        "leave/leave_type/list.html",
        {"page": page, "create_leave_type_form": create_leave_type_form},
    )


@login_required
@user_passes_test(lambda u: u.profile.role == "ADMIN" or u.profile.role == "HR")
def leave_type_detail(request, id):
    leave_type = LeaveType.objects.get(id=id)
    edit_leave_type_form = EditLeaveTypeForm(instance=leave_type)
    leaves = Leave.objects.filter(leave_type=leave_type).order_by("start_date")
    paginated = Paginator(leaves, 30)
    page_number = request.GET.get("page")

    page = paginated.get_page(page_number)
    context = {
        "leave_type": leave_type,
        "edit_leave_type_form": edit_leave_type_form,
        "page": page,
    }
    return render(request, "leave/leave_type/detail.html", context)


@login_required
@user_passes_test(lambda u: u.profile.role == "ADMIN" or u.profile.role == "HR")
def create_leave_type(request):
    form = CreateLeaveTypeForm(request.POST)
    if form.is_valid():
        name = form.cleaned_data["name"]
        description = form.cleaned_data["description"]
        maximum_days = form.cleaned_data["maximum_days"]
        paid = form.cleaned_data["paid"]
        exclude_rest_days = form.cleaned_data["exclude_rest_days"]

        leave_type = LeaveType(
            name=name,
            description=description,
            maximum_days=maximum_days,
            paid=paid,
            exclude_rest_days=exclude_rest_days,
        )
        leave_type.save()
    return redirect("leave:leave_types")


@login_required
@user_passes_test(lambda u: u.profile.role == "ADMIN" or u.profile.role == "HR")
def edit_leave_type(request, id):
    form = EditLeaveTypeForm(request.POST)
    leave_type = LeaveType.objects.get(id=id)
    if form.is_valid():
        leave_type.name = form.cleaned_data["name"]
        leave_type.description = form.cleaned_data["description"]
        leave_type.maximum_days = form.cleaned_data["maximum_days"]
        leave_type.paid = form.cleaned_data["paid"]
        leave_type.annual = form.cleaned_data["annual"]
        leave_type.exclude_rest_days = form.cleaned_data["exclude_rest_days"]
        leave_type.save()
    return redirect("leave:leave_type_detail", id=id)


@login_required
def download_evidence(request, evidence):
    uploaded_file = Leave.objects.get(evicence=evidence)
    response = HttpResponse(
        uploaded_file.file, content_type="application/force-download"
    )
    response["Content-Disposition"] = (
        f'attachment; filename="{uploaded_file.file.name}"'
    )
    return response
