from random import choice
import django_filters
from django_select2 import forms as s2forms
import django_filters.widgets
from employee.models import Employee
from leave.models import Leave, LeaveType
from overtime.models import Overtime
from holiday.models import Holiday
from account.custom_widgets import EmployeeWidget, LeaveTypeWidget


class LeaveFilter(django_filters.FilterSet):
    class Meta:
        model = Leave
        fields = (
            "employee",
            "leave_type",
            "half_day",
            "start_date",
        )

    employee = django_filters.ModelChoiceFilter(
        queryset=Employee.objects.all(),
        label="Employee",
        lookup_expr="exact",
        widget=EmployeeWidget(),
    )
    leave_type = django_filters.ModelChoiceFilter(
        queryset=LeaveType.objects.all(),
        label="Leave Type",
        lookup_expr="exact",
        widget=s2forms.Select2Widget(
            attrs={"class": "w-full"},
            choices=LeaveType.objects.all().values_list("id", "name"),
        ),
    )
    half_day = django_filters.BooleanFilter(
        label="Half Day",
        lookup_expr="exact",
        widget=s2forms.Select2Widget(
            attrs={"class": "w-full"},
            choices=(
                (None, ""),
                (True, "Yes"),
                (False, "No"),
            ),
        ),
    )
    start_date = django_filters.DateFromToRangeFilter(
        label="Start Date",
        widget=django_filters.widgets.DateRangeWidget(
            attrs={"type": "date", "class": "w-full h-10 rounded-sm"}
        ),
    )


class OvertimeFilter(django_filters.FilterSet):
    class Meta:
        model = Overtime
        fields = {
            "employee",
        }

    employee = django_filters.ModelChoiceFilter(
        queryset=Employee.objects.all(),
        label="Employee",
        lookup_expr="exact",
        widget=EmployeeWidget(),
    )


class HolidayFilter(django_filters.FilterSet):
    class Meta:
        model = Holiday
        fields = (
            "name",
            "date",
        )

    name = django_filters.CharFilter(
        label="Name",
        lookup_expr="exact",
        widget=s2forms.Select2Widget(
            attrs={"class": "w-full"},
            choices=Holiday.objects.filter(approved=False, rejected=False).values_list(
                "name", "name"
            ),
        ),
    )

    date = django_filters.DateFromToRangeFilter(
        label="Date",
        widget=django_filters.widgets.DateRangeWidget(
            attrs={"type": "date", "class": "w-full h-10 rounded-sm"}
        ),
    )
