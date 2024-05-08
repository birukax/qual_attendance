import django_filters
from .models import Employee


class EmployeeFilter(django_filters.FilterSet):
    class Meta:
        model = Employee
        fields = {
            "name": ["icontains"],
            "shift": ["exact"],
            "status": ["exact"],
            "department": ["exact"],
            "device": ["exact"],
        }
