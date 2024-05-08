from django import forms
from .models import *
from employee.models import Employee
from django.utils.text import slugify

from django_flatpickr.widgets import (
    DatePickerInput,
    TimePickerInput,
    DateTimePickerInput,
)
from django_flatpickr.schemas import FlatpickrOptions


class CreateShiftForm(forms.ModelForm):
    class Meta:
        model = Shift
        fields = (
            "name",
            "device",
            "saturday_half",
            "continous",
        )

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
    class Meta:
        model = Shift
        fields = ["name"]

    shift = forms.ModelChoiceField(Shift.objects.all())


class EditShiftForm(forms.ModelForm):
    class Meta:
        model = Shift
        fields = (
            "name",
            "device",
            "continous",
            "current_pattern",
            "saturday_half",
        )

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
            "start_time",
            "end_time",
            "tolerance",
            "day_span",
        )
        widgets = {
            "start_time": TimePickerInput(options=FlatpickrOptions()),
            "end_time": TimePickerInput(options=FlatpickrOptions()),
        }

    def __init__(self, shift, *args, **kwargs):
        super(CreatePatternForm, self).__init__(*args, **kwargs)
        self.fields["next"].queryset = Pattern.objects.filter(shift=shift)

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
            "start_time": TimePickerInput(options=FlatpickrOptions()),
            "end_time": TimePickerInput(options=FlatpickrOptions()),
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
