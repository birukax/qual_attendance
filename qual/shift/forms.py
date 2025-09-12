from django import forms
from .models import Shift, Pattern
from employee.models import Employee
from django.utils.text import slugify
from django_flatpickr.widgets import (
    DatePickerInput,
    TimePickerInput,
    DateTimePickerInput,
)
from django_select2 import forms as s2forms
from django_flatpickr.schemas import FlatpickrOptions
from account.custom_widgets import DeviceWidget, ShiftWidget, PatternWidget
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class CreateShiftForm(forms.ModelForm):
    class Meta:
        model = Shift
        fields = (
            "name",
            "device",
            "saturday_half",
            "continous",
        )
        widgets = {
            "name": forms.TextInput(attrs={"class": "w-full rounded-sm"}),
            "device": DeviceWidget,
            "saturday_half": s2forms.Select2Widget(
                attrs={"class": "w-full"},
                choices=(
                    (None, ""),
                    (True, "Yes"),
                    (False, "No"),
                ),
            ),
            "continous": s2forms.Select2Widget(
                attrs={"class": "w-full"},
                choices=(
                    (None, ""),
                    (True, "Yes"),
                    (False, "No"),
                ),
            ),
        }
        labels = {
            "continous": "Continuous",
        }

    def save(self, force_insert=False, force_update=False, commit=True):
        shift = Shift
        shift.slug = slugify(shift.name)

        shift.save()

        return shift


class SelectEmployeesForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ["employees"]

    employees = forms.ModelMultipleChoiceField(
        queryset=Employee.objects.filter(status="Active"),
        widget=forms.CheckboxSelectMultiple,
    )


class SelectShiftForm(forms.Form):
    # class Meta:
    #     model = Shift
    #     fields = ["id"]

    shift = forms.ModelChoiceField(
        Shift.objects.all(), label="Shift", widget=ShiftWidget
    )


class EditShiftForm(forms.ModelForm):
    class Meta:
        model = Shift
        fields = (
            "name",
            "device",
            "current_pattern",
            "continous",
            "saturday_half",
        )
        widgets = {
            "name": forms.TextInput(attrs={"class": "w-full rounded-sm"}),
            "device": DeviceWidget,
            "current_pattern": PatternWidget,
            "continous": s2forms.Select2Widget(
                attrs={"class": "w-full rounded-sm"},
                choices=(
                    (None, ""),
                    (True, "Yes"),
                    (False, "No"),
                ),
            ),
            "saturday_half": s2forms.Select2Widget(
                attrs={"class": "w-full rounded-sm"},
                choices=(
                    (None, ""),
                    (True, "Yes"),
                    (False, "No"),
                ),
            ),
        }

        labels = {
            "continous": "Continuous",
        }

    def save(self, force_insert=False, force_update=False, commit=True):
        shift = super(EditShiftForm, self).save(commit=False)
        shift.slug = slugify(shift.name)
        shift.save()
        return shift

    def __init__(self, *args, **kwargs):
        super(EditShiftForm, self).__init__(*args, **kwargs)
        self.fields["current_pattern"].queryset = Pattern.objects.filter(
            shift__id=self.instance.id
        )


class CreatePatternForm(forms.ModelForm):
    class Meta:
        model = Pattern
        fields = (
            "name",
            "next",
            "tolerance",
            "day_span",
            "start_time",
            "end_time",
        )
        widgets = {
            "name": forms.TextInput(attrs={"class": "w-full rounded-sm"}),
            "next": forms.Select(attrs={"class": "w-full h-10 rounded-sm"}),
            "tolerance": forms.NumberInput(attrs={"class": "w-full rounded-sm"}),
            "day_span": forms.NumberInput(attrs={"class": "w-full rounded-sm"}),
            "start_time": TimePickerInput(
                attrs={"type": "date", "class": "w-full h-10 rounded-sm"},
                options=FlatpickrOptions(),
            ),
            "end_time": TimePickerInput(
                attrs={"type": "date", "class": "w-full h-10 rounded-sm"},
                options=FlatpickrOptions(),
            ),
        }

    def __init__(self, shift, *args, **kwargs):
        super(CreatePatternForm, self).__init__(*args, **kwargs)
        self.fields["next"].queryset = Pattern.objects.filter(shift=shift)

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get("name")
        next = cleaned_data.get("next")
        start_time = cleaned_data.get("start_time")
        end_time = cleaned_data.get("end_time")
        tolerance = cleaned_data.get("tolerance")
        day_span = cleaned_data.get("day_span")
        if start_time and end_time and day_span:
            if start_time > end_time and day_span < 2:
                raise ValidationError(_("Start Time cannot be greater than End Time."))
        if tolerance and day_span:
            if tolerance > 120:
                raise ValidationError(
                    _("Tolerance cannot be greater than 120 minutes.")
                )

            if day_span > 2:
                raise ValidationError(_("Day Span cannot be greater than 2 days."))

    def save(self, force_insert=False, force_update=False, commit=True):
        pattern = Pattern
        pattern.slug = slugify(pattern.name)
        pattern.save()
        return pattern


class EditPatternForm(forms.ModelForm):
    class Meta:
        model = Pattern
        fields = (
            "name",
            "next",
            "day_span",
            "tolerance",
            "start_time",
            "end_time",
        )
        widgets = {
            "name": forms.TextInput(attrs={"class": "w-full rounded-sm"}),
            "next": forms.Select(attrs={"class": "w-full h-10 rounded-sm"}),
            "day_span": forms.NumberInput(attrs={"class": "w-full rounded-sm"}),
            "tolerance": forms.NumberInput(attrs={"class": "w-full rounded-sm"}),
            "start_time": TimePickerInput(
                attrs={"type": "date", "class": "w-full h-10 rounded-sm"},
                options=FlatpickrOptions(),
            ),
            "end_time": TimePickerInput(
                attrs={"type": "date", "class": "w-full h-10 rounded-sm"},
                options=FlatpickrOptions(),
            ),
        }

    def __init__(self, *args, **kwargs):
        super(EditPatternForm, self).__init__(*args, **kwargs)
        self.fields["next"].queryset = Pattern.objects.filter(shift=self.instance.shift)

    def save(self, force_insert=False, force_update=False, commit=True):
        pattern = super(EditPatternForm, self).save(commit=False)
        pattern.slug = slugify(pattern.name)
        pattern.save()
        return pattern


# class ChangePatternForm(forms.ModelForm):
#     class Meta:
#         model = Shift()
#         fields = [
#             "current_pattern",
#         ]

#     def __init__(self, *args, **kwargs):
#         super(ChangePatternForm, self).__init__(*args, **kwargs)
#         self.fields["current_pattern"].queryset = Pattern.objects.filter(
#             shift__id=self.instance.id,
#         )
