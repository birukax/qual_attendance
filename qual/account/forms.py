from .models import *
from employee.models import *
from django import forms
from django.contrib.auth.models import User


class CreateUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "first_name",
            "last_name",
        ]

    password = forms.CharField(label="Password", widget=forms.PasswordInput)
    confirm_password = forms.CharField(
        label="Confirm password", widget=forms.PasswordInput
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
        fields = ["email", "first_name", "last_name", "is_active"]

    def __init__(self, *args, **kwargs):
        super(EditUserForm, self).__init__(*args, **kwargs)

        for fieldname in ["email", "is_active"]:
            self.fields[fieldname].help_text = None


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["role", "employee", "manages"]

    def __init__(self, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.fields["employee"].queryset = Employee.objects.filter(
            status="Active"
        ).order_by("name")
        # self.fields["employee"].initial = self.instance.employee


class EditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            "email",
            "first_name",
            "last_name",
        ]
