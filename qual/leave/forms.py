from .models import *
from django import forms
from django.utils.text import slugify
from employee.models import Employee



class CreateLeaveForm(forms.ModelForm):
    class Meta:
        model = Leave
        fields = ( 'employee', 'leave_type', 'start_date', 'end_date', 'is_half_day', 'evidence', 'reason')
        
    def __init__(self, *args, **kwargs):
        super(CreateLeaveForm, self).__init__(*args, **kwargs)
        self.fields['employee'].queryset = Employee.objects.all().order_by('name')
        self.fields['leave_type'].queryset = LeaveType.objects.all()
        self.fields['evidence'].required = False
        
        
class CreateLeaveTypeForm(forms.ModelForm):
    class Meta:
        model = LeaveType
        fields = ('name',  'maximum_days', 'description', 'paid')
        
        
    def save(self, force_insert=False, force_update=False, commit=True):
        leave_type = LeaveType()
        leave_type.slug = slugify(leave_type.name)

        leave_type.save()

        return leave_type
    
class EditLeaveTypeForm(forms.ModelForm):
    class Meta:
        model = LeaveType
        fields = ('name', 'maximum_days', 'description', 'paid')
        
        
    def save(self, force_insert=False, force_update=False, commit=True):
        leave_type = LeaveType()
        leave_type.slug = slugify(leave_type.name)

        leave_type.save()

        return leave_type