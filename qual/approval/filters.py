import django_filters
from django_select2 import forms as s2forms
import django_filters.widgets
from leave.models import Leave
from overtime.models import Overtime
from holiday.models import Holiday


class LeaveFilter(django_filters.FilterSet):
    class Meta:
        model = Leave
        fields = {
            "employee__name": ["icontains"],
            "leave_type": ["exact"],
            "half_day": ["exact"],
            "start_date": ["exact"],
        }

    start_date = django_filters.DateFromToRangeFilter(
        widget=django_filters.widgets.DateRangeWidget(
            attrs={"type": "date", "class": "w-full h-10 rounded-sm"}
        ),
    )


class OvertimeFilter(django_filters.FilterSet):
    class Meta:
        model = Overtime
        fields = {
            "employee__name": ["icontains"],
        }


class HolidayFilter(django_filters.FilterSet):
    class Meta:
        model = Holiday
        fields = (
            "name",
            "date",
        )

    name = django_filters.CharFilter(
        label="Name",
        lookup_expr="exact",
        widget=s2forms.Select2Widget(
            attrs={"class": "w-full"},
            choices=Holiday.objects.filter(approved=False, rejected=False).values_list(
                "name", "name"
            ),
        ),
    )

    date = django_filters.DateFromToRangeFilter(
        label="Date",
        widget=django_filters.widgets.DateRangeWidget(
            attrs={"type": "date", "class": "w-full h-10 rounded-sm"}
        ),
    )
