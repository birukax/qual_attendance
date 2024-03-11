from django.contrib import admin
from .models import *


@admin.register(OvertimeType)
class OvertimeTypeAdmin(admin.ModelAdmin):
    list_display = ["name", "rate", "slug", "day_span"]
    prepopulated_fields = {"slug": ("name",)}
    list_per_page = 15


@admin.register(Overtime)
class OvertimeAdmin(admin.ModelAdmin):
    list_display = [
        "employee",
        "overtime_type",
        "start_date",
        "end_date",
        "worked_hours",
        "approved",
        "start_time_expected",
        "start_time_expected",
        # "end_time_actual",
        # "end_time_actual",
        "total_rate",
    ]
    list_per_page = 15
