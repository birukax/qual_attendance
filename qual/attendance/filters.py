import django_filters
from .models import *
from employee.models import Employee
from device.models import Device
from shift.models import Pattern
from leave.models import LeaveType

class AttendanceDownloadFilter(django_filters.FilterSet):
    class Meta:
        model = Attendance
        fields = {'employee__name': ['icontains'], 
                #   'device__name': ['icontains'], 
                  'current_pattern__name': ['icontains'],  
                  'status': ['exact'], 
                  'check_in_type': ['exact'], 
                  'check_out_type': ['exact'], }
    status = django_filters.ChoiceFilter(choices=Attendance.CHOICES)
    check_in_date = django_filters.DateFromToRangeFilter(widget=django_filters.widgets.RangeWidget(attrs={'type': 'date'}))

class AttendanceFilter(django_filters.FilterSet):
    class Meta:
        model = Attendance
        fields = {
            'employee__name': ['icontains'],
            'device': ['exact'],
            'current_pattern': ['exact'],
            'check_in_date': ['exact'],
            'status': ['exact'],
            'check_in_type': ['exact'],
            'check_out_type': ['exact'],
        }

class RawAttendanceFilter(django_filters.FilterSet):
    class Meta:
        model = RawAttendance
        fields = {
            'employee__name': ['icontains'],
            'device': ['exact'],
            'date': ['exact'],
        }