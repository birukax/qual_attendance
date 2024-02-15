import django_filters 
from .models import *

class EmployeeFilter(django_filters.FilterSet):
    class Meta:
        model = Employee
        fields = {
            'employee_id': ['icontains'],
            'name': ['icontains'],
            'shift': ['exact'],
            'pattern': ['exact'],
            'status' : ['exact'],
        }