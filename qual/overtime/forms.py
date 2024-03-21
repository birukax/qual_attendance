from django import forms
from .models import *


class CreateOvertimeTypeForm(forms.ModelForm):
    class Meta:
        model = OvertimeType
        fields = (
            "name",
            "rate",
            "day_span",
            "description",
        )


class EditOvertimeTypeForm(forms.ModelForm):
    class Meta:
        model = OvertimeType
        fields = (
            "name",
            "rate",
            "day_span",
            "description",
        )


class CreateOvertimeForm(forms.ModelForm):
    class Meta:
        model = Overtime
        fields = (
            "employee",
            "overtime_type",
            "start_date",
            "end_date",
            "start_time_expected",
            "end_time_expected",
            "reason",
        )
