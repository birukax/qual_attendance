import django_filters
from employee.models import Employee
from device.models import Device
from shift.models import Pattern, Shift
from .models import Attendance, RawAttendance
from django_select2 import forms as s2forms
from qual.custom_widgets import EmployeeWidget, DeviceWidget, PatternWidget, ShiftWidget


# class AttendanceDownloadFilter(django_filters.FilterSet):
#     class Meta:
#         model = Attendance
#         fields = {
#             "employee",
#             "device",
#             "current_pattern__shift",
#             "status",
#             "check_in_type",
#             "check_out_type",
#             "check_in_date",
#         }

#     check_in_date = django_filters.DateFromToRangeFilter(
#         widget=django_filters.widgets.DateRangeWidget(attrs={"type": "date"})
#     )

# status = django_filters.ChoiceFilter(choices=Attendance.CHOICES)


# class CompiledAttendanceDownloadFilter(django_filters.FilterSet):
#     class Meta:
#         model = Attendance
#         fields = (
#             "employee",
#             "current_pattern__shift",
#             "current_pattern",
#             "status",
#             "check_in_type",
#             "check_out_type",
#         )

# status = django_filters.ChoiceFilter(choices=Attendance.CHOICES)


class AttendanceFilter(django_filters.FilterSet):
    class Meta:
        model = Attendance
        fields = (
            "employee",
            "device",
            "current_pattern__shift",
            "current_pattern",
            "status",
            "check_in_type",
            "check_out_type",
            "check_in_date",
        )

    check_in_date = django_filters.DateFromToRangeFilter(
        label="Check-in Date",
        widget=django_filters.widgets.DateRangeWidget(
            attrs={"type": "date", "class": "w-full h-10 rounded-sm"}
        ),
    )
    employee = django_filters.ModelChoiceFilter(
        queryset=Employee.objects.all(),
        label="Employee",
        lookup_expr="exact",
        widget=EmployeeWidget(),
    )

    device = django_filters.ModelChoiceFilter(
        queryset=Device.objects.all(),
        label="Device",
        lookup_expr="exact",
        widget=DeviceWidget(),
    )
    current_pattern__shift = django_filters.ModelChoiceFilter(
        queryset=Shift.objects.all(),
        label="Shift",
        lookup_expr="exact",
        widget=ShiftWidget(),
    )
    current_pattern = django_filters.ModelChoiceFilter(
        queryset=Pattern.objects.all(),
        label="Current Pattern",
        lookup_expr="exact",
        widget=PatternWidget(),
    )
    status = django_filters.CharFilter(
        label="Status",
        lookup_expr="exact",
        widget=s2forms.Select2Widget(
            attrs={"class": "w-full"},
            choices=(
                ("", "-------"),
                ("Checked", "Checked"),
                ("No Data", "No Data"),
                ("Absent", "Absent"),
                ("Day Off", "Day Off"),
                ("On Leave", "On Leave"),
                ("On Field", "On Field"),
                ("Holiday", "Holiday"),
            ),
        ),
    )
    check_in_type = django_filters.CharFilter(
        label="Check-in Type",
        lookup_expr="exact",
        widget=s2forms.Select2Widget(
            attrs={"class": "w-full"},
            choices=(
                ("", "-------"),
                ("Late", "Late"),
                ("Early", "Early"),
                ("On Time", "On Time"),
                ("No Data", "No Data"),
            ),
        ),
    )

    check_out_type = django_filters.CharFilter(
        label="Check-out Type",
        lookup_expr="exact",
        widget=s2forms.Select2Widget(
            attrs={"class": "w-full"},
            choices=(
                ("", "-------"),
                ("Late", "Late"),
                ("Early", "Early"),
                ("On Time", "On Time"),
                ("No Data", "No Data"),
            ),
        ),
    )


class CompileFilter(django_filters.FilterSet):
    class Meta:
        model = Attendance
        fields = (
            "employee",
            "current_pattern__shift",
            "current_pattern",
            "status",
            "check_in_type",
            "check_out_type",
        )

    employee = django_filters.ModelChoiceFilter(
        queryset=Employee.objects.all(),
        label="Employee",
        lookup_expr="exact",
        widget=EmployeeWidget(),
    )
    current_pattern__shift = django_filters.ModelChoiceFilter(
        queryset=Shift.objects.all(),
        label="Shift",
        lookup_expr="exact",
        widget=ShiftWidget(),
    )
    current_pattern = django_filters.ModelChoiceFilter(
        queryset=Pattern.objects.all(),
        label="Current Pattern",
        lookup_expr="exact",
        widget=PatternWidget(),
    )
    status = django_filters.CharFilter(
        label="Status",
        lookup_expr="exact",
        widget=s2forms.Select2Widget(
            attrs={"class": "w-full"},
            choices=(
                ("", "-------"),
                ("Checked", "Checked"),
                ("No Data", "No Data"),
                ("Absent", "Absent"),
                ("Day Off", "Day Off"),
                ("On Leave", "On Leave"),
                ("On Field", "On Field"),
                ("Holiday", "Holiday"),
            ),
        ),
    )
    check_in_type = django_filters.CharFilter(
        label="Check-in Type",
        lookup_expr="exact",
        widget=s2forms.Select2Widget(
            attrs={"class": "w-full"},
            choices=(
                ("", "-------"),
                ("Late", "Late"),
                ("Early", "Early"),
                ("On Time", "On Time"),
                ("No Data", "No Data"),
            ),
        ),
    )

    check_out_type = django_filters.CharFilter(
        label="Check-out Type",
        lookup_expr="exact",
        widget=s2forms.Select2Widget(
            attrs={"class": "w-full"},
            choices=(
                ("", "-------"),
                ("Late", "Late"),
                ("Early", "Early"),
                ("On Time", "On Time"),
                ("No Data", "No Data"),
            ),
        ),
    )


class RawAttendanceFilter(django_filters.FilterSet):
    class Meta:
        model = RawAttendance
        fields = (
            "employee",
            "date",
        )

    employee = django_filters.ModelChoiceFilter(
        queryset=Employee.objects.all(),
        label="Name",
        lookup_expr="exact",
        widget=EmployeeWidget(),
    )
    date = django_filters.DateFromToRangeFilter(
        widget=django_filters.widgets.DateRangeWidget(
            attrs={"type": "date", "class": "w-full h-10 rounded-sm"}
        )
    )
