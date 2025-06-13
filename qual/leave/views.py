from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Leave, LeaveType
from .forms import (
    CreateLeaveForm,
    EditLeaveForm,
    CreateLeaveTypeForm,
    EditLeaveTypeForm,
    ALCalculateDateForm,
)
from django.core.paginator import Paginator
from django.http import HttpResponse
from .tasks import calculate_annual_leaves, calculate_total_leave_days
from django.contrib.auth.decorators import user_passes_test
from employee.models import Employee
from attendance.models import Attendance
from employee.filters import EmployeeFilter
from .filters import AnnualLeaveDownloadFilter, LeaveFilter
from openpyxl import Workbook
import datetime


@login_required
def leaves(request):
    context = {}
    user = request.user.profile
    # if user.role == "ADMIN" or user.role == "HR":
    leaves = Leave.objects.select_related("employee", "leave_type").all()
    # else:
    #     leaves = Leave.objects..select_related('employee', 'leave_type','approved_by','rejected_by').filter(
    #         employee__department__in=user.manages.all()
    #     ).order_by("-start_date")
    # for l in leaves:
    #     # if l.employee.shift:
    #     # l.saturday_half = l.employee.shift.saturday_half
    #     # l.save()
    #     calculate_total_leave_days(l.id)
    leave_filter = LeaveFilter(request.GET, queryset=leaves)
    # download_filter = LeaveDownloadFilter(queryset=leaves)
    leaves = leave_filter.qs

    paginated = Paginator(leaves, 30)
    page_number = request.GET.get("page")
    page = paginated.get_page(page_number)
    context["page"] = page
    context["leave_filter"] = leave_filter
    # context["download_filter"] = download_filter
    return render(request, "leave/list.html", context)


@login_required
def leave_detail(request, id):
    calculate_total_leave_days(id)
    leave = get_object_or_404(Leave, id=id)
    if not (request.user.profile.role == "HR" or request.user.profile.role == "ADMIN"):
        if leave.employee.department not in request.user.profile.manages.all():
            return redirect("leave:leaves")
    return render(request, "leave/detail.html", {"leave": leave})


@login_required
def download_leave(request):
    user = request.user.profile
    if user.role == "HR" or user.role == "ADMIN":
        leaves = Leave.objects.all().order_by("start_date")
    else:
        leaves = Leave.objects.filter(department__in=user.manages.all()).order_by(
            "start_date"
        )
    form = LeaveFilter(
        data=request.POST,
        queryset=leaves,
    )
    leaves = form.qs
    response = HttpResponse(content_type="application/ms-excel")
    response["Content-Disposition"] = 'attachment; filename="leave.xlsx"'
    wb = Workbook()
    ws = wb.active
    ws.title = "leave"

    headers = [
        "ID",
        "Name",
        "Department",
        "Device",
        "Employment date",
        "Leave Type",
        "Start date",
        "End date",
        "Half day",
        "Total days",
        "Status",
        "Approved by",
        "Rejected by",
    ]
    ws.append(headers)

    for leave in leaves:
        if leave.approved:
            status = "Approved"
        elif leave.rejected:
            status = "Rejected"
        else:
            status = "Pending"
        if leave.approved_by:
            approved_by = leave.approved_by.username
        else:
            approved_by = ""
        if leave.rejected_by:
            rejected_by = leave.rejected_by.username
        else:
            rejected_by = ""
        if leave.employee.device:
            device_name = leave.employee.device.name
        else:
            device_name = ""
        ws.append(
            [
                leave.employee.employee_id,
                leave.employee.name,
                leave.employee.department.name,
                device_name,
                leave.employee.employment_date,
                leave.leave_type.name,
                leave.start_date,
                leave.end_date,
                leave.half_day,
                leave.total_days,
                status,
                approved_by,
                rejected_by,
            ]
        )
    wb.save(response)
    return response


@login_required
def create_leave(request):
    if request.method == "POST":
        form = CreateLeaveForm(request.POST, user=request.user)
        if form.is_valid():
            employee = form.cleaned_data["employee"]
            leave_type = form.cleaned_data["leave_type"]
            start_date = form.cleaned_data["start_date"]
            end_date = form.cleaned_data["end_date"]
            half_day = form.cleaned_data["half_day"]
            reason = form.cleaned_data["reason"]
            if employee.shift:
                saturday_half = employee.shift.saturday_half
            else:
                saturday_half = False
            leave = Leave(
                employee=employee,
                leave_type=leave_type,
                start_date=start_date,
                end_date=end_date,
                half_day=half_day,
                reason=reason,
                saturday_half=saturday_half,
            )
            leave.save()
            calculate_total_leave_days(leave.id)
            return redirect("leave:leaves")
        # return redirect("leave:leaves")
    else:
        form = CreateLeaveForm(request.GET, user=request.user)
    return render(request, "leave/create.html", {"form": form})
    # return redirect("leave:create_leave")


@login_required
def cancel_leave(request, id):
    leave = get_object_or_404(Leave, id=id)
    if leave.approved == False:
        leave.rejected = True
        leave.rejected_by = request.user
        leave.save()
    return redirect("leave:leave_detail", id=id)


@login_required
@user_passes_test(lambda u: u.has_perm("account.can_approve"))
def reopen_leave(request, id):
    leave = get_object_or_404(Leave, id=id)
    attendances = Attendance.objects.filter(
        employee=leave.employee,
        check_in_date__gte=leave.start_date,
        check_in_date__lte=leave.end_date,
        status="On Leave",
    )
    if leave.rejected:
        leave.rejected = False
        leave.rejected_by = None
        leave.save()
    elif leave.approved:
        leave.approved = False
        leave.approved_by = None
        leave.save()
    if attendances:
        for attendance in attendances:
            attendance.status = "Absent"
            attendance.save()
    return redirect("leave:leave_detail", id=id)


@login_required
def edit_leave(request, id):
    leave = get_object_or_404(Leave, id=id)
    if not leave.approved:
        if request.method == "POST":
            form = EditLeaveForm(data=request.POST, instance=leave)
            if form.is_valid():
                employee = form.cleaned_data["employee"]
                leave.leave_type = form.cleaned_data["leave_type"]
                leave.start_date = form.cleaned_data["start_date"]
                leave.end_date = form.cleaned_data["end_date"]
                leave.half_day = form.cleaned_data["half_day"]
                leave.reason = form.cleaned_data["reason"]
                if employee.shift:
                    saturday_half = employee.shift.saturday_half
                else:
                    saturday_half = False
                leave.saturday_half = saturday_half
                leave.rejected = False
                leave.save()
                return redirect("leave:leave_detail", id=id)
        else:
            form = EditLeaveForm(instance=leave)
        context = {"form": form, "leave": leave}
        return render(request, "leave/edit.html", context)

    return redirect("leave:leave_detail", id=id)


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
        half_day_leave = form.cleaned_data["half_day_leave"]

        leave_type = LeaveType(
            name=name,
            description=description,
            maximum_days=maximum_days,
            paid=paid,
            exclude_rest_days=exclude_rest_days,
            half_day_leave=half_day_leave,
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
        leave_type.half_day_leave = form.cleaned_data["half_day_leave"]
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
