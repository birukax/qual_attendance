from django import forms
from employee.models import Employee
from .models import OvertimeType, Overtime
from django_flatpickr.widgets import (
    DatePickerInput,
    TimePickerInput,
    DateTimePickerInput,
)
from django_flatpickr.schemas import FlatpickrOptions
from django_select2 import forms as s2forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class EmployeeWidget(s2forms.ModelSelect2Widget):
    search_fields = ["name__icontains", "employee_id__icontains"]


class CreateOvertimeTypeForm(forms.ModelForm):
    class Meta:
        model = OvertimeType
        fields = (
            "name",
            "pay_item_code",
            "start_time",
            "end_time",
            "day_span",
            "days",
        )
        widgets = {
            "start_time": TimePickerInput(options=FlatpickrOptions()),
            "end_time": TimePickerInput(options=FlatpickrOptions()),
        }


class EditOvertimeTypeForm(forms.ModelForm):
    class Meta:
        model = OvertimeType
        fields = (
            "name",
            "pay_item_code",
            "start_time",
            "end_time",
            "day_span",
            "days",
        )
        widgets = {
            "start_time": TimePickerInput(options=FlatpickrOptions()),
            "end_time": TimePickerInput(options=FlatpickrOptions()),
        }


class CreateOvertimeForm(forms.ModelForm):
    class Meta:
        model = Overtime
        fields = (
            "employee",
            "start_date",
            "end_date",
            "start_time",
            "end_time",
            "reason",
        )
        widgets = {
            "employee": EmployeeWidget,
            "start_date": DatePickerInput(options=FlatpickrOptions()),
            "end_date": DatePickerInput(options=FlatpickrOptions()),
            "start_time": TimePickerInput(options=FlatpickrOptions()),
            "end_time": TimePickerInput(options=FlatpickrOptions()),
            "reason": forms.Textarea(attrs={"rows": 3}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user")
        super(CreateOvertimeForm, self).__init__(*args, **kwargs)
        self.fields["employee"].queryset = Employee.objects.filter(
            status="Active"
        ).order_by("name")
        if self.user.profile.role == "ADMIN" or self.user.profile.role == "HR":
            self.fields["employee"].queryset = Employee.objects.filter(status="Active")
        else:

            self.fields["employee"].queryset = Employee.objects.filter(
                status="Active", department__in=self.user.profile.manages.all()
            )

    def clean(self):
        cleaned_data = super().clean()
        employee = cleaned_data.get("employee")
        start_date = cleaned_data.get("start_date")
        end_date = cleaned_data.get("end_date")
        start_time = cleaned_data.get("start_time")
        end_time = cleaned_data.get("end_time")

        if Overtime.objects.filter(
            employee=employee, start_date=start_date, approved=True
        ).exists():
            raise ValidationError(
                _("Employee can't have multiple overtime on the same date.")
            )
        if start_date and end_date and start_time and end_time:
            if start_date > end_date:
                raise ValidationError(_("Start Date cannot be greater than End Date."))
            if start_time > end_time:
                if not start_date < end_date:
                    raise ValidationError(
                        _("Start Time cannot be greater than End Time.")
                    )
