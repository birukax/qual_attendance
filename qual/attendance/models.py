import threading
import pandas
import datetime
from threading import Thread
from asyncio.windows_events import NULL
from datetime import date, datetime, timedelta
from django.db import models
from django.urls import reverse
from zk import ZK
from device.models import Device
from employee.models import Employee
from shift.models import Pattern
import device.models
import employee.models
import shift.models
import leave.models

class RawAttendance(models.Model):
    uid = models.CharField()
    device = models.ForeignKey(
        device.models.Device, on_delete=models.CASCADE, related_name="raw_attendances"
    )
    employee = models.ForeignKey(
        employee.models.Employee, on_delete=models.CASCADE, related_name="raw_attendances"
    )
    date = models.DateField(null=True)
    time = models.TimeField(null=True)
    status = models.CharField(null=True)
    punch = models.CharField()

    class Meta:
        get_latest_by = ["-date", "-time"]

    def sync_raw_attendance(self):
        devices = Device.objects.all()
        def sync(attendance, device):
            emp_id = str(attendance.user_id).rjust(4, "0")
            try:
                employee = Employee.objects.get(employee_id=emp_id)
            except:
                pass
            try:
                date, time = str(attendance.timestamp).split()
                att, created = RawAttendance.objects.get_or_create(
                    uid=attendance.uid,
                    device=device,
                    employee=employee,
                    date=date,
                    time=time,
                    status=attendance.status,
                    punch=attendance.punch,
                )
            except:
                pass
        
        for device in devices:
            try:
                device_connected = ZK(
                    ip=device.ip,
                    port=device.port,
                    timeout=300,
                )
                device_connected.connect()

                print("Connecting to device...")
                device_connected.disable_device()
                print("Device connected..")
                count_attendance = RawAttendance.objects.filter(device=device).count()
                attendances = device_connected.get_attendance()
                for attendance in attendances[count_attendance:]:
                    if attendance.timestamp < datetime(2024,1,1):
                        pass
                    else:
                        sync(attendance, device)
                print("Sync successful..")

                device_connected.enable_device()
                device_connected.disconnect()
            except:
                pass
        
class Attendance(models.Model):
    TYPES = [
        ('Late', 'Late'),
        ('Early', 'Early'),
        ('On Time', 'On Time'),
        ('No Data', 'No Data')
    ]
    CHOICES = [
    ("Checked In", "Checked In"),
    ("Absent", "Absent"),
    ("Day Off", "Day Off"),
    ("On Leave", "On Leave"),
    ("Holiday", "Holiday")
    ]
    id = models.AutoField(primary_key=True)
    employee = models.ForeignKey(
        employee.models.Employee, on_delete=models.CASCADE, related_name="attendances"
    )
    device = models.ForeignKey(
        device.models.Device, on_delete=models.CASCADE, related_name="attendances", null=True
    )
    current_pattern = models.ForeignKey(Pattern, on_delete=models.CASCADE, null=True)
    worked_hours = models.DurationField(null=True )
    check_in_date = models.DateField()
    check_out_date = models.DateField(null=True)
    check_in_time = models.TimeField(null=True)
    check_out_time = models.TimeField(null=True)
    check_in_type = models.CharField(max_length=10, choices=TYPES, null=True)
    check_out_type = models.CharField(max_length=10, choices=TYPES, null=True)
    status = models.CharField(max_length=10, choices=CHOICES, null=True)
    leave_type = models.CharField(null=True)
    approved = models.BooleanField(default=False)
    
    
    
    def get_absolute_url(self):
        return reverse("attendance:attendance_detail", args={self.id})

class DailyRecord(models.Model):
    date = models.DateField()
    attendances = models.IntegerField()
    late_check_in = models.IntegerField()
    late_check_out = models.IntegerField()
    early_check_in = models.IntegerField()
    early_check_out = models.IntegerField()
    absent = models.IntegerField()
    day_off = models.IntegerField()
    leave = models.IntegerField()
    