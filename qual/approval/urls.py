from django.urls import path
from . import views

app_name = "approval"
urlpatterns = [
    # path("", views.index, name="index"),
    path("approval/", views.approval, name="approval"),
    path("attendance_approval", views.attendance_approval, name="attendance_approval"),
    path("approve_attendance", views.approve_attendance, name="approve_attendance"),
    path("reject_attendance", views.reject_attendance, name="reject_attendance"),
    path("leave_approval", views.leave_approval, name="leave_approval"),
    path("approve_leave/<int:id>", views.approve_leave, name="approve_leave"),
    path("reject_leave/<int:id>", views.reject_leave, name="reject_leave"),
    path("overtime_approval", views.overtime_approval, name="overtime_approval"),
    path("approve_overtime/<int:id>", views.approve_overtime, name="approve_overtime"),
    path("reject_overtime/<int:id>", views.reject_overtime, name="reject_overtime"),
    path("holiday_approval", views.holiday_approval, name="holiday_approval"),
    path("approve_holiday/<int:id>", views.approve_holiday, name="approve_holiday"),
    path("reject_holiday/<int:id>", views.reject_holiday, name="reject_holiday"),
]
