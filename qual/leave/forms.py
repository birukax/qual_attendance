from datetime import date
from .models import Leave, LeaveType
from django import forms
from django.utils.text import slugify
from employee.models import Employee
from django_flatpickr.widgets import (
    DatePickerInput,
)
from django_flatpickr.schemas import FlatpickrOptions
from django_select2 import forms as s2forms
from django.core.exceptions import ValidationError
from django.db.models import Q
from .tasks import calculate_total_days
from django.utils.translation import gettext_lazy as _
from account.custom_widgets import EmployeeWidget


class ALCalculateDateForm(forms.Form):
    date = forms.DateField(
        initial=date.today(),
        widget=DatePickerInput(
            attrs={"type": "date", "class": "w-full h-10 rounded-sm text-center"},
            options=FlatpickrOptions(),
        ),
    )


class CreateLeaveForm(forms.ModelForm):
    class Meta:
        model = Leave
        fields = (
            "employee",
            "leave_type",
            "start_date",
            "end_date",
            "half_day",
            "reason",
        )
        widgets = {
            "employee": EmployeeWidget,
            "leave_type": s2forms.Select2Widget(
                attrs={"class": "w-full"},
                choices=LeaveType.objects.all().values_list("id", "name"),
            ),
            "start_date": DatePickerInput(
                attrs={"type": "date", "class": "w-full h-10 rounded-sm"},
                options=FlatpickrOptions(),
            ),
            "end_date": DatePickerInput(
                attrs={"type": "date", "class": "w-full h-10 rounded-sm"},
                options=FlatpickrOptions(),
            ),
            "half_day": s2forms.Select2Widget(
                attrs={"class": "w-full"},
                choices=(
                    (None, ""),
                    (True, "Yes"),
                    (False, "No"),
                ),
            ),
            "reason": forms.Textarea(attrs={"rows": 3, "class": "w-full rounded-sm"}),
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
        qs = Leave.objects.filter(employee=employee).exclude(rejected=True)

        if employee:
            qs = Leave.objects.filter(employee=employee).exclude(rejected=True)
            active_leave = qs.filter(
                Q(start_date__lte=start_date, end_date__gte=start_date)
                | Q(start_date__lte=end_date, end_date__gte=end_date)
            ).exists()
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
                pass
                # employee_balance = employee.annual_leave_remaining
                # total_days = total_days.days + 1
                # if employee_balance < total_days:
                #     raise ValidationError(_("Insufficient annual leave balance."))
            else:
                maximum_days = leave_type.maximum_days
                if total_days > maximum_days:
                    raise ValidationError(
                        _("Total date is greater than the leave type's maximum date.")
                    )


class EditLeaveForm(forms.ModelForm):
    class Meta:
        model = Leave
        fields = (
            "leave_type",
            "start_date",
            "end_date",
            "half_day",
            "reason",
        )

        widgets = {
            "leave_type": s2forms.Select2Widget(
                attrs={"class": "w-full"},
                choices=LeaveType.objects.all().values_list("id", "name"),
            ),
            "start_date": DatePickerInput(
                attrs={"type": "date", "class": "w-full h-10 rounded-sm"},
                options=FlatpickrOptions(),
            ),
            "end_date": DatePickerInput(
                attrs={"type": "date", "class": "w-full h-10 rounded-sm"},
                options=FlatpickrOptions(),
            ),
            "half_day": s2forms.Select2Widget(
                attrs={"class": "w-full"},
                choices=(
                    (None, ""),
                    (True, "Yes"),
                    (False, "No"),
                ),
            ),
            "reason": forms.Textarea(attrs={"rows": 3, "class": "w-full  rounded-sm"}),
        }

    def clean(self):
        cleaned_data = super().clean()
        employee = self.instance.employee
        start_date = cleaned_data.get("start_date")
        end_date = cleaned_data.get("end_date")
        leave_type = cleaned_data.get("leave_type")
        half_day = cleaned_data.get("half_day")
        if not leave_type:
            raise ValidationError(_("Leave Type is required."))
        if employee:
            qs = (
                Leave.objects.filter(employee=employee)
                .exclude(id=self.instance.id)
                .exclude(rejected=True)
            )
            active_leave = qs.filter(
                Q(start_date__lte=start_date, end_date__gte=start_date)
                | Q(start_date__lte=end_date, end_date__gte=end_date)
            ).exists()
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
                pass
                # employee_balance = employee.annual_leave_remaining
                # total_days = total_days.days + 1
                # if employee_balance < total_days:
                #     raise ValidationError(_("Insufficient annual leave balance."))
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
            "annual",
            "exclude_rest_days",
            "half_day_leave",
            "paid",
            "description",
        )
        widgets = {
            "name": forms.TextInput(attrs={"class": "w-full rounded-sm"}),
            "maximum_days": forms.NumberInput(attrs={"class": "w-full rounded-sm"}),
            "paid": forms.CheckboxInput(),
            "description": forms.Textarea(
                attrs={"rows": 3, "class": "w-full rounded-sm"}
            ),
            "annual": s2forms.Select2Widget(
                attrs={"class": "w-full rounded-sm"},
                choices=(
                    (None, ""),
                    (True, "Yes"),
                    (False, "No"),
                ),
            ),
            "exclude_rest_days": s2forms.Select2Widget(
                attrs={"class": "w-full rounded-sm"},
                choices=(
                    (None, ""),
                    (True, "Yes"),
                    (False, "No"),
                ),
            ),
            "half_day_leave": s2forms.Select2Widget(
                attrs={"class": "w-full rounded-sm"},
                choices=(
                    (None, ""),
                    (True, "Yes"),
                    (False, "No"),
                ),
            ),
            "paid": s2forms.Select2Widget(
                attrs={"class": "w-full rounded-sm"},
                choices=(
                    (None, ""),
                    (True, "Yes"),
                    (False, "No"),
                ),
            ),
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
            "annual",
            "exclude_rest_days",
            "half_day_leave",
            "paid",
            "description",
        )
        widgets = {
            "name": forms.TextInput(attrs={"class": "w-full rounded-sm"}),
            "maximum_days": forms.NumberInput(attrs={"class": "w-full rounded-sm"}),
            "paid": forms.CheckboxInput(),
            "description": forms.Textarea(
                attrs={"rows": 3, "class": "w-full rounded-sm"}
            ),
            "annual": s2forms.Select2Widget(
                attrs={"class": "w-full rounded-sm"},
                choices=(
                    (None, ""),
                    (True, "Yes"),
                    (False, "No"),
                ),
            ),
            "exclude_rest_days": s2forms.Select2Widget(
                attrs={"class": "w-full rounded-sm"},
                choices=(
                    (None, ""),
                    (True, "Yes"),
                    (False, "No"),
                ),
            ),
            "half_day_leave": s2forms.Select2Widget(
                attrs={"class": "w-full rounded-sm"},
                choices=(
                    (None, ""),
                    (True, "Yes"),
                    (False, "No"),
                ),
            ),
            "paid": s2forms.Select2Widget(
                attrs={"class": "w-full rounded-sm"},
                choices=(
                    (None, ""),
                    (True, "Yes"),
                    (False, "No"),
                ),
            ),
        }

    def save(self, force_insert=False, force_update=False, commit=True):
        leave_type = LeaveType()
        leave_type.slug = slugify(leave_type.name)

        leave_type.save()

        return leave_type
