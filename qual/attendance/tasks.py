from __future__ import absolute_import
from celery import shared_task
from .models import RawAttendance, Attendance
from device.models import Device
from employee.models import Employee
import datetime
from zk import ZK


@shared_task
def sync_raw_attendance():
    devices = Device.objects.all()
    # devices = Device.objects.all().order_by("name")

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

        device_connected = ZK(
            ip=device.ip,
            port=device.port,
            timeout=300,
            # encoding=
        )
        device_connected.connect()

        print("Connecting to device...")
        device_connected.disable_device()
        print("Device connected..")
        count_attendance = RawAttendance.objects.filter(device=device).count()
        print("Device disabled")
        attendances = device_connected.get_attendance()
        print("syncing attendance...")
        for attendance in attendances:
            # for attendance in attendances[count_attendance:]:
            if not attendance.timestamp < datetime.datetime(2024, 1, 1):
                sync(attendance, device)
        print("Sync successful..")

        device_connected.enable_device()
        device_connected.disconnect()
