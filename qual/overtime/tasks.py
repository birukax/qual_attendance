from __future__ import absolute_import
import requests
from celery import shared_task
from attendance.models import RawAttendance
from django.shortcuts import get_object_or_404
from datetime import datetime, timedelta
from .models import Overtime, OvertimeType, Ot
from holiday.models import Holiday
from django.db.models import Q
from requests_ntlm import HttpNtlmAuth
from decouple import config


def calculate_uw(start, end):
    units_worked = end - start
    units_worked = units_worked.seconds / 3600
    units_worked = round(units_worked, 2)
    return units_worked


def create_ots(id):
    overtime = get_object_or_404(Overtime, id=id)
    holiday = Holiday.objects.filter(date=overtime.start_date).first()
    ot_types = OvertimeType.objects.all()
    if holiday:

        ot = Ot(
            start_date=overtime.start_date,
            end_date=overtime.end_date,
            employee=overtime.employee,
            start_time=overtime.start_time,
            end_time=overtime.end_time,
            overtime_type=OvertimeType.objects.filter(pay_item_code="OTH").first(),
            overtime=overtime,
        )
        start = datetime.combine(overtime.start_date, overtime.start_time)

        end = datetime.combine(overtime.end_date, overtime.end_time)
        ot.units_worked = calculate_uw(
            start=start,
            end=end,
        )
        ot.save()
    elif overtime.start_date.isoweekday() == 7:
        ot = Ot(
            start_date=overtime.start_date,
            end_date=overtime.end_date,
            employee=overtime.employee,
            start_time=overtime.start_time,
            end_time=overtime.end_time,
            overtime_type=OvertimeType.objects.filter(pay_item_code="OTW").first(),
            overtime=overtime,
        )
    else:
        for ot_type in ot_types:
            if ot_type.day_span == 2 and overtime.start_date < overtime.end_date:
                ott_start = datetime.combine(overtime.start_date, ot_type.start_time)
                ott_end = datetime.combine(overtime.end_date, ot_type.end_time)
                ot_start = datetime.combine(overtime.start_date, overtime.start_time)
                ot_end = datetime.combine(overtime.end_date, overtime.end_time)
                print("a")
                start_date = overtime.start_date
                end_date = overtime.end_date

            elif ot_type.day_span == 1 and overtime.start_date < overtime.end_date:
                ott_start = datetime.combine(overtime.start_date, ot_type.start_time)
                ott_end = datetime.combine(overtime.start_date, ot_type.end_time)
                ot_start = datetime.combine(overtime.start_date, overtime.start_time)
                ot_end = datetime.combine(overtime.end_date, overtime.end_time)
                print("b")
                start_date = overtime.start_date
                end_date = overtime.start_date
            elif ot_type.day_span == 2 and overtime.start_date == overtime.end_date:
                ott_start = datetime.combine(overtime.start_date, ot_type.start_time)
                ott_end = datetime.combine(
                    overtime.start_date + timedelta(1), ot_type.end_time
                )
                ot_start = datetime.combine(overtime.start_date, overtime.start_time)
                ot_end = datetime.combine(overtime.start_date, overtime.end_time)
                print("c")
                start_date = overtime.start_date
                end_date = overtime.start_date
            else:
                ott_start = datetime.combine(overtime.start_date, ot_type.start_time)
                ott_end = datetime.combine(overtime.start_date, ot_type.end_time)
                ot_start = datetime.combine(overtime.start_date, overtime.start_time)
                ot_end = datetime.combine(overtime.start_date, overtime.end_time)
                print("c")
                start_date = overtime.start_date
                end_date = overtime.start_date

            if overtime.start_date.isoweekday() in ot_type.days.all().values_list(
                "no", flat=True
            ):
                if ot_start <= ott_start < ot_end or ott_start <= ot_start < ott_end:
                    if ott_start <= ot_start and ott_end >= ot_end:
                        print(1)
                        start_time = overtime.start_time
                        end_time = overtime.end_time
                    elif ott_start <= ot_start and ott_end <= ot_end:
                        print(2)
                        start_time = overtime.start_time
                        end_time = ot_type.end_time
                    elif ott_start >= ot_start and ott_end <= ot_end:
                        print(3)
                        start_time = ot_type.start_time
                        end_time = ot_type.end_time
                    elif ott_start >= ot_start and ott_end >= ot_end:
                        print(4)
                        start_time = ot_type.start_time
                        end_time = overtime.end_time

                    if ot_type.day_span == 2:
                        start = datetime.combine(overtime.start_date, start_time)
                        end = datetime.combine(overtime.end_date, end_time)
                    else:
                        start = datetime.combine(overtime.start_date, start_time)
                        end = datetime.combine(overtime.start_date, end_time)

                    units_worked = calculate_uw(
                        start=start,
                        end=end,
                    )
                    Ot.objects.filter(
                        overtime=overtime, overtime_type=ot_type
                    ).get_or_create(
                        employee=overtime.employee,
                        start_date=start_date,
                        end_date=end_date,
                        start_time=start_time,
                        end_time=end_time,
                        overtime_type=ot_type,
                        overtime=overtime,
                        units_worked=units_worked,
                    )


