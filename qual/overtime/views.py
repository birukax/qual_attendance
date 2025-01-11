from datetime import datetime
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
import requests
from requests_ntlm import HttpNtlmAuth
from .models import Overtime, Ot, OvertimeType
from django.core.paginator import Paginator
from .forms import CreateOvertimeForm, EditOvertimeTypeForm, CreateOvertimeTypeForm
from .tasks import calculate_ot, post_ot
from urllib.parse import quote
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from .filters import OvertimeDownloadFilter, OvertimeFilter
from openpyxl import Workbook
from django.http import HttpResponse


@login_required
def overtimes(request):
    user = request.user.profile
    create_overtime_form = CreateOvertimeForm(user=request.user)
    if user.role == "HR" or user.role == "ADMIN":
        overtimes = Overtime.objects.all().order_by("-start_date")
    else:
        overtimes = Overtime.objects.filter(
            employee__department__in=user.manages.all()
        ).order_by("-start_date")
    overtime_filter = OvertimeFilter(request.GET, queryset=overtimes)
    download_filter = OvertimeDownloadFilter(queryset=overtimes)
    overtimes = overtime_filter.qs
    paginated = Paginator(overtimes, 30)
    page_number = request.GET.get("page")

    page = paginated.get_page(page_number)
    context = {
        "page": page,
        "create_overtime_form": create_overtime_form,
        "download_filter": download_filter,
        "overtime_filter": overtime_filter,
    }
    return render(request, "overtime/list.html", context)


@login_required
def overtime_detail(request, id):
    overtime = get_object_or_404(Overtime, id=id)
    if not (request.user.profile.role == "HR" or request.user.profile.role == "ADMIN"):
        if overtime.employee.department not in request.user.profile.manages.all():
            return redirect("overtime:overtimes")
    context = {"overtime": overtime}
    return render(request, "overtime/detail.html", context)


@login_required
def create_overtime(request):
    if request.method == "POST":
        form = CreateOvertimeForm(request.POST, user=request.user)
        if form.is_valid():
            form.save()
            return redirect("overtime:overtimes")
    else:
        form = CreateOvertimeForm(request.GET, user=request.user)
    return render(request, "overtime/create.html", {"form": form})


@login_required
def download_overtime(request):
    user = request.user.profile
    if user.role == "HR" or user.role == "ADMIN":
        overtimes = Overtime.objects.all().order_by("start_date")
    else:
        overtimes = Overtime.objects.filter(department__in=user.manages.all()).order_by(
            "name"
        )
    form = OvertimeDownloadFilter(
        data=request.POST,
        queryset=overtimes,
    )
    overtimes = form.qs
    response = HttpResponse(content_type="application/ms-excel")
    response["Content-Disposition"] = 'attachment; filename="overtimes.xlsx"'
    wb = Workbook()
    ws = wb.active
    ws.title = "annual leave"

    headers = [
        "Employee name",
        "Start date",
        "Start time" "End date",
        "End time",
        "Total hours",
        "Approved",
        "Rejected",
        "paid",
        "Approved by",
    ]
    ws.append(headers)

    for overtime in overtimes:

        ws.append(
            [
                overtime.employee.name,
                overtime.start_date,
                overtime.start_time,
                overtime.end_date,
                overtime.start_time,
                overtime.worked_hours,
                overtime.approved,
                overtime.rejected,
                overtime.paid,
                overtime.approved_by.first_name,
            ]
        )
    wb.save(response)
    return response


@login_required
def edit_overtime(request, id):
    pass


@login_required
@user_passes_test(lambda u: u.profile.role == "ADMIN")
def overtime_types(request):
    crate_overtime_type_form = CreateOvertimeTypeForm()
    overtime_types = OvertimeType.objects.all().order_by("name")
    paginated = Paginator(overtime_types, 30)
    page_number = request.GET.get("page")

    page = paginated.get_page(page_number)
    context = {"page": page, "create_ot_type_form": crate_overtime_type_form}
    return render(request, "overtime/overtime_type/list.html", context)


@login_required
@user_passes_test(lambda u: u.profile.role == "ADMIN")
def overtime_type_detail(request, id):
    overtime_type = get_object_or_404(OvertimeType, id=id)
    edit_overtime_type_form = EditOvertimeTypeForm(instance=overtime_type)
    overtimes = Ot.objects.filter(overtime_type=overtime_type)
    days = overtime_type.days.all()
    paginated = Paginator(overtimes, 30)
    page_number = request.GET.get("page")
    page = paginated.get_page(page_number)

    context = {
        "overtime_type": overtime_type,
        "page": page,
        "edit_ot_type_form": edit_overtime_type_form,
        "days": days,
    }
    return render(request, "overtime/overtime_type/detail.html", context)


@login_required
@user_passes_test(lambda u: u.profile.role == "ADMIN")
def create_overtime_type(request):
    if request.method == "POST":
        create_ot_type_form = CreateOvertimeTypeForm(request.POST)
        if create_ot_type_form.is_valid():
            create_ot_type_form.save()
            return redirect("overtime:overtime_types")


@login_required
@user_passes_test(lambda u: u.profile.role == "ADMIN")
def edit_overtime_type(request, id):
    overtime_type = get_object_or_404(OvertimeType, id=id)
    if request.method == "POST":
        edit_ot_type_form = EditOvertimeTypeForm(request.POST, instance=overtime_type)
        if edit_ot_type_form.is_valid():
            edit_ot_type_form.save()
    return redirect("overtime:overtime_type_detail", id=id)


@login_required
@user_passes_test(lambda u: u.profile.role == "ADMIN" or u.profile.role == "HR")
def ots(request):
    ots = Ot.objects.all().order_by("-start_date")
    paginated = Paginator(ots, 30)
    page_number = request.GET.get("page")
    page = paginated.get_page(page_number)
    context = {"page": page}
    return render(request, "overtime/ot/list.html", context)


@login_required
@user_passes_test(lambda u: u.profile.role == "ADMIN" or u.profile.role == "HR")
def calculate_ots(request):
    calculate_ot()
    overtimes = Overtime.objects.filter(paid=False)
    ots = Ot.objects.filter(overtime__in=overtimes, paid=False).order_by("-start_date")
    paginated = Paginator(ots, 30)
    page_number = request.GET.get("page")
    page = paginated.get_page(page_number)
    context = {"page": page}
    return render(request, "overtime/calculate/list.html", context)


@login_required
@user_passes_test(lambda u: u.profile.role == "ADMIN" or u.profile.role == "HR")
def post_overtime(request):
    post_ot()

    return redirect("overtime:calculate_ots")
