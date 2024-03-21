from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import *
from django.core.paginator import Paginator
from django.http import HttpResponse
from .calculate import calculate_annual_leaves

# from django.contrib.auth.decorators import permission_required


@login_required
def leave_list(request):
    leaves = Leave.objects.all().order_by("-start_date")
    create_leave_form = CreateLeaveForm()
    paginated = Paginator(leaves, 10)
    page_number = request.GET.get("page")

    page = paginated.get_page(page_number)
    return render(
        request,
        "leave/list.html",
        {"page": page, "create_leave_form": create_leave_form},
    )


@login_required
def annual_leave_list(request):
    employees = Employee.objects.all().order_by("employment_date")
    paginated = Paginator(employees, 10)
    page_number = request.GET.get("page")

    page = paginated.get_page(page_number)
    context = {"page": page}
    return render(request, "leave/annual_leave/list.html", context)


@login_required
def calculate_leave_balance(request):
    print("calculating")
    calculate_annual_leaves()
    return redirect("leave:annual_leaves")


@login_required
def leave_detail(request, id):
    leave = Leave.objects.get(id=id)
    return render(request, "leave/detail.html", {"leave": leave})


@login_required
def create_leave(request):
    form = CreateLeaveForm(request.POST, request.FILES)
    if form.is_valid():
        form.save()

    return redirect("leave:leaves")


@login_required
def edit_leave(request, id):
    return render(request, "leave/edit.html")


@login_required
def leave_type_list(request):
    leave_types = LeaveType.objects.all()
    create_leave_type_form = CreateLeaveTypeForm()
    paginated = Paginator(leave_types, 10)
    page_number = request.GET.get("page")
    page = paginated.get_page(page_number)
    return render(
        request,
        "leave/leave_type/list.html",
        {"page": page, "create_leave_type_form": create_leave_type_form},
    )


# @login_required
# @permission_required('leave.can_approve_leave')
# def approve_leave(request, id):
#     leave = Leave.objects.get(id=id)
#     leave.approved = True
#     leave.active = True
#     leave.save()
#     return redirect('leave:leave_detail', id=id)


@login_required
def leave_type_detail(request, id):
    leave_type = LeaveType.objects.get(id=id)
    edit_leave_type_form = EditLeaveTypeForm(instance=leave_type)
    leaves = Leave.objects.filter(leave_type=leave_type)
    paginated = Paginator(leaves, 10)
    page_number = request.GET.get("page")

    page = paginated.get_page(page_number)
    context = {
        "leave_type": leave_type,
        "edit_leave_type_form": edit_leave_type_form,
        "page": page,
    }
    return render(request, "leave/leave_type/detail.html", context)


@login_required
def create_leave_type(request):
    form = CreateLeaveTypeForm(request.POST)
    if form.is_valid():
        name = form.cleaned_data["name"]
        description = form.cleaned_data["description"]
        maximum_days = form.cleaned_data["maximum_days"]
        paid = form.cleaned_data["paid"]
        leave_type = LeaveType(
            name=name, description=description, maximum_days=maximum_days, paid=paid
        )
        leave_type.save()
    return redirect("leave:leave_types")


@login_required
def edit_leave_type(request, id):
    form = EditLeaveTypeForm(request.POST)
    leave_type = LeaveType.objects.get(id=id)
    if form.is_valid():
        leave_type.name = form.cleaned_data["name"]
        leave_type.description = form.cleaned_data["description"]
        leave_type.maximum_days = form.cleaned_data["maximum_days"]
        leave_type.paid = form.cleaned_data["paid"]
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
