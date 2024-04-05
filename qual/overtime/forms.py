from django import forms
from .models import *


class CreateOvertimeTypeForm(forms.ModelForm):
    class Meta:
        model = OvertimeType
        fields = (
            "name",
            "day_span",
            "days",
            "start_time",
            "end_time",
            "pay_item_code",
        )


class EditOvertimeTypeForm(forms.ModelForm):
    class Meta:
        model = OvertimeType
        fields = (
            "name",
            "day_span",
            "start_time",
            "end_time",
        )


class CreateOvertimeForm(forms.ModelForm):
    class Meta:
        model = Overtime
        fields = (
            "employee",
            "start_date",
            "end_date",
            "start_time_expected",
            "end_time_expected",
            "reason",
        )
