from operator import is_
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .models import *
from attendance.models import Attendance
from .forms import *
from django.contrib.auth.decorators import user_passes_test


@login_required
@user_passes_test(lambda u: u.profile.role == "ADMIN" or u.profile.role == "HR")
def holidays(request):
    create_holiday_form = CreateHolidayForm(data=request.GET)
    holidays = Holiday.objects.all().order_by("-date")
    # for holiday in holidays.filter(approved=True):
    #     holiday_attendances = Attendance.objects.filter(
    #         check_in_date=holiday.date,
    #         status__in=("Absent", "Day Off", "On Leave"),
    #     )
    #     if holiday_attendances:
    #         for att in holiday_attendances:
    #             att.status = "Holiday"
    #             att.save()
    paginated = Paginator(holidays, 30)
    page_number = request.GET.get("page")

    page = paginated.get_page(page_number)
    context = {
        "form": create_holiday_form,
        "page": page,
    }
    return render(request, "holiday/list.html", context)


@login_required
@user_passes_test(lambda u: u.profile.role == "ADMIN" or u.profile.role == "HR")
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