# @shared_task
def calculate_ot():

    overtimes = Overtime.objects.filter(paid=False, approved=True)

    for overtime in overtimes:
        cal_start = datetime.combine(overtime.start_date, overtime.start_time)
        cal_end = datetime.combine(overtime.end_date, overtime.end_time)
        overtime.worked_hours = cal_end - cal_start
        overtime.save()
        try:
            employee = overtime.employee
            ots = overtime.ots.all()
            ots.delete()
            create_ots(overtime.id)
            attendance_first = RawAttendance.objects.filter(
                employee=employee, date=overtime.start_date
            ).order_by("time")
            attendance_last = RawAttendance.objects.filter(
                employee=employee, date=overtime.end_date
            ).order_by("time")
            if overtime.start_date == overtime.end_date:
                a_start = datetime.combine(
                    overtime.start_date, attendance_first.first().time
                )
                a_end = datetime.combine(
                    overtime.end_date, attendance_first.last().time
                )
            else:
                a_start = datetime.combine(
                    overtime.start_date, attendance_first.first().time
                )
                a_end = datetime.combine(
                    overtime.end_date, attendance_last.first().time
                )
            for ot in ots:
                ot_start = datetime.combine(ot.start_date, ot.start_time)
                ot_end = datetime.combine(ot.end_date, ot.end_time)
                if attendance_first and attendance_last:
                    if a_start <= ot_start and a_end >= ot_end:
                        start_time = ot_start.time()
                        end_time = ot_end.time()
                    elif a_start <= ot_start and a_end <= ot_end:
                        start_time = ot_start.time()
                        end_time = a_end.time()
                    elif a_start >= ot_start and a_end <= ot_end:
                        start_time = a_start.time()
                        end_time = a_end.time()
                    elif a_start >= ot_start and a_end >= ot_end:
                        start_time = a_start.time()
                        end_time = ot_end.time

                    start = datetime.combine(ot.start_date, start_time)
                    end = datetime.combine(ot.end_date, end_time)
                    units = calculate_uw(
                        start=start,
                        end=end,
                    )
                    ot.units_worked = units
                    ot.start_time = start_time
                    ot.end_time = end_time
                    ot.have_attendance = True
                    ot.save()
                else:
                    print("no attendance")

        except:
            pass


# @shared_task
def post_ot():
    url = config("NAV")
    user = config("NAV_INSTANCE_USER")
    password = config("NAV_INSTANCE_PASSWORD")
    auth = HttpNtlmAuth(user, password)
    ots = Ot.objects.filter(paid=False, have_attendance=True)
    for ot in ots:
        date = f"{ot.start_date}"
        headers = {
            "Content-Type": "application/json; odata.metadata=minimal",
            "Server": "Microsoft-HTTPAPI/2.0",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Credentials": "true",
            "Access-Control-Expose-Headers": "Date",
            "Access-Control-Expose-Headers": "Content-Length",
            "Access-Control-Expose-Headers": "Server",
            "Access-Control-Expose-Headers": "OData-Version",
            "OData-Version": "4.0",
        }
        data = {
            "PersonID": ot.employee.employee_id,
            "Date": date,
            "PayrollItemCode": ot.overtime_type.pay_item_code,
            "UnitsWorked": ot.units_worked,
        }
        try:
            response = requests.post(
                url,
                json=data,
                headers=headers,
                auth=auth,
            )
            if response.ok:
                ot.paid = True
                ot.save()
            else:
                response.raise_for_status()
            not_completely_paid = Ot.objects.filter(paid=False, id=ot.id)
            if not not_completely_paid:
                overtime = ot.overtime
                overtime.paid = True
                overtime.save()
        except requests.exceptions.HTTPError as err:
            print(f"Error {err}")
