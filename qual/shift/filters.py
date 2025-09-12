import django_filters
from .models import Shift
from django_select2 import forms as s2forms
from device.models import Device
from account.custom_widgets import DeviceWidget


class ShiftFilter(django_filters.FilterSet):
    class Meta:
        model = Shift
        fields = (
            "id",
            "device",
            "continous",
            "saturday_half",
        )

    id = django_filters.CharFilter(
        label="name",
        lookup_expr="exact",
        widget=s2forms.Select2Widget(
            attrs={"class": "w-full"},
            choices=Shift.objects.all().values_list("id", "name"),
        ),
    )
    device = django_filters.ModelChoiceFilter(
        queryset=Device.objects.all(),
        label="Device",
        lookup_expr="exact",
        widget=DeviceWidget(),
    )
    continous = django_filters.BooleanFilter(
        label="Continuous",
        lookup_expr="exact",
        widget=s2forms.Select2Widget(
            attrs={"class": "w-full"},
            choices=(
                (None, ""),
                (True, "Yes"),
                (False, "No"),
            ),
        ),
    )

    saturday_half = django_filters.BooleanFilter(
        label="Saturday Half",
        lookup_expr="exact",
        widget=s2forms.Select2Widget(
            attrs={"class": "w-full"},
            choices=(
                (None, ""),
                (True, "Yes"),
                (False, "No"),
            ),
        ),
    )
