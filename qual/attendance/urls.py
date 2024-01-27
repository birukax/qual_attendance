from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views

app_name = "attendance"


urlpatterns = [
    # path("", include("django.contrib.auth.urls")),
    path("", views.dashboard, name="dashboard"),
    path("employees", views.employees, name="employees"),
    path("sync_employee", views.sync_employee, name="sync_employee"),
    path("employees/<int:id>", views.employee_detail, name="employee_detail"),
    path("sync_attendance", views.sync_attendance, name="sync_attendance"),
    path("attendances", views.attendance_list, name="attendances"),
    path(
        "get_latest_attendance",
        views.get_latest_attendance,
        name="get_latest_attendance",
    ),
    path("raw_attendance", views.raw_attendance, name="raw_attendance"),
    path("download_attendance", views.download_attendance, name="download_attendance"),
    path("devices", views.devices, name="devices"),
    path("create_device", views.create_device, name="create_device"),
    path("shifts", views.shifts, name="shifts"),
    path("shifts/<int:id>", views.shift_detail, name="shift_detail"),
    path("create_shift", views.create_shift, name="create_shift"),
]
