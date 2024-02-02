from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Shift, Pattern
from django.core.paginator import Paginator
from .forms import CreateShiftForm,EditShiftForm ,CreatePatternForm,EditPatternForm ,ChangeEmployeeShiftForm, ChangeEmployeePatternForm
from employee.models import Employee



@login_required
def create_shift(request):
    if request.method == "POST":
        form = CreateShiftForm(data=request.POST)
        if form.is_valid():
            name = form.cleaned_data["name"]
            continous = form.cleaned_data["continous"]
            saturday_half = form.cleaned_data["saturday_half"]
            shft, created = Shift.objects.get_or_create(
                name=name,
                continous=continous,
                saturday_half=saturday_half,
            )
            return redirect("shift:shifts")

@login_required
def shifts(request):
    create_shift_form = CreateShiftForm(data=request.GET)
    shifts = Shift.objects.all()
    paginated = Paginator(shifts, 15)
    page_number = request.GET.get("page")
    
    page = paginated.get_page(page_number)
    return render(
        request, "shift/shift_list.html", {"create_shift_form":create_shift_form,"shifts":shifts ,"page":page}   
    )

@login_required
def shift_detail(request, id):
    shift = get_object_or_404(Shift, id=id)
    patterns = Pattern.objects.filter(shift=shift)
    create_pattern_form = CreatePatternForm(data=request.GET, shift=shift,)
    edit_shift_form = EditShiftForm(instance=shift)
    employees = Employee.objects.filter(shift=shift)
    paginated = Paginator(employees, 15)
    page_number = request.GET.get("page")
    page = paginated.get_page(page_number)
    
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
            return redirect("shift:shift_detail", id=pattern.shift.id)
        
    context = {
        "shift": shift, 
        "page": page, 
        "patterns":patterns , 
        "create_pattern_form":create_pattern_form, 
        "edit_shift_form":edit_shift_form 
        }
    return render(
        request, "shift/shift_detail.html", context
    )

@login_required
def change_shift(request, id ):
    if request.method == "POST":
        employee = Employee.objects.get(id=id)
        shift_form = ChangeEmployeeShiftForm(request.POST, instance=employee)
        if shift_form.is_valid():
            shift_form.save()
            return redirect("employee:employee_detail", id=id)
        
@login_required
def change_pattern(request, id ):
    if request.method == "POST":
        employee = Employee.objects.get(id=id)
        pattern_form = ChangeEmployeePatternForm(request.POST, instance=employee)
        if pattern_form.is_valid():
            pattern_form.save()
            return redirect("employee:employee_detail", id=id)

@login_required
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
            
            return redirect("shift:shift_detail", id=pattern.shift.id)
    else:
        form = EditPatternForm(instance=pattern)
    return render(request, "shift/pattern/edit_pattern.html", {"pattern":pattern,"form": form})

@login_required
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