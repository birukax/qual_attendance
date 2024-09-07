from django.urls import path, include
from . import views

app_name = "attendance"


urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("compile", views.compile_view, name="compile_view"),
    path("recompile", views.recompile, name="recompile"),
    path(
        "select_for_recompile", views.select_for_recompile, name="select_for_recompile"
    ),
    path("recompile_view", views.recompile_view, name="recompile_view"),
    path("cancel_recompile", views.cancel_recompile, name="cancel_recompile"),
    path("save_recompile", views.save_recompile, name="save_recompile"),
    path("compile_attendance", views.compile_attendance, name="compile_attendance"),
    path(
        "delete_compiled_attendance",
        views.delete_compiled_attendance,
        name="delete_compiled_attendance",
    ),
    path("attendances", views.attendance_list, name="attendances"),
    path("get_raw_data", views.get_raw_data, name="get_raw_data"),
    path("raw_attendance_list", views.raw_attendance_list, name="raw_attendance"),
    path("download_raw_data", views.download_raw_data, name="download_raw_data"),
    path("download_attendance", views.download_attendance, name="download_attendance"),
    path(
        "download_compiled_attendance",
        views.download_compiled_attendance,
        name="download_compiled_attendance",
    ),
    # path("on_fields", views.on_fields, name="on_fields"),
    # path("on_fields/<int:id>", views.on_field_detail, name="on_field_detail"),
    # path("on_fields/create", views.create_on_field, name="create_on_field"),
    # path("on_fields/<int:id>/edit", views.edit_on_field, name="edit_on_field"),
    # path("on_fields/<int:id>/cancel", views.cancel_on_field, name="cancel_on_field"),
    # path("on_fields/download", views.download_on_field, name="download_on_field"),
]
