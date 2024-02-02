import pyodbc
import threading
import pandas
import datetime
from ast import pattern
from enum import unique
from tabnanny import check
from tracemalloc import start
from asyncio.windows_events import NULL
from email.policy import default
from datetime import date, datetime, timedelta, time
from dateutil import parser
from django.db import models
from django.forms import CharField
from django.db.models import Q
from django.urls import reverse
from django.utils.text import slugify
from django.utils.timesince import timesince
from functools import reduce
from itertools import count
from operator import truediv
from tkinter import CASCADE
from regex import D
from zk import ZK
from device.models import Device
from employee.models import Employee
from shift.models import Shift
from shift.models import Pattern
import device.models
import employee.models
import shift.models


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
        for device in devices:
            # if device == Device.objects.get(slug="production"):
            #     encoding = "gbk"
            # else:
            #     encoding = "UTF-8"
            device_connected = ZK(
                ip=device.ip,
                port=device.port,
                timeout=300,
                # encoding=encoding,
            )
            device_connected.connect()

            print("Connecting to device...")
            device_connected.disable_device()
            print("Device connected..")
            count_attendance = RawAttendance.objects.filter(device=device).count()
            attendances = device_connected.get_attendance()

            # for attendance in attendances[count_attendance:]:
            for attendance in attendances[count_attendance:]:
                # print(attendance.user)
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

            print("Sync successful..")

            device_connected.enable_device()
            device_connected.disconnect()
        


