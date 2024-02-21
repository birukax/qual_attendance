from django.urls import path, include
from . import views

app_name = "attendance"


urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("compile", views.compile_view, name="compile_view"),
    path("compile_attendance", views.compile_attendance, name="compile_attendance"),
    path('save_compiled_data', views.save_compiled_attendance, name="save_compiled_data"),
    path("attendances", views.attendance_list, name="attendances"),
    path("get_raw_data", views.get_raw_data, name="get_raw_data"),
    path("raw_attendance_list", views.raw_attendance_list, name="raw_attendance"),
    path("download_attendance", views.download_attendance, name="download_attendance"),
]
