import django_filters
import django_filters.widgets
from .models import Leave, LeaveType
from django_select2 import forms as s2forms
from employee.models import Employee


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
