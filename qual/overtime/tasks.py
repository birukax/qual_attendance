from __future__ import absolute_import
from celery import shared_task
from attendance.models import RawAttendance
from django.shortcuts import get_object_or_404
from datetime import datetime, timedelta
from .models import Overtime, OvertimeType, Ot
from holiday.models import Holiday
from django.db.models import Q
from requests_ntlm import HttpNtlmAuth
import pyodbc
import requests


def create_ots(id):

    def calculate_uw(date, starttime, endtime):
        start = datetime.combine(date, starttime)
        end = datetime.combine(date, endtime)
        units_worked = end - start
        units_worked = units_worked.seconds / 3600
        return units_worked

    overtime = get_object_or_404(Overtime, id=id)
    holiday = Holiday.objects.filter(date=overtime.start_date).first()
    ot_types = OvertimeType.objects.filter(
        Q(start_time__gte=overtime.start_time_actual)
        | Q(start_time__lte=overtime.end_time_actual),
        days=overtime.start_date.isoweekday(),
    )
    if holiday:
        ot = Ot(
            employee=overtime.employee,
            start_time=overtime.start_time_actual,
            end_time=overtime.end_time_actual,
            overtime_type=OvertimeType.objects.filter(pay_item_type="OTH").first(),
            overtime=overtime,
        )
        ot.units_worked = calculate_uw(
            date=overtime.start_date,
            endtime=overtime.end_time_actual,
            starttime=overtime.start_time_actual,
        )
        ot.save()
    else:
        for ot_type in ot_types:
            print("creating overtimes")
            print(ot_type.name)
            if (
                ot_type.start_time <= overtime.start_time_actual
                and ot_type.end_time >= overtime.end_time_actual
            ):
                print(1)
                start_time = overtime.start_time_actual
                end_time = overtime.end_time_actual
            elif (
                ot_type.start_time <= overtime.start_time_actual
                and ot_type.end_time <= overtime.end_time_actual
            ):
                print(2)
                start_time = overtime.start_time_actual
                end_time = ot_type.end_time
            elif (
                ot_type.start_time >= overtime.start_time_actual
                and ot_type.end_time <= overtime.end_time_actual
            ):
                print(3)
                start_time = ot_type.start_time
                end_time = ot_type.end_time
            elif (
                ot_type.start_time >= overtime.start_time_actual
                and ot_type.end_time >= overtime.end_time_actual
            ):
                print(4)
                start_time = ot_type.start_time
                end_time = overtime.end_time_actual

            units_worked = calculate_uw(
                date=overtime.start_date,
                starttime=start_time,
                endtime=end_time,
            )
            Ot.objects.create(
                employee=overtime.employee,
                date=overtime.start_date,
                start_time=start_time,
                end_time=end_time,
                overtime_type=ot_type,
                overtime=overtime,
                units_worked=units_worked,
            )


def calculate_ot(id):
    overtime = get_object_or_404(Overtime, id=id)
    employee = overtime.employee
    # salary = (
    #     Salary.objects.filter(employee=employee).order_by("-effective_date").first()
    # )
    attendance = RawAttendance.objects.filter(
        employee=employee, date=overtime.start_date
    ).order_by("time")
    if attendance:
        # if overtime.overtime_type.day_span == 2:
        if attendance.first().time > overtime.start_time_expected:
            start_time_actual = attendance.first().time
        elif attendance.first().time <= overtime.start_time_expected:
            start_time_actual = overtime.start_time_expected

        if (
            attendance.last().time >= overtime.end_time_expected
            or attendance.count() < 2
        ):
            end_time_actual = overtime.end_time_expected
        elif attendance.last().time < overtime.end_time_expected:
            end_time_actual = attendance.last().time

        start = datetime.combine(overtime.start_date, start_time_actual)
        end = datetime.combine(overtime.end_date, end_time_actual)
        overtime.worked_hours = end - start
        overtime.start_time_actual = start_time_actual
        overtime.end_time_actual = end_time_actual
        overtime.save()
    if not overtime.paid:
        Ot.objects.filter(overtime=overtime).delete()
        create_ots(id=id)


@shared_task
def post_ot():
    url = "http://v-qua-navapp-01.qualabels.local:7248/Test/ODataV4/Company('QuaLabels%20Manufacturers')/Overtimes"
    overtimes = Overtime.objects.filter(paid=False)
    auth = HttpNtlmAuth("qualabels\\administrator", "Admin!@2020")

    for overtime in overtimes:
        ots = Ot.objects.filter(overtime=overtime)
        for ot in ots:
            date = f"{ot.date}"

            url = "http://v-qua-navapp-01.qualabels.local:7248/Test/ODataV4/Company('QuaLabels%20Manufacturers')/Overtimes"
            headers = {
                "Content-Type": "application/json; odata.metadata=minimal",
                "Server": "Microsoft-HTTPAPI/2.0",
                "Accept": "application/json",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Credentials": "true",
                "Access-Control-Expose-Headers": "Date, Content-Length, Server, OData-Version",
                "OData-Version": "4.0",
            }
            data = {
                "PersonID": ot.employee.employee_id,
                "Date": date,
                "PayrollItemCode": ot.overtime_type.pay_item_code,
                "UnitsWorked": ot.units_worked,
            }
            response = requests.post(
                url,
                json=data,
                headers=headers,
                auth=auth,
            )
            print(response.status_code)
        overtime.paid = True
        overtime.save()
