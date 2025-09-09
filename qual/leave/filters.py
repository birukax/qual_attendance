import django_filters
import django_filters.widgets
from django_select2 import forms as s2forms
from .models import Leave, LeaveType
from shift.models import Shift
from device.models import Device
from employee.models import Employee, Department
from qual.custom_widgets import (
    DepartmentWidget,
    EmployeeWidget,
    DeviceWidget,
    ShiftWidget,
)


class AnnualLeaveFilter(django_filters.FilterSet):
    class Meta:
        model = Employee
        fields = (
            "employee_id",
            "id",
            "department",
            "device",
            "shift",
            "status",
        )

    employee_id = django_filters.CharFilter(
        label="Employee ID",
        lookup_expr="exact",
        widget=s2forms.Select2Widget(
            attrs={"class": "w-full"},
            choices=Employee.objects.all().values_list("employee_id", "employee_id"),
        ),
    )
    id = django_filters.CharFilter(
        label="Employee Name",
        lookup_expr="exact",
        widget=s2forms.Select2Widget(
            attrs={"class": "w-full"},
            choices=Employee.objects.all().values_list("id", "name"),
        ),
    )

    department = django_filters.ModelChoiceFilter(
        queryset=Department.objects.all(),
        label="Department",
        lookup_expr="exact",
        widget=DepartmentWidget(),
    )

    shift = django_filters.ModelChoiceFilter(
        queryset=Shift.objects.all(),
        label="Shift",
        lookup_expr="exact",
        widget=ShiftWidget(),
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


class LeaveFilter(django_filters.FilterSet):
    class Meta:
        model = Leave
        fields = (
            "employee",
            "employee__department",
            "leave_type",
            "approved",
            "rejected",
            "half_day",
            "start_date",
        )

    employee = django_filters.ModelChoiceFilter(
        queryset=Employee.objects.all(),
        label="Employee",
        lookup_expr="exact",
        widget=EmployeeWidget(),
    )
    employee__department = django_filters.ModelChoiceFilter(
        queryset=Department.objects.all(),
        label="Department",
        lookup_expr="exact",
        widget=DepartmentWidget(),
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
    approved = django_filters.BooleanFilter(
        label="Approved",
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
    rejected = django_filters.BooleanFilter(
        label="Rejected",
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


# class LeaveDownloadFilter(django_filters.FilterSet):
#     class Meta:
#         model = Leave
#         fields = {
#             "employee__name": ["icontains"],
#             "employee__device": ["exact"],
#             "leave_type": ["exact"],
#             "approved": ["exact"],
#             "rejected": ["exact"],
#             "half_day": ["exact"],
#             "start_date": ["exact"],
#         }

#     start_date = django_filters.DateFromToRangeFilter(
#         widget=django_filters.widgets.RangeWidget(attrs={"type": "date"})
#     )
