from django_select2 import forms as s2forms
from employee.models import Department, Employee
from leave.models import Leave, LeaveType
from shift.models import Shift, Pattern
from device.models import Device, DeviceUser


class BaseSelectWidget(s2forms.ModelSelect2Widget):
    attrs = {"class": "w-full"}


class DepartmentWidget(BaseSelectWidget):
    queryset = Department.objects.all()
    search_fields = [
        "code__icontains",
        "name__icontains",
    ]


class DeviceWidget(BaseSelectWidget):
    queryset = Device.objects.all()
    search_fields = [
        "name__icontains",
    ]


class EmployeeWidget(BaseSelectWidget):
    queryset = Employee.objects.all()
    search_fields = [
        "employee_id__icontains",
        "name__icontains",
    ]


class LeaveTypeWidget(BaseSelectWidget):
    queryset = LeaveType.objects.all()
    search_fields = [
        "name__icontains",
    ]


class PatternWidget(BaseSelectWidget):
    queryset = Pattern.objects.all()
    search_fields = [
        "name__icontains",
    ]


class ShiftWidget(BaseSelectWidget):
    queryset = Shift.objects.all()
    search_fields = [
        "name__icontains",
    ]