class Attendance(models.Model):
    # attendance_id = models.ForeignKey(RawAttendance, on_delete=models.CASCADE)
    employee = models.ForeignKey(
        employee.models.Employee, on_delete=models.CASCADE, related_name="attendances"
    )
    device = models.ForeignKey(
        device.models.Device, on_delete=models.CASCADE, related_name="attendances"
    )
    current_pattern = models.ForeignKey(Pattern, on_delete=models.CASCADE, null=True)
    check_in_date = models.DateField()
    check_out_date = models.DateField(null=True)
    check_in_time = models.TimeField()
    check_out_time = models.TimeField(null=True)
    
    def get_absolute_url(self):
        return reverse("attendance:attendance_detail", args={self.id})

    def sync_attendance(self, id, end_date=date.today()):
        if id:
            employees = Employee.objects.filter(id=id)
            
        else:
            employees = Employee.objects.all()
            
        for employee in employees:
            if employee.shift and employee.pattern:
                if employee.shift.continous == False:
                    date_range = pandas.date_range(start=employee.last_updated, end=end_date)
                    for date in date_range.date:
                        attendance = RawAttendance.objects.filter(
                            date=date, employee=employee
                        ).order_by("time")
                        if date.isoweekday() == 1 and date != employee.last_updated:
                            print(date.isoweekday())
                            employee.pattern = employee.pattern.next
                            employee.save()
                            print(employee.pattern)
                        if date.isoweekday() == 6 and employee.shift.saturday_half:
                            print(date.isoweekday())
                            employee.pattern = employee.pattern.next
                            employee.save()
                            print(employee.pattern)
                        if attendance:
                            attendance_first = datetime.combine(
                                attendance.first().date, attendance.first().time
                            )
                            attendance_last = datetime.combine(
                                attendance.last().date, attendance.last().time
                            )
                            check_in = RawAttendance.objects.filter(employee=employee, date=date - timedelta(days=1)).order_by('time')
                            
                            check_out = RawAttendance.objects.filter(employee=employee, date=date + timedelta(days=1)).order_by('time')
                            
                            
                            if attendance.count() == 1 or (
                                attendance.count() >= 2
                                and attendance_last - attendance_first < timedelta(hours=1)
                            ):
                                if employee.pattern.day_span == 2 and check_out:
                                    
                                    at, created = Attendance.objects.update_or_create(
                                        employee=employee,
                                        device=attendance.first().device,
                                        current_pattern = employee.pattern,
                                        check_in_date=attendance.first().date,
                                        check_in_time=attendance.first().time,
                                        check_out_date=check_out.first().date,
                                        check_out_time=check_out.first().time,
                                    )

                                else:
                                    at, created = Attendance.objects.update_or_create(
                                        employee=employee,
                                        device=attendance.first().device,
                                        current_pattern = employee.pattern,
                                        check_in_date=attendance.first().date,
                                        check_in_time=attendance.first().time,
                                    )
                            elif attendance.count() >= 2 and attendance_last - attendance_first > timedelta(hours=1):
                                if employee.pattern.day_span == 1:
                                    at, created = Attendance.objects.update_or_create(
                                        employee=employee,
                                        device=attendance.first().device,
                                        current_pattern = employee.pattern,
                                        check_in_date=attendance.first().date,
                                        check_in_time=attendance.first().time,
                                        check_out_date=attendance.last().date,
                                        check_out_time=attendance.last().time,
                                    )
                                elif employee.pattern.day_span == 2 and check_out:
                                    at, created = Attendance.objects.update_or_create(
                                        employee=employee,
                                        device=attendance.first().device,
                                        current_pattern = employee.pattern,
                                        check_in_date=attendance.last().date,
                                        check_in_time=attendance.last().time,
                                        check_out_date=check_out.first().date,
                                        check_out_time=check_out.first().time,
                                    )
                elif employee.shift.continous == True:
                    date_range = pandas.date_range(start=employee.last_updated, end=datetime.today())
                    for date in date_range.date:
                        if employee.pattern.day_span == 0:
                            employee.pattern = employee.pattern.next
                            employee.save()
                        else:
                            attendance = RawAttendance.objects.filter(
                                date=date, employee=employee
                            ).order_by('time')
                            if attendance:
                                attendance_first = datetime.combine(
                                    attendance.first().date, attendance.first().time
                                )
                                attendance_last = datetime.combine(
                                        attendance.last().date, attendance.last().time
                                    )
                                next_day = date + timedelta(days=1)
                                check_out = RawAttendance.objects.filter(employee=employee, date=next_day).order_by('time')
                                
                                if (attendance.count() == 1 or (attendance.count() >= 2 and attendance_last - attendance_first < timedelta(hours=1))):
                                    if check_out:
                                        at, created = Attendance.objects.update_or_create(
                                            employee=employee,
                                            device=attendance.first().device,
                                            current_pattern = employee.pattern,
                                            check_in_date=attendance.first().date,
                                            check_in_time=attendance.first().time,
                                            check_out_date=check_out.first().date,
                                            check_out_time=check_out.first().time,
                                        )
                                    else:
                                        at, created = Attendance.objects.update_or_create(
                                        employee=employee,
                                        device=attendance.first().device,
                                        current_pattern = employee.pattern,
                                        check_in_date=attendance.first().date,
                                        check_in_time=attendance.first().time,
                                    )
                                elif attendance.count() >= 2 and ( attendance_last - attendance_first > timedelta(hours=1)):
                                    if employee.pattern.day_span == 2 and check_out:
                                        at, created = Attendance.objects.update_or_create(
                                            employee=employee,
                                            device=attendance.first().device,
                                            current_pattern = employee.pattern,
                                            check_in_date=attendance.first().date,
                                            check_in_time=attendance.first().time,
                                            check_out_date=check_out.first().date,
                                            check_out_time=check_out.first().time,
                                        )
                                    elif employee.pattern.day_span == 1:
                                        at, created = Attendance.objects.update_or_create(
                                            employee=employee,
                                            device=attendance.first().device,
                                            current_pattern = employee.pattern,
                                            check_in_date=attendance.first().date,
                                            check_in_time=attendance.first().time,
                                            check_out_date=attendance.last().date,
                                            check_out_time=attendance.last().time,
                                        )
                                employee.pattern = employee.pattern.next
                                employee.save()
            else:
                pass
    
                            