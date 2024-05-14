from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Shift, Pattern
from django.core.paginator import Paginator
from .forms import (
    CreateShiftForm,
    SelectShiftForm,
    EditShiftForm,
    EditPatternForm,
    CreatePatternForm,
)
from employee.models import Employee
from employee.filters import EmployeeFilter
from employee.forms import ChangeEmployeeShiftForm
from django.contrib.auth.decorators import user_passes_test
from device.models import Device


@login_required
@user_passes_test(lambda u: u.profile.role != "USER")
def shifts(request):
    create_shift_form = CreateShiftForm(data=request.GET)
    shifts = Shift.objects.all().order_by("-name")
    paginated = Paginator(shifts, 30)
    page_number = request.GET.get("page")

    page = paginated.get_page(page_number)
    context = {
        "create_shift_form": create_shift_form,
        "page": page,
    }
    return render(request, "shift/list.html", context)


@login_required
@user_passes_test(lambda u: u.profile.role != "USER")
def shift_detail(request, id):
    shift = get_object_or_404(Shift, id=id)
    edit_shift_form = EditShiftForm(instance=shift)
    employees = Employee.objects.filter(shift=shift)
    paginated = Paginator(employees, 30)
    page_number = request.GET.get("page")
    page = paginated.get_page(page_number)

    context = {
        "shift": shift,
        "page": page,
        "edit_shift_form": edit_shift_form,
    }
    return render(request, "shift/detail.html", context)


@login_required
@user_passes_test(lambda u: u.profile.role == "ADMIN" or u.profile.role == "HR")
def create_shift(request):
    if request.method == "POST":
        form = CreateShiftForm(data=request.POST)
        if form.is_valid():
            name = form.cleaned_data["name"]
            continous = form.cleaned_data["continous"]
            saturday_half = form.cleaned_data["saturday_half"]
            device = form.cleaned_data["device"]
            shift = Shift(
                name=name,
                continous=continous,
                saturday_half=saturday_half,
                device=device,
            )
            shift.save()

    return redirect("shift:shifts")


@login_required
@user_passes_test(lambda u: u.profile.role == "ADMIN" or u.profile.role == "HR")
def edit_shift(request, id):
    shift = get_object_or_404(Shift, id=id)
    if request.method == "POST":
        form = EditShiftForm(data=request.POST, instance=shift)
        if form.is_valid():
            shift.name = form.cleaned_data["name"]
            shift.continous = form.cleaned_data["continous"]
            shift.saturday_half = form.cleaned_data["saturday_half"]
            shift.save()
    return redirect("shift:shift_detail", id=shift.id)


@login_required
@user_passes_test(lambda u: u.profile.role != "USER")
def change_shift(request, id):
    if request.method == "POST":
        employee = Employee.objects.get(id=id)
        shift_form = ChangeEmployeeShiftForm(request.POST, instance=employee)
        if request.user.profile.role == "ADMIN" or request.user.profile.role == "HR":
            if shift_form.is_valid():
                shift_form.save()
        elif employee.department in request.user.profile.manages.all():
            if shift_form.is_valid():
                shift_form.save()
    return redirect("employee:employee_detail", id=id)


@login_required
@user_passes_test(lambda u: u.profile.role != "USER")
def shift_employees(request, id):
    shift = get_object_or_404(Shift, id=id)
    if request.user.profile.role == "ADMIN" or request.user.profile.role == "HR":
        employees = Employee.objects.filter(shift=shift)
    else:
        employees = Employee.objects.filter(
            shift=shift,
            department__in=request.user.profile.manages.all(),
        )
    paginated = Paginator(employees, 30)
    page_number = request.GET.get("page")
    page = paginated.get_page(page_number)
    context = {
        "page": page,
        "shift": shift,
    }
    return render(request, "shift/employee/list.html", context)


@login_required
@user_passes_test(lambda u: u.profile.role != "USER")
def shift_patterns(request, id):
    shift = get_object_or_404(Shift, id=id)
    patterns = Pattern.objects.filter(shift=shift)
    create_pattern_form = CreatePatternForm(
        data=request.GET,
        shift=shift,
    )
    paginated = Paginator(patterns, 30)
    page_number = request.GET.get("page")
    page = paginated.get_page(page_number)
    context = {
        "page": page,
        "shift": shift,
        "create_pattern_form": create_pattern_form,
    }
    return render(request, "shift/pattern/list.html", context)


