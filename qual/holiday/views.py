from operator import is_
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .models import *
from .forms import *


@login_required
def create_holiday(request):
    if request.method == "POST":
        form = CreateHolidayForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data["name"]
            date = form.cleaned_data["date"]
            description = form.cleaned_data["description"]
            holiday = Holiday(name=name, date=date, description=description)
            holiday.save()
        return redirect("holiday:holidays")


@login_required
def holidays(request):
    create_holiday_form = CreateHolidayForm(data=request.GET)
    holidays = Holiday.objects.all().order_by("-date")
    paginated = Paginator(holidays, 10)
    page_number = request.GET.get("page")

    page = paginated.get_page(page_number)
    context = {"create_holiday_form": create_holiday_form, "page": page}
    return render(request, "holiday/list.html", context)


# @login_required
# def holiday_detail(request, id):
#     holiday = get_object_or_404(Holiday, id=id)

#     context = {"holiday": holiday}
#     return render(request, "holiday/detail.html", context)


@login_required
def approve_holiday(request, id):
    holiday = Holiday.objects.get(id=id)
    holiday.approved = True
    holiday.save()
    return redirect("holiday:holidays")


@login_required
def edit_holiday(request, id):
    holiday = get_object_or_404(Holiday, id=id)

    if request.method == "POST":
        pass
