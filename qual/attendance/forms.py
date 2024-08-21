# from asyncio.windows_events import NULL
from django import forms
from .models import Attendance, OnField
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


class CreateOnFieldForm(forms.ModelForm):
    class Meta:
        model = OnField
        fields = ("employee", "start_date", "end_date", "reason")

        widgets = {
            "employee": EmployeeWidget,
            "start_date": DatePickerInput(options=FlatpickrOptions()),
            "end_date": DatePickerInput(options=FlatpickrOptions()),
            "reason": forms.Textarea(attrs={"rows": 3, "cols": 40}),
        }

    def clean(self):
        cleaned_data = super().clean()
        employee = cleaned_data.get("employee")
        start_date = cleaned_data.get("start_date")
        end_date = cleaned_data.get("end_date")
        if start_date and end_date:
            if start_date > end_date:
                raise forms.ValidationError(
                    _("Start date should be less than or equal to end date.")
                )
        qs = OnField.objects.filter(employee=employee).exclude(rejected=True)
        active_on_field = qs.filter(
            Q(start_date__lte=start_date, end_date__gte=start_date)
            | Q(start_date__lte=end_date, end_date__gte=end_date)
        ).exists()
        if active_on_field:
            raise ValidationError(
                _("Employee can't have multiple on field data on the same date.")
            )

        return cleaned_data


class EditOnFieldForm(forms.ModelForm):
    class Meta:
        model = OnField
        fields = ("employee", "start_date", "end_date", "reason")

        widgets = {
            "start_date": DatePickerInput(options=FlatpickrOptions()),
            "end_date": DatePickerInput(options=FlatpickrOptions()),
            "reason": forms.Textarea(attrs={"rows": 3, "cols": 40}),
        }

    def __init__(self, *args, **kwargs):
        super(EditOnFieldForm, self).__init__(*args, **kwargs)
        self.fields["employee"].disabled = True

    def clean(self):
        cleaned_data = super().clean()
        employee = cleaned_data.get("employee")
        start_date = cleaned_data.get("start_date")
        end_date = cleaned_data.get("end_date")
        if start_date and end_date:
            if start_date > end_date:
                raise forms.ValidationError(
                    _("Start date should be less than or equal to end date.")
                )
        qs = (
            OnField.objects.filter(employee=employee)
            .exclude(id=self.instance.id)
            .exclude(rejected=True)
        )
        active_on_field = qs.filter(
            Q(start_date__lte=start_date, end_date__gte=start_date)
            | Q(start_date__lte=end_date, end_date__gte=end_date)
        ).exists()
        if active_on_field:
            raise ValidationError(
                _("Employee can't have multiple on field data on the same date.")
            )

        return cleaned_data
