from .models import *
from django.utils.text import slugify
from django import forms
from django_flatpickr.widgets import (
    DatePickerInput,
    TimePickerInput,
    DateTimePickerInput,
)
from django_flatpickr.schemas import FlatpickrOptions


class CreateHolidayForm(forms.ModelForm):
    class Meta:
        model = Holiday
        fields = (
            "name",
            "date",
            "description",
        )

        widgets = {
            "name": forms.TextInput(attrs={"class": "w-full rounded-sm"}),
            "date": DatePickerInput(
                attrs={"type": "date", "class": "w-full h-10 rounded-sm"},
                options=FlatpickrOptions(),
            ),
            "description": forms.Textarea(
                attrs={"rows": 3, "class": "w-full rounded-sm"}
            ),
        }

    # date = forms.DateField(widget=forms.DateInput(attrs={"type": "date"}))

    def save(self, force_insert=False, force_update=False, commit=True):
        holiday = Holiday()
        holiday.slug = slugify(holiday.name)

        holiday.save()

        return holiday
