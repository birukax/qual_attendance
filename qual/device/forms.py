from django import forms
from .models import Device, DeviceUser
from django.utils.text import slugify
from account.custom_widgets import DeviceWidget


class CreateDeviceForm(forms.ModelForm):
    class Meta:
        model = Device
        fields = (
            "name",
            "ip",
        )
        widgets = {
            "name": forms.TextInput(attrs={"class": "w-full rounded-sm"}),
            "ip": forms.TextInput(attrs={"class": "w-full rounded-sm"}),
        }

    def save(self, force_insert=False, force_update=False, commit=True):
        device = Device()
        device.slug = slugify(device.name)

        device.save()

        return device


class AddDeviceUserForm(forms.ModelForm):
    class Meta:
        model = DeviceUser
        fields = ("device",)

    device = forms.ModelChoiceField(
        queryset=Device.objects.all(),
        label="Device",
        widget=DeviceWidget(),
    )
