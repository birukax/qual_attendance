import django_filters
import django_filters.widgets
from .models import Overtime


class OvertimeDownloadFilter(django_filters.FilterSet):
    class Meta:
        model = Overtime
        fields = {
            "employee__name": ["icontains"],
            "approved": ["exact"],
            "paid": ["exact"],
            "rejected": ["exact"],
        }


class OvertimeFilter(django_filters.FilterSet):
    class Meta:
        model = Overtime
        fields = {
            "employee__name": ["icontains"],
            "paid": ["exact"],
            "approved": ["exact"],
            "rejected": ["exact"],
        }
