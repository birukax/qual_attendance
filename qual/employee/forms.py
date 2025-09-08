from django import forms
from .models import Employee
from shift.models import Shift
from device.models import Device
from qual.custom_widgets import ShiftWidget, DeviceWidget


class ChangeEmployeeShiftForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ("device", "shift")

    device = forms.ModelChoiceField(
        queryset=Device.objects.all(),
        widget=DeviceWidget(),
    )

    shift = forms.ModelChoiceField(
        queryset=Shift.objects.all(),
        widget=ShiftWidget(),
    )
    # def __init__(self, *args, **kwargs):
    #     super(ChangeEmployeeShiftForm, self).__init__(*args, **kwargs)
    #     self.fields["shift"].queryset = Shift.objects.all()
    #     if self.instance.shift:
    #         self.fields["shift"].initial = Shift.objects.get(id=self.instance.shift.id)

    # shift = forms.ModelChoiceField(Shift.objects.all())
    # device = forms.ModelChoiceField(Device.objects.all())
