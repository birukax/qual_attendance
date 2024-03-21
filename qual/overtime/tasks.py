# from __future__ import absolute_import
# from celery import shared_task
from attendance.models import RawAttendance
from django.shortcuts import get_object_or_404
from datetime import datetime, timedelta
from .models import Overtime


def calculate_ot(id):
    overtime = get_object_or_404(Overtime, id=id)
    employee = overtime.employee
    # salary = (
    #     Salary.objects.filter(employee=employee).order_by("-effective_date").first()
    # )
    attendance = RawAttendance.objects.filter(
        employee=employee, date=overtime.start_date
    )
    if attendance:
        # if overtime.overtime_type.day_span == 2:
        if attendance.first().time > overtime.start_time_expected:
            start_time_actual = attendance.first().time
        elif attendance.first().time <= overtime.end_time_expected:
            start_time_actual = overtime.start_time_expected

        if attendance.last().time >= overtime.end_time_expected:
            end_time_actual = overtime.end_time_expected
        elif attendance.last().time < overtime.end_time_expected:
            end_time_actual = attendance.last().time

        start = datetime.combine(overtime.start_date, start_time_actual)
        end = datetime.combine(overtime.end_date, end_time_actual)
        # total_seconds = timedelta.total_seconds(end - start)
        # total_hours = round(float(total_seconds / 3600), 2)
        # total_rate = total_hours * overtime.overtime_type.rate
        # hourly_rate = salary.salary / 240
        # overtime.total_amount = round(total_rate * hourly_rate, 2)
        # overtime.total_rate = round(total_rate, 2)
        overtime.worked_hours = end - start
        overtime.start_time_actual = start_time_actual
        overtime.end_time_actual = end_time_actual
        overtime.save()
