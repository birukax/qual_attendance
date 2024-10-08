from email.policy import default
import django_filters
import django_filters.widgets
from .models import Leave, LeaveType
from django_select2 import forms as s2forms
from employee.models import Employee
from django.db import models


class AnnualLeaveDownloadFilter(django_filters.FilterSet):
    class Meta:
        model = Employee
        fields = {
            "id": ["icontains"],
            "name": ["icontains"],
            "department": ["exact"],
            "device": ["exact"],
            "shift": ["exact"],
            "status": ["exact"],
        }


class LeaveFilter(django_filters.FilterSet):
    class Meta:
        model = Leave
        fields = {
            "employee__name": ["icontains"],
            "employee__device": ["exact"],
            "leave_type": ["exact"],
            "approved": ["exact"],
            "rejected": ["exact"],
            "half_day": ["exact"],
            "start_date": ["exact"],
        }

    start_date = django_filters.DateFromToRangeFilter(
        widget=django_filters.widgets.RangeWidget(attrs={"type": "date"})
    )


class LeaveDownloadFilter(django_filters.FilterSet):
    class Meta:
        model = Leave
        fields = {
            "employee__name": ["icontains"],
            "employee__device": ["exact"],
            "leave_type": ["exact"],
            "approved": ["exact"],
            "rejected": ["exact"],
            "half_day": ["exact"],
            "start_date": ["exact"],
        }

    start_date = django_filters.DateFromToRangeFilter(
        widget=django_filters.widgets.RangeWidget(attrs={"type": "date"})
    )
