from .models import *
from employee.models import *
from django import forms
from django.contrib.auth.models import User
from django_select2 import forms as s2forms
from device.models import Device
from qual.custom_widgets import DeviceWidget, EmployeeWidget

widget_attr = {"class": "w-full rounded-sm"}


class CreateUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
        )
        widgets = {
            "username": forms.TextInput(attrs=widget_attr),
            "email": forms.EmailInput(attrs=widget_attr),
            "first_name": forms.TextInput(attrs=widget_attr),
            "last_name": forms.TextInput(attrs=widget_attr),
        }

    password = forms.CharField(
        label="Password", widget=forms.PasswordInput(attrs=widget_attr)
    )
    confirm_password = forms.CharField(
        label="Confirm password", widget=forms.PasswordInput(attrs=widget_attr)
    )

    def clean_confirm_password(self):
        password = self.cleaned_data.get("password")
        confirm_password = self.cleaned_data.get("confirm_password")
        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match")
        return confirm_password


class EditUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "email",
            "is_active",
        )
        widgets = {
            "email": forms.EmailInput(attrs=widget_attr),
            "first_name": forms.TextInput(attrs=widget_attr),
            "last_name": forms.TextInput(attrs=widget_attr),
            "is_active": s2forms.Select2Widget(
                attrs=widget_attr,
                choices=(
                    (None, ""),
                    (True, "Yes"),
                    (False, "No"),
                ),
            ),
        }

    # def __init__(self, *args, **kwargs):
    #     super(EditUserForm, self).__init__(*args, **kwargs)

    #     for fieldname in ["email", "is_active"]:
    #         self.fields[fieldname].help_text = None


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = (
            "role",
            "device",
            "employee",
            "manages",
        )
        widgets = {
            "role": s2forms.Select2Widget(
                attrs=widget_attr,
                choices=(
                    ("USER", "USER"),
                    ("HR", "HR"),
                    ("ADMIN", "ADMIN"),
                    ("MANAGER", "MANAGER"),
                ),
            ),
            "device": DeviceWidget,
            "employee": EmployeeWidget,
            "manages": s2forms.ModelSelect2MultipleWidget(
                attrs=widget_attr,
                queryset=Department.objects.all(),
                search_fields=[
                    "code__icontains",
                    "name__icontains",
                ],
            ),
        }

    def __init__(self, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.fields["employee"].queryset = Employee.objects.filter(
            status="Active"
        ).order_by("name")
        # self.fields["employee"].initial = self.instance.employee


class EditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = (
            "email",
            "first_name",
            "last_name",
        )
        widgets = {
            "email": forms.EmailInput(attrs=widget_attr),
            "first_name": forms.TextInput(attrs=widget_attr),
            "last_name": forms.TextInput(attrs=widget_attr),
        }


class SelectDeviceForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ("device",)
        widgets = {
            "device": s2forms.Select2Widget(
                attrs=widget_attr,
                choices=Device.objects.all().values_list("id", "name"),
            ),
        }
