from django import forms
from .models import Device
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
