import django_filters
from .models import Attendance
from employee.models import Employee
from device.models import Device
from shift.models import Pattern
from leave.models import LeaveType

class AttendanceDownloadFilter(django_filters.FilterSet):
    class Meta:
        model = Attendance
        fields = ['employee', 'device', 'leave', 'current_pattern', 'check_in_date' ]
    
    employee = django_filters.ModelChoiceFilter(queryset=Employee.objects.all().order_by('name'))
    device = django_filters.ModelChoiceFilter(queryset=Device.objects.all().order_by('name'))
    current_pattern = django_filters.ModelChoiceFilter(queryset=Pattern.objects.all().order_by('name'))
    check_in_date = django_filters.DateFromToRangeFilter(widget=django_filters.widgets.RangeWidget(attrs={'type': 'date'}))

class AttendanceFilter(django_filters.FilterSet):
    class Meta:
        model = Attendance
        fields = ['employee', 'device', 'leave', 'current_pattern', 'check_in_date' ]

    employee = django_filters.ModelChoiceFilter(queryset=Employee.objects.all().order_by('name'))
    device = django_filters.ModelChoiceFilter(queryset=Device.objects.all().order_by('name'))
    current_pattern = django_filters.ModelChoiceFilter(queryset=Pattern.objects.all().order_by('name'))
    leave = django_filters.ModelChoiceFilter(queryset=LeaveType.objects.all().order_by('name'))
    check_in_date = django_filters.DateFromToRangeFilter(widget=django_filters.widgets.RangeWidget(attrs={'type': 'date'}))