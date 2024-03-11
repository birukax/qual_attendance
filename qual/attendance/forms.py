#from asyncio.windows_events import NULL
from dataclasses import fields
from email.policy import default
from urllib import request
from colorama import init
from django import forms
from .models import *
from django.utils.text import slugify
import datetime

class AttendanceDownloadForm(forms.Form):
    class Meta:
        model = Attendance()
        fields = ["employee", "device", "current_pattern"]
    
    def __init__(self, *args, **kwargs):
        super(AttendanceDownloadForm, self).__init__(*args, **kwargs)
        self.fields['employee'].initial = Employee.objects.all()
        self.fields['device'].initial = Device.objects.all()
        self.fields['current_pattern'].initial = Pattern.objects.all()
        self.fields['start_date'].initial = datetime.date.today()
        self.fields['end_date'].initial = datetime.date.today()

    employee = forms.ModelChoiceField(Employee.objects.all(), required=False)
    device = forms.ModelChoiceField(Device.objects.all(), required=False)
    current_pattern = forms.ModelChoiceField(Pattern.objects.all(), required=False)
    start_date = forms.DateField()
    end_date = forms.DateField()

class SyncEmployeeAttendanceForm(forms.Form):
    
    end_date = forms.DateField(initial=datetime.date.today())
