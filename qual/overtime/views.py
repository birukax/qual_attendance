from datetime import datetime
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
import requests
from requests_ntlm import HttpNtlmAuth
from .models import *
from django.core.paginator import Paginator
from .forms import *
from .tasks import calculate_ot, post_ot
from urllib.parse import quote


@login_required
def create_overtime(request):
    if request.method == "POST":
        form = CreateOvertimeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("overtime:overtimes")


# @login_required
# def approve_overtime(request, id):
#     overtime = Overtime.objects.get(id=id)
#     overtime.approved = True
#     overtime.save()
#     return redirect("overtime:overtime_detail", id=id)


@login_required
def calculate_overtime(request, id):
    calculate_ot(id=id)
    return redirect("overtime:overtime_detail", id=id)


@login_required
def post_overtime(request):
    post_ot()

    return redirect("overtime:overtimes")


@login_required
def overtimes(request):
    create_overtime_form = CreateOvertimeForm()
    overtimes = Overtime.objects.all().order_by("-start_date")
    paginated = Paginator(overtimes, 10)
    page_number = request.GET.get("page")

    page = paginated.get_page(page_number)
    context = {"page": page, "create_overtime_form": create_overtime_form}
    return render(request, "overtime/list.html", context)


@login_required
def overtime_detail(request, id):
    overtime = get_object_or_404(Overtime, id=id)
    context = {"overtime": overtime}
    return render(request, "overtime/detail.html", context)


@login_required
def edit_overtime(request, id):
    pass
    # overtime = get_object_or_404(Overtime, id=id)
    # edit_overtime_form = EditOvertimeForm(instance=overtime)
    # context = {"overtime": overtime, "edit_overtime_form": edit_overtime_form}
    # return render(request, "overtime/edit.html", context)


@login_required
def create_overtime_type(request):
    if request.method == "POST":
        create_ot_type_form = CreateOvertimeTypeForm(request.POST)
        if create_ot_type_form.is_valid():
            create_ot_type_form.save()
            return redirect("overtime:overtime_types")


@login_required
def edit_overtime_type(request, id):
    overtime_type = get_object_or_404(OvertimeType, id=id)
    if request.method == "POST":
        edit_ot_type_form = EditOvertimeTypeForm(request.POST, instance=overtime_type)
        if edit_ot_type_form.is_valid():
            edit_ot_type_form.save()
    return redirect("overtime:overtime_type_detail", id=id)


@login_required
def overtime_types(request):
    crate_overtime_type_form = CreateOvertimeTypeForm()
    overtime_types = OvertimeType.objects.all().order_by("name")
    paginated = Paginator(overtime_types, 10)
    page_number = request.GET.get("page")

    page = paginated.get_page(page_number)
    context = {"page": page, "create_ot_type_form": crate_overtime_type_form}
    return render(request, "overtime/overtime_type/list.html", context)


@login_required
def overtime_type_detail(request, id):
    overtime_type = get_object_or_404(OvertimeType, id=id)
    edit_overtime_type_form = EditOvertimeTypeForm(instance=overtime_type)
    overtimes = Ot.objects.filter(overtime_type=overtime_type)
    days = overtime_type.days.all()
    paginated = Paginator(overtimes, 10)
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
def ots(request):
    ots = Ot.objects.all().order_by("-date")
    paginated = Paginator(ots, 10)
    page_number = request.GET.get("page")
    page = paginated.get_page(page_number)
    context = {"page": page}
    return render(request, "overtime/ot/list.html", context)
