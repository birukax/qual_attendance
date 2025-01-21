from django.contrib import admin
from .models import Attendance, RawAttendance, DailyRecord


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "employee",
        "device",
        "current_pattern",
        "worked_hours",
        "check_in_date",
        "check_in_time",
        "check_out_date",
        "check_out_time",
        "leave_type",
        "check_in_type",
        "check_out_type",
        "status",
        "approved",
        "deleted",
        "recompiled",
    ]
    list_per_page = 50
    list_filter = ["status", "approved", "recompiled", "deleted"]


@admin.register(RawAttendance)
class RawAttendanceAdmin(admin.ModelAdmin):
    list_display = ["uid", "device", "employee", "date", "time", "status", "punch"]
    list_filter = ["date", "device"]
    search_fields = ["employee__name"]
    list_per_page = 50


@admin.register(DailyRecord)
class DailyRecordAdmin(admin.ModelAdmin):
    list_display = [
        "date",
        "attendances",
        "early_check_in",
        "late_check_in",
        "early_check_out",
        "late_check_out",
        "absent",
        "day_off",
        "leave",
    ]
    list_per_page = 50
