from asyncio.windows_events import NULL
from dataclasses import fields
from email.policy import default
from urllib import request
from colorama import init
from django import forms
from .models import Device, RawAttendance, Attendance, Shift, Employee, Pattern
from django.utils.text import slugify


class CreateDeviceForm(forms.Form):
    class Meta:
        model = Device()
        fields = ["name", "slug", "ip"]

    name = forms.CharField()
    ip = forms.CharField()

    def save(self, force_insert=False, force_update=False, commit=True):
        device = Device()
        device.slug = slugify(device.name)

        device.save()

        return device


class AttendanceFilterForm(forms.Form):
    class Meta:
        model = Attendance()
        fields = ["employee_id", "device_id"]

    employee_id = forms.IntegerField(required=False, initial=0)
    device_id = forms.IntegerField(required=False, initial=0)
    # date = forms.DateInput()


class CreateShiftForm(forms.Form):
    class Meta:
        model = Shift()
        fields = ["name", "continous", "saturday_half" ]

    name = forms.CharField()
    continous = forms.BooleanField(required=False)
    saturday_half = forms.BooleanField(required=False)

    def save(self, force_insert=False, force_update=False, commit=True):
        shift = Shift()
        shift.slug = slugify(shift.name)

        shift.save()

        return shift

class ChangeEmployeeStatusForm(forms.ModelForm):
    class Meta:
        model = Employee()
        fields = ['shift', 'pattern', 'last_updated']
        
    def __init__(self, *args, **kwargs):
        super(ChangeEmployeeStatusForm, self).__init__(*args, **kwargs)
        self.fields['shift'].queryset = Shift.objects.all()
        self.fields['pattern'].queryset = Pattern.objects.filter(shift=self.instance.shift)
        if self.instance.shift:
            self.fields['shift'].initial = Shift.objects.get(id=self.instance.shift.id)
        if self.instance.pattern:
            self.fields['pattern'].initial = Pattern.objects.get(id=self.instance.pattern.id)
    
    shift = forms.ModelChoiceField(Shift.objects.all())
    pattern = forms.ModelChoiceField(Pattern.objects.all())
    last_updated = forms.DateField(required=False)
    
        