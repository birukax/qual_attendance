from django.contrib import admin
from .models import Shift, Pattern


@admin.register(Shift)
class ShiftAdmin(admin.ModelAdmin):
    list_display = ["name", "slug", "current_pattern", "continous", "saturday_half"]
    prepopulated_fields = {"slug": ("name",)}
    list_per_page = 15


@admin.register(Pattern)
class PatternAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "day_span",
        "shift",
        "next",
        "start_time",
        "end_time",
        "tolerance",
    ]
    list_per_page = 15
