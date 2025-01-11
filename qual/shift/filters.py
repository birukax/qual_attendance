import django_filters
import django_filters.widgets
from .models import Shift


class ShiftFilter(django_filters.FilterSet):
    class Meta:
        model = Shift
        fields = {
            "name": ["icontains"],
            "device": ["exact"],
            "continous": ["exact"],
            "saturday_half": ["exact"],
        }
