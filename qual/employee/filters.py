import django_filters
from .models import *


class EmployeeFilter(django_filters.FilterSet):
    class Meta:
        model = Employee
        fields = {
            "employee_id": ["icontains"],
            "name": ["icontains"],
            "shift": ["exact"],
            "status": ["exact"],
            "department": ["exact"],
        }
