from .models import *
from django.utils.text import slugify
from django import forms


class CreateHolidayForm(forms.ModelForm):
    class Meta:
        model = Holiday
        fields = ("name", "date", "description")

    name = forms.CharField(max_length=100)
    date = forms.DateField(widget=forms.DateInput(attrs={"type": "date"}))
    description = forms.Textarea()

    def save(self, force_insert=False, force_update=False, commit=True):
        holiday = Holiday()
        holiday.slug = slugify(holiday.name)

        holiday.save()

        return holiday