@login_required
@user_passes_test(lambda u: u.profile.role != "USER")
def select_employees(request):
    if request.user.profile.role == "ADMIN" or request.user.profile.role == "HR":
        employees = Employee.objects.filter(status="Active").order_by("name")
    else:
        employees = Employee.objects.filter(
            status="Active", department__in=request.user.profile.manages.all()
        ).order_by("name")
    employee_filter = EmployeeFilter(request.GET, queryset=employees)
    employees = employee_filter.qs
    context = {"employee_filter": employee_filter, "employees": employees}
    return render(request, "shift/assign/select.html", context)


@login_required
@user_passes_test(lambda u: u.profile.role != "USER")
def set_employees(request):
    if request.method == "POST":
        if request.user.profile.role == "ADMIN" or request.user.profile.role == "HR":
            employees = Employee.objects.filter(
                status="Active", id__in=request.POST.getlist("employees")
            ).order_by("name")
        else:
            employees = Employee.objects.filter(
                status="Active",
                department__in=request.user.profile.manages.all(),
                id__in=request.POST.getlist("employees"),
            ).order_by("name")
        select_shift_form = SelectShiftForm()
        context = {
            "employees": employees,
            "select_shift_form": select_shift_form,
        }
        # shift = form.cleaned_data["shift"]
        # for employee in employees:
        #     employee.shift = shift
        #     employee.save()
        return render(request, "shift/assign/set.html", context)


@login_required
@user_passes_test(lambda u: u.profile.role != "USER")
def assign_employees(request):
    if request.method == "POST":
        form = SelectShiftForm(request.POST)
        if form.is_valid():
            shift = form.cleaned_data["shift"]
            if (
                request.user.profile.role == "ADMIN"
                or request.user.profile.role == "HR"
            ):
                employees = Employee.objects.filter(
                    status="Active", id__in=request.POST.getlist("employees")
                ).order_by("name")
            else:
                employees = Employee.objects.filter(
                    status="Active",
                    department__in=request.user.profile.manages.all(),
                    id__in=request.POST.getlist("employees"),
                ).order_by("name")
            for employee in employees:
                employee.shift = shift
                if employee.device is None:
                    employee.device = shift.device
                employee.save()
            if (
                request.user.profile.role == "Admin"
                or request.user.profile.role == "HR"
            ):
                return redirect("shift:shifts")
            else:
                return redirect("employee:employees")
        return render(request, "shift/assign/select.html")


@login_required
@user_passes_test(lambda u: u.profile.role == "ADMIN" or u.profile.role == "HR")
def create_pattern(request, id):
    shift = get_object_or_404(Shift, id=id)
    if request.method == "POST":
        form = CreatePatternForm(data=request.POST, shift=shift)
        if form.is_valid():
            name = form.cleaned_data["name"]
            day_span = form.cleaned_data["day_span"]
            shift = shift
            start_time = form.cleaned_data["start_time"]
            end_time = form.cleaned_data["end_time"]
            tolerance = form.cleaned_data["tolerance"]
            next = form.cleaned_data["next"]
            pattern, created = Pattern.objects.get_or_create(
                name=name,
                day_span=day_span,
                shift=shift,
                start_time=start_time,
                end_time=end_time,
                tolerance=tolerance,
                next=next,
            )
            if not pattern.next:
                pattern.next = pattern
                pattern.save()
        return redirect("shift:shift_patterns", id=shift.id)


@login_required
@user_passes_test(lambda u: u.profile.role == "ADMIN" or u.profile.role == "HR")
def edit_pattern(request, id):
    pattern = get_object_or_404(Pattern, id=id)
    if request.method == "POST":
        form = EditPatternForm(data=request.POST, instance=pattern)
        if form.is_valid():
            pattern.name = form.cleaned_data["name"]
            pattern.day_span = form.cleaned_data["day_span"]
            pattern.shift = pattern.shift
            pattern.start_time = form.cleaned_data["start_time"]
            pattern.end_time = form.cleaned_data["end_time"]
            pattern.tolerance = form.cleaned_data["tolerance"]
            pattern.next = form.cleaned_data["next"]
            pattern.save()

            return redirect("shift:shift_patterns", id=pattern.shift.id)
    else:
        form = EditPatternForm(instance=pattern)
    return render(
        request, "shift/pattern/edit.html", {"pattern": pattern, "form": form}
    )
