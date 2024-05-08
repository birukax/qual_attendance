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


class EmployeeWidget(s2forms.ModelSelect2Widget):
    search_fields = ["name__icontains", "employee_id__icontains"]


class CreateLeaveForm(forms.ModelForm):
    class Meta:
        model = Leave
        fields = (
            "employee",
            "leave_type",
            "start_date",
            "end_date",
            "reason",
            "is_half_day",
        )
        widgets = {
            "employee": EmployeeWidget,
            "leave_type": forms.Select(attrs={"class": "search-select"}),
            "start_date": DatePickerInput(options=FlatpickrOptions()),
            "end_date": DatePickerInput(options=FlatpickrOptions()),
            "reason": forms.Textarea(attrs={"rows": 3}),
            "is_half_day": forms.CheckboxInput(),
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


class CreateLeaveTypeForm(forms.ModelForm):
    class Meta:
        model = LeaveType
        fields = (
            "name",
            "maximum_days",
            "description",
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
