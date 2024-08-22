from django.forms import DateInput
import django_filters
from .models import Attendance, RawAttendance, OnField
from django_select2 import forms as s2forms


class EmployeeWidget(s2forms.ModelSelect2Widget):
    search_fields = ["name__icontains", "employee_id__icontains"]


class AttendanceDownloadFilter(django_filters.FilterSet):
    class Meta:
        model = Attendance
        fields = {
            "employee__name": ["icontains"],
            "device": ["exact"],
            "current_pattern__shift": ["exact"],
            "status": ["exact"],
            "check_in_type": ["exact"],
            "check_out_type": ["exact"],
            "check_in_date": ["exact"],
        }

    check_in_date = django_filters.DateFromToRangeFilter(
        widget=django_filters.widgets.RangeWidget(attrs={"type": "date"})
    )

    # status = django_filters.ChoiceFilter(choices=Attendance.CHOICES)


class CompiledAttendanceDownloadFilter(django_filters.FilterSet):
    class Meta:
        model = Attendance
        fields = {
            "employee__name": ["icontains"],
            "device": ["exact"],
            "current_pattern__shift": ["exact"],
            "status": ["exact"],
            "check_in_type": ["exact"],
            "check_out_type": ["exact"],
        }

    # status = django_filters.ChoiceFilter(choices=Attendance.CHOICES)


class AttendanceFilter(django_filters.FilterSet):
    class Meta:
        model = Attendance
        fields = {
            "employee__name": ["icontains"],
            "device": ["exact"],
            "current_pattern": ["exact"],
            "status": ["exact"],
            "check_in_type": ["exact"],
            "check_out_type": ["exact"],
        }

    check_in_date = django_filters.DateFromToRangeFilter(
        widget=django_filters.widgets.RangeWidget(attrs={"type": "date"})
    )


class CompileFilter(django_filters.FilterSet):
    class Meta:
        model = Attendance
        fields = {
            "employee__name": ["icontains"],
            "device": ["exact"],
            "current_pattern": ["exact"],
            "status": ["exact"],
            "check_in_type": ["exact"],
            "check_out_type": ["exact"],
        }


class RawAttendanceFilter(django_filters.FilterSet):
    class Meta:
        model = RawAttendance
        fields = {
            "employee__name": ["icontains"],
            "date": ["exact"],
        }

    date = django_filters.DateFromToRangeFilter(
        widget=django_filters.widgets.RangeWidget(attrs={"type": "date"})
    )


class OnFieldFilter(django_filters.FilterSet):
    class Meta:
        model = OnField
        fields = {
            "employee__name": ["icontains"],
            "approved": ["exact"],
            "rejected": ["exact"],
            "start_date": ["exact"],
        }

    start_date = django_filters.DateFromToRangeFilter(
        widget=django_filters.widgets.RangeWidget(attrs={"type": "date"})
    )
