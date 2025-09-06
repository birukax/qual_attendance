import django_filters
from django_select2 import forms as s2forms
from django import forms

from device.models import Device
from shift.models import Shift
from .models import Department, Employee
from qual.custom_widgets import (
    EmployeeWidget,
    ShiftWidget,
    DepartmentWidget,
    DeviceWidget,
)


class EmployeeFilter(django_filters.FilterSet):
    class Meta:
        model = Employee
        fields = (
            "id",
            "shift",
            "department",
            "device",
            "status",
            "employment_date",
        )

    id = django_filters.ModelChoiceFilter(
        queryset=Employee.objects.all(),
        label="Name",
        lookup_expr="exact",
        widget=EmployeeWidget(),
    )
    shift = django_filters.ModelChoiceFilter(
        queryset=Shift.objects.all(),
        label="Shift",
        lookup_expr="exact",
        widget=ShiftWidget(),
    )
    department = django_filters.ModelChoiceFilter(
        queryset=Department.objects.all(),
        label="Department",
        lookup_expr="exact",
        widget=DepartmentWidget(),
    )
    device = django_filters.ModelChoiceFilter(
        queryset=Device.objects.all(),
        label="Device",
        lookup_expr="exact",
        widget=DeviceWidget(),
    )
    status = django_filters.CharFilter(
        label="Status",
        lookup_expr="exact",
        widget=s2forms.Select2Widget(
            attrs={"class": "w-full"},
            choices=(
                ("", "-------"),
                ("Active", "Active"),
                ("Inactive", "Inactive"),
                ("Terminated", "Terminated"),
            ),
        ),
    )

    employment_date = django_filters.DateFromToRangeFilter(
        label="Employment Date",
        widget=django_filters.widgets.DateRangeWidget(
            attrs={"type": "date", "class": "w-full h-10 rounded-sm"}
        ),
    )
