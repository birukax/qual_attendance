from django.urls import path, include
from . import views

app_name = "attendance"


urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("attendances", views.attendance_list, name="attendances"),
    path("sync_attendance", views.sync_attendance, name="sync_attendance"),
    path("sync_employee_attendance/<int:id>", views.sync_employee_attendance, name="sync_employee_attendance"),
    path(
        "get_latest_attendance",
        views.get_latest_attendance,
        name="get_latest_attendance",
    ),
    path("raw_attendance_list", views.raw_attendance_list, name="raw_attendance"),
    path("download_attendance", views.download_attendance, name="download_attendance"),
]
