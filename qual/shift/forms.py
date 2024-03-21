# from asyncio.windows_events import NULL
from dataclasses import fields
from email.policy import default
from urllib import request
from colorama import init
from django import forms
from .models import *
from employee.models import Employee
from django.utils.text import slugify
import datetime


class CreateShiftForm(forms.Form):
    class Meta:
        model = Shift()
        fields = [
            "name",
            "continous",
            "saturday_half",
        ]

    name = forms.CharField()
    continous = forms.BooleanField(required=False)
    saturday_half = forms.BooleanField(required=False)

    def save(self, force_insert=False, force_update=False, commit=True):
        shift = Shift()
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
        model = Shift()
        fields = ["name", "continous", "saturday_half", "current_pattern"]

    name = forms.CharField()
    continous = forms.BooleanField(required=False)
    saturday_half = forms.BooleanField(required=False)

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


class CreatePatternForm(forms.Form):
    class Meta:
        model = Pattern()
        fields = ["name", "day_span", "tolerance", "start_time", "end_time"]

    name = forms.CharField()
    day_span = forms.IntegerField()
    tolerance = forms.IntegerField()
    next = forms.ModelChoiceField(
        Pattern.objects.all(), required=False, empty_label=None, label="Next Pattern"
    )
    start_time = forms.TimeField()
    end_time = forms.TimeField()

    def __init__(self, shift, *args, **kwargs):
        super(CreatePatternForm, self).__init__(*args, **kwargs)
        self.fields["next"].queryset = Pattern.objects.filter(shift=shift)

    def save(self, force_insert=False, force_update=False, commit=True):
        pattern = Pattern()
        pattern.slug = slugify(pattern.name)
        pattern.save()
        return pattern


class EditPatternForm(forms.ModelForm):
    class Meta:
        model = Pattern()
        fields = ["name", "day_span", "tolerance", "start_time", "end_time"]

    next = forms.ModelChoiceField(
        Pattern.objects.all(), required=False, empty_label=None, label="Next Pattern"
    )
    start_time = forms.TimeField()
    end_time = forms.TimeField()
    tolerance = forms.IntegerField()
    day_span = forms.IntegerField()

    def __init__(self, *args, **kwargs):
        super(EditPatternForm, self).__init__(*args, **kwargs)
        self.fields["next"].queryset = Pattern.objects.filter(shift=self.instance.shift)

    def save(self, force_insert=False, force_update=False, commit=True):
        pattern = super(EditPatternForm, self).save(commit=False)
        pattern.slug = slugify(pattern.name)
        pattern.save()
        return pattern


class ChangeEmployeeShiftForm(forms.ModelForm):
    class Meta:
        model = Employee()
        fields = [
            "shift",
        ]

    def __init__(self, *args, **kwargs):
        super(ChangeEmployeeShiftForm, self).__init__(*args, **kwargs)
        self.fields["shift"].queryset = Shift.objects.all()
        if self.instance.shift:
            self.fields["shift"].initial = Shift.objects.get(id=self.instance.shift.id)

    shift = forms.ModelChoiceField(Shift.objects.all())


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
