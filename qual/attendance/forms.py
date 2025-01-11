# from asyncio.windows_events import NULL
from django import forms
from .models import Attendance
from employee.models import Employee
from device.models import Device
from shift.models import Pattern
from django_flatpickr.widgets import (
    DatePickerInput,
)
from django_flatpickr.schemas import FlatpickrOptions
from django_select2 import forms as s2forms
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.utils.translation import gettext_lazy as _


class EmployeeWidget(s2forms.ModelSelect2Widget):
    search_fields = ["name__icontains", "employee_id__icontains"]


class AttendanceDownloadForm(forms.ModelForm):
    class Meta:
        model = Attendance()
        fields = ("employee", "device", "current_pattern")

    employee = forms.ModelChoiceField(Employee.objects.all(), required=False)
    device = forms.ModelChoiceField(Device.objects.all(), required=False)
    current_pattern = forms.ModelChoiceField(Pattern.objects.all(), required=False)
    start_date = forms.DateField()
    end_date = forms.DateField()


class RecompileForm(forms.Form):

    pattern = forms.ModelChoiceField(Pattern.objects.all(), required=False)
    date = forms.DateField(widget=DatePickerInput(options=FlatpickrOptions()))


class EmployeesForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ("id", "selected")

    selected = forms.BooleanField(required=False)
