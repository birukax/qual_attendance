from django.contrib import admin
from .models import *


@admin.register(Holiday)
class HolidayAdmin(admin.ModelAdmin):
    list_display = ["name", "date", "approved"]
    prepopulated_fields = {"slug": ("name",)}
    list_filter = ["date"]
    search_fields = ["name"]
