import django_filters
import django_filters.widgets
from leave.models import Leave
from overtime.models import Overtime


class LeaveFilter(django_filters.FilterSet):
    class Meta:
        model = Leave
        fields = {
            "employee__name": ["icontains"],
            "leave_type": ["exact"],
            "half_day": ["exact"],
        }


class OvertimeFilter(django_filters.FilterSet):
    class Meta:
        model = Overtime
        fields = {
            "employee__name": ["icontains"],
        }
