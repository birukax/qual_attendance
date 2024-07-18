from datetime import date, timedelta, datetime, time
from .models import Leave, LeaveType
from django import forms
from django.utils.text import slugify
from employee.models import Employee
from django_flatpickr.widgets import (
    DatePickerInput,
    TimePickerInput,
    DateTimePickerInput,
)
from django_flatpickr.schemas import FlatpickrOptions
from django_select2 import forms as s2forms
from django.core.exceptions import ValidationError
from django.db.models import Q
from .tasks import calculate_total_days
from django.utils.translation import gettext_lazy as _


class EmployeeWidget(s2forms.ModelSelect2Widget):
    search_fields = ["name__icontains", "employee_id__icontains"]


class ALCalculateDateForm(forms.Form):
    date = forms.DateField(initial=date.today())


class CreateLeaveForm(forms.ModelForm):
    class Meta:
        model = Leave
        fields = (
            "employee",
            "leave_type",
            "start_date",
            "end_date",
            "reason",
            "half_day",
        )
        widgets = {
            "employee": EmployeeWidget,
            "leave_type": forms.Select(attrs={"class": "search-select"}),
            "start_date": DatePickerInput(options=FlatpickrOptions()),
            "end_date": DatePickerInput(options=FlatpickrOptions()),
            "reason": forms.Textarea(attrs={"rows": 3}),
            "half_day": forms.CheckboxInput(),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user")
        super(CreateLeaveForm, self).__init__(*args, **kwargs)
        if self.user.profile.role == "ADMIN" or self.user.profile.role == "HR":
            self.fields["employee"].queryset = Employee.objects.filter(status="Active")
        else:
            user = self.user.profile
            self.fields["employee"].queryset = Employee.objects.filter(
                status="Active", department__in=user.manages.all()
            )

    def clean(self):
        cleaned_data = super().clean()
        employee = cleaned_data.get("employee")
        start_date = cleaned_data.get("start_date")
        end_date = cleaned_data.get("end_date")
        leave_type = cleaned_data.get("leave_type")
        half_day = cleaned_data.get("half_day")

        if employee:
            active_leave = Leave.objects.filter(
                ~Q(rejected=True),
                start_date__range=(start_date, end_date),
                end_date__range=(start_date, end_date),
                employee=employee,
            )
            if active_leave:
                raise ValidationError(
                    _("Employee can't have multiple leave on the same date.")
                )

        if end_date and start_date and leave_type:
            total_days = calculate_total_days(start_date, end_date, leave_type.annual)
            if half_day:
                total_days = total_days - 0.5
            if start_date > end_date:
                raise ValidationError(_("Start Date cannot be greater than End Date."))

            if leave_type.annual == True:
                employee_balance = employee.annual_leave_remaining
                # total_days = total_days.days + 1
                if employee_balance < total_days:
                    raise ValidationError(_("Insufficient annual leave balance."))
            else:
                maximum_days = leave_type.maximum_days
                if total_days > maximum_days:
                    raise ValidationError(
                        _("Total date is greater than the leave type's maximum date.")
                    )


class CreateLeaveTypeForm(forms.ModelForm):
    class Meta:
        model = LeaveType
        fields = (
            "name",
            "maximum_days",
            "description",
            "annual",
            "paid",
        )
        widgets = {
            "paid": forms.CheckboxInput(),
            "description": forms.Textarea(attrs={"rows": 3}),
        }

    def save(self, force_insert=False, force_update=False, commit=True):
        leave_type = LeaveType()
        leave_type.slug = slugify(leave_type.name)

        leave_type.save()

        return leave_type


class EditLeaveTypeForm(forms.ModelForm):
    class Meta:
        model = LeaveType
        fields = (
            "name",
            "maximum_days",
            "description",
            "annual",
            "paid",
        )
        widgets = {
            "paid": forms.CheckboxInput(),
            "description": forms.Textarea(attrs={"rows": 3}),
        }

    def save(self, force_insert=False, force_update=False, commit=True):
        leave_type = LeaveType()
        leave_type.slug = slugify(leave_type.name)

        leave_type.save()

        return leave_type
