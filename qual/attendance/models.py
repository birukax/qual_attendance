from django.urls import reverse
from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User

# from datetime import date, datetime, timedelta


class RawAttendance(models.Model):
    uid = models.CharField(max_length=50)
    device = models.ForeignKey(
        "device.Device", on_delete=models.CASCADE, related_name="raw_attendances"
    )
    employee = models.ForeignKey(
        "employee.Employee",
        on_delete=models.CASCADE,
        related_name="raw_attendances",
    )
    date = models.DateField(null=True)
    time = models.TimeField(null=True)
    status = models.CharField(null=True, max_length=50)
    punch = models.CharField(max_length=50)

    class Meta:
        get_latest_by = ["-date", "-time"]


class Attendance(models.Model):
    TYPES = [
        ("Late", "Late"),
        ("Early", "Early"),
        ("On Time", "On Time"),
        ("No Data", "No Data"),
    ]
    CHOICES = [
        # ("Checked In", "Checked In"),
        ("Checked", "Checked"),
        ("No Data", "No Data"),
        ("Absent", "Absent"),
        ("Day Off", "Day Off"),
        ("On Leave", "On Leave"),
        ("On Field", "On Field"),
        ("Holiday", "Holiday"),
    ]
    id = models.AutoField(primary_key=True)
    employee = models.ForeignKey(
        "employee.Employee", on_delete=models.CASCADE, related_name="attendances"
    )
    device = models.ForeignKey(
        "device.Device",
        on_delete=models.CASCADE,
        related_name="attendances",
        null=True,
        blank=True,
    )
    current_pattern = models.ForeignKey(
        "shift.Pattern", on_delete=models.CASCADE, null=True
    )
    worked_hours = models.DurationField(null=True, blank=True)
    check_in_date = models.DateField()
    check_out_date = models.DateField(null=True, blank=True)
    check_in_time = models.TimeField(null=True, blank=True)
    check_out_time = models.TimeField(null=True, blank=True)
    check_in_type = models.CharField(max_length=10, choices=TYPES, null=True)
    check_out_type = models.CharField(max_length=10, choices=TYPES, null=True)
    status = models.CharField(max_length=10, choices=CHOICES, null=True)
    compile_date = models.DateField(default=now)
    leave_type = models.ForeignKey(
        "leave.LeaveType",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="leave_type",
    )
    deleted = models.BooleanField(default=False)
    recompiled = models.BooleanField(default=False)
    approved = models.BooleanField(default=False)
    rejected = models.BooleanField(default=False)
    approved_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="attendance_approval",
    )

    def get_absolute_url(self):
        return reverse("attendance:attendance_detail", args={self.id})


class DailyRecord(models.Model):
    date = models.DateField()
    device = models.ForeignKey(
        "device.Device",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    attendances = models.IntegerField()
    late_check_in = models.IntegerField()
    late_check_out = models.IntegerField()
    early_check_in = models.IntegerField()
    early_check_out = models.IntegerField()
    absent = models.IntegerField()
    day_off = models.IntegerField()
    leave = models.IntegerField()
    holiday = models.IntegerField(null=True)
