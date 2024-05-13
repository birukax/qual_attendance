from __future__ import absolute_import
from celery import shared_task
from .models import RawAttendance, Attendance, DailyRecord
from device.models import Device
from employee.models import Employee
import datetime
from zk import ZK
from leave.models import Leave
from holiday.models import Holiday
from datetime import date, datetime, timedelta, time
from shift.models import Shift, Pattern


@shared_task
def sync_raw_attendance(request_device=None):
    if request_device is None:
        devices = Device.objects.all()
    else:
        devices = Device.objects.filter(id=request_device)

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
            if not attendance.timestamp < datetime(2024, 1, 1):
                sync(attendance, device)
        print("Sync successful..")

        device_connected.enable_device()
        device_connected.disconnect()


def create_attendance(**kwargs):

    try:
        try:
            if kwargs["status"]:
                status = kwargs["status"]
        except:
            status = "Checked In"

        try:
            emp = kwargs["employee"]

            if kwargs["check_in_time"]:
                inn = datetime.combine(kwargs["check_in_date"], kwargs["check_in_time"])
                expected = datetime.combine(
                    kwargs["check_in_date"], emp.shift.current_pattern.start_time
                )
                early_expected = expected - timedelta(
                    minutes=emp.shift.current_pattern.tolerance
                )
                late_expected = expected + timedelta(
                    minutes=emp.shift.current_pattern.tolerance
                )
                if inn < early_expected:
                    check_in_type = "Early"
                elif inn > late_expected:
                    check_in_type = "Late"
                else:
                    check_in_type = "On Time"
        except:
            check_in_type = "No Data"

        try:
            emp = kwargs["employee"]
            if kwargs["check_out_time"]:
                outt = datetime.combine(
                    kwargs["check_out_date"], kwargs["check_out_time"]
                )
                expected = datetime.combine(
                    kwargs["check_out_date"], emp.shift.current_pattern.end_time
                )
                early_expected = expected - timedelta(
                    minutes=emp.shift.current_pattern.tolerance
                )
                late_expected = expected + timedelta(
                    minutes=emp.shift.current_pattern.tolerance
                )
                if outt < early_expected:
                    check_out_type = "Early"
                elif outt > late_expected:
                    check_out_type = "Late"
                else:
                    check_out_type = "On Time"
        except:
            check_out_type = "No Data"

        try:
            if kwargs["check_in_date"] and kwargs["check_out_date"]:
                c_in = datetime.combine(
                    kwargs["check_in_date"], kwargs["check_in_time"]
                )
                c_out = datetime.combine(
                    kwargs["check_out_date"], kwargs["check_out_time"]
                )
                worked_hours = c_out - c_in
        except:
            worked_hours = None
        a, created = Attendance.objects.filter(
            check_in_date=kwargs["check_in_date"], employee=kwargs["employee"]
        ).get_or_create(
            kwargs,
            worked_hours=worked_hours,
            check_in_type=check_in_type,
            check_out_type=check_out_type,
            status=status,
        )

    except Exception as e:
        print("final error", e)


def compile(date, employees, request_device, pattern, recompiled):
    date = date
    request_device = request_device
    recompiled = recompiled
    employees = employees
    pattern = pattern
    try:
        if employees:
            employees = Employee.objects.filter(
                employee_id__in=employees, device=request_device
            )
        else:
            employees = Employee.objects.filter(
                status="Active", device=request_device
            ).order_by("name")

        for employee in employees:

            if employee.shift:
                # print(employee.name)
                if pattern:
                    current_pattern = Pattern.objects.get(id=pattern)
                else:
                    current_pattern = employee.shift.current_pattern
                leave = Leave.objects.filter(employee=employee, active=True)
                holiday = Holiday.objects.filter(date=date, approved=True)
                # emp_data = Attendance.objects.filter(
                #     employee=employee, approved=False, deleted=False
                # ).first()
                emp_data = Attendance.objects.filter(
                    employee=employee,
                    check_in_date=date,
                    deleted=False,
                ).first()
                if recompiled and emp_data:

                    emp_data.deleted = True
                    emp_data.save()
                elif emp_data:
                    emp_data.delete()
                if employee.shift.continous == False:
                    attendance = RawAttendance.objects.filter(
                        date=date, employee=employee
                    ).order_by("time")
                    if holiday:
                        # print(1)
                        create_attendance(
                            employee=employee,
                            current_pattern=current_pattern,
                            device=request_device,
                            check_in_date=date,
                            recompiled=recompiled,
                            status="Holiday",
                        )
                    elif date.isoweekday() == 7:
                        # print(2)
                        create_attendance(
                            employee=employee,
                            current_pattern=current_pattern,
                            device=request_device,
                            check_in_date=date,
                            recompiled=recompiled,
                            status="Day Off",
                        )

                    elif attendance:
                        attendance_first = datetime.combine(
                            attendance.first().date, attendance.first().time
                        )
                        attendance_last = datetime.combine(
                            attendance.last().date, attendance.last().time
                        )
                        check_out = RawAttendance.objects.filter(
                            date=date + timedelta(days=1),
                            time__lt=time(hour=9, minute=0),
                            employee=employee,
                        ).order_by("time")
                        if attendance.count() == 1 or (
                            attendance.count() >= 2
                            and attendance_last - attendance_first < timedelta(hours=1)
                        ):
                            if current_pattern.day_span == 2 and check_out:
                                attendance = attendance.filter(
                                    time__gt=time(hour=9, minute=0)
                                )
                                if attendance:
                                    # print(3)
                                    create_attendance(
                                        employee=employee,
                                        device=attendance.first().device,
                                        current_pattern=current_pattern,
                                        check_in_date=date,
                                        recompiled=recompiled,
                                        check_in_time=attendance.first().time,
                                        check_out_date=check_out.first().date,
                                        check_out_time=check_out.first().time,
                                    )
                                else:
                                    # print(3.1)
                                    create_attendance(
                                        employee=employee,
                                        device=check_out.first().device,
                                        current_pattern=current_pattern,
                                        check_in_date=date,
                                        recompiled=recompiled,
                                        check_out_date=check_out.first().date,
                                        check_out_time=check_out.first().time,
                                    )

                            else:
                                # print(4)
                                create_attendance(
                                    employee=employee,
                                    device=attendance.first().device,
                                    current_pattern=current_pattern,
                                    check_in_date=date,
                                    recompiled=recompiled,
                                    check_in_time=attendance.first().time,
                                )
                        elif (
                            attendance.count() >= 2
                            and attendance_last - attendance_first > timedelta(hours=1)
                        ):
                            if current_pattern.day_span == 1:
                                # print(5)
                                create_attendance(
                                    employee=employee,
                                    device=attendance.first().device,
                                    current_pattern=current_pattern,
                                    check_in_date=date,
                                    recompiled=recompiled,
                                    check_in_time=attendance.first().time,
                                    check_out_date=attendance.last().date,
                                    check_out_time=attendance.last().time,
                                )
                            elif current_pattern.day_span == 2 and check_out:
                                # print(6)
                                create_attendance(
                                    employee=employee,
                                    device=attendance.first().device,
                                    current_pattern=current_pattern,
                                    check_in_date=date,
                                    recompiled=recompiled,
                                    check_in_time=attendance.last().time,
                                    check_out_date=check_out.first().date,
                                    check_out_time=check_out.first().time,
                                )
                    elif leave:
                        # print(7)
                        create_attendance(
                            employee=employee,
                            current_pattern=current_pattern,
                            device=request_device,
                            check_in_date=date,
                            recompiled=recompiled,
                            status="On Leave",
                            leave_type=leave.first().leave_type,
                        )
                    else:
                        # print(8)
                        create_attendance(
                            employee=employee,
                            current_pattern=current_pattern,
                            device=request_device,
                            check_in_date=date,
                            recompiled=recompiled,
                            status="Absent",
                        )
                elif employee.shift.continous == True:
                    attendance = RawAttendance.objects.filter(
                        date=date, employee=employee
                    ).order_by("time")
                    if holiday:
                        # print(9)
                        create_attendance(
                            employee=employee,
                            current_pattern=current_pattern,
                            device=request_device,
                            check_in_date=date,
                            recompiled=recompiled,
                            status="Holiday",
                        )
                    elif current_pattern.day_span == 0:
                        # print(10)
                        create_attendance(
                            employee=employee,
                            current_pattern=current_pattern,
                            device=request_device,
                            check_in_date=date,
                            recompiled=recompiled,
                            status="Day Off",
                        )
                    elif attendance:
                        attendance_first = datetime.combine(
                            attendance.first().date, attendance.first().time
                        )
                        attendance_last = datetime.combine(
                            attendance.last().date, attendance.last().time
                        )
                        next_day = date + timedelta(days=1)
                        check_out = RawAttendance.objects.filter(
                            employee=employee,
                            date=next_day,
                            time__lt=time(hour=10, minute=0),
                        ).order_by("time")
                        if attendance.count() == 1 or (
                            attendance.count() >= 2
                            and attendance_last - attendance_first < timedelta(hours=1)
                        ):

                            if check_out:
                                attendance = attendance.filter(
                                    time__lt=time(hour=10, minute=0)
                                )
                                # print(11)
                                if attendance:
                                    create_attendance(
                                        employee=employee,
                                        device=attendance.first().device,
                                        current_pattern=current_pattern,
                                        check_in_date=date,
                                        recompiled=recompiled,
                                        check_in_time=attendance.first().time,
                                        check_out_date=check_out.first().date,
                                        check_out_time=check_out.first().time,
                                    )
                                else:
                                    # print(11.1)
                                    create_attendance(
                                        employee=employee,
                                        device=check_out.first().device,
                                        current_pattern=current_pattern,
                                        check_in_date=date,
                                        recompiled=recompiled,
                                        check_out_date=check_out.first().date,
                                        check_out_time=check_out.first().time,
                                    )
                            else:
                                # print(12)
                                create_attendance(
                                    employee=employee,
                                    device=attendance.first().device,
                                    current_pattern=current_pattern,
                                    check_in_date=date,
                                    recompiled=recompiled,
                                    check_in_time=attendance.first().time,
                                )
                        elif attendance.count() >= 2 and (
                            attendance_last - attendance_first > timedelta(hours=1)
                        ):
                            if current_pattern.day_span == 2 and check_out:
                                # print(13)
                                create_attendance(
                                    employee=employee,
                                    device=attendance.first().device,
                                    current_pattern=current_pattern,
                                    check_in_date=date,
                                    recompiled=recompiled,
                                    check_in_time=attendance.first().time,
                                    check_out_date=check_out.first().date,
                                    check_out_time=check_out.first().time,
                                )
                            elif current_pattern.day_span == 1:
                                # print(14)
                                create_attendance(
                                    employee=employee,
                                    device=attendance.first().device,
                                    current_pattern=current_pattern,
                                    check_in_date=date,
                                    recompiled=recompiled,
                                    check_in_time=attendance.first().time,
                                    check_out_date=attendance.last().date,
                                    check_out_time=attendance.last().time,
                                )

                    elif leave:
                        # print(15)
                        create_attendance(
                            employee=employee,
                            current_pattern=current_pattern,
                            device=request_device,
                            check_in_date=date,
                            recompiled=recompiled,
                            status="On Leave",
                            leave_type=leave.first().leave_type,
                        )

                    else:
                        # print(16)
                        create_attendance(
                            employee=employee,
                            current_pattern=current_pattern,
                            device=request_device,
                            check_in_date=date,
                            recompiled=recompiled,
                            status="Absent",
                        )
            else:
                pass
    except Exception as e:
        print(e)


def save_data(request, date):
    request_device = request.user.profile.device
    attendances = Attendance.objects.filter(
        approved=False,
        deleted=False,
        recompiled=False,
        check_in_date=date,
        device=request_device,
    )
    shifts = Shift.objects.filter(device=request_device)
    try:
        for attendance in attendances:
            attendance.approved = True
            attendance.approved_by = request.user
            attendance.save()
            emp = Employee.objects.get(id=attendance.employee.id)
            emp.last_updated = attendance.check_in_date
            emp.save()

            emp_leave = Leave.objects.filter(employee=emp, active=True)
            if emp_leave:
                if emp_leave.first().end_date >= attendance.check_in_date:
                    e_leave = emp_leave.first()
                    e_leave.active = False
                    e_leave.save()
        for shift in shifts:
            if shift.continous:
                shift.current_pattern = shift.current_pattern.next
                shift.save()
            elif shift.current_pattern.day_span == 0 and shift.continous == False:
                shift.current_pattern = shift.current_pattern.next
                shift.save()
            elif (
                date.isoweekday() == 5
                and shift.saturday_half
                and shift.continous == False
            ):
                shift.current_pattern = shift.current_pattern.next
                shift.save()
            elif date.isoweekday() == 7 and shift.continous == False:
                shift.current_pattern = shift.current_pattern.next
                shift.save()
        if attendances.count() > 0:
            rec, created = DailyRecord.objects.filter(date=date).update_or_create(
                date=date,
                device=request_device,
                attendances=attendances.count(),
                late_check_in=attendances.filter(check_in_type="Late").count(),
                late_check_out=attendances.filter(check_out_type="Late").count(),
                early_check_in=attendances.filter(check_in_type="Early").count(),
                early_check_out=attendances.filter(check_out_type="Early").count(),
                absent=attendances.filter(status="Absent").count(),
                day_off=attendances.filter(status="Day Off").count(),
                leave=attendances.filter(status="On Leave").count(),
                holiday=attendances.filter(status="Holiday").count(),
            )
    except Exception as e:
        print(e)


def save_recompiled(request):
    request_device = request.user.profile.device
    attendances = Attendance.objects.filter(
        approved=False, recompiled=True, deleted=False, device=request_device
    )
    date = attendances.first().check_in_date
    for attendance in attendances:
        attendance.approved = True
        attendance.approved_by = request.user
        attendance.save()
        emp = Employee.objects.get(
            id=attendance.employee.id,
        )
        emp.last_updated = attendance.check_in_date

    daily_record = DailyRecord.objects.get(date=date, device=request_device)
    attendance_record = Attendance.objects.filter(
        check_in_date=date,
        deleted=False,
        recompiled=True,
        approved=True,
        device=request_device,
    )
    daily_record.attendances = attendance_record.count()
    daily_record.late_check_in = attendance_record.filter(
        check_in_type="Late",
    ).count()
    daily_record.late_check_out = attendance_record.filter(
        check_out_type="Late",
    ).count()
    daily_record.early_check_in = attendance_record.filter(
        check_in_type="Early"
    ).count()
    daily_record.early_check_out = attendance_record.filter(
        check_out_type="Early"
    ).count()
    daily_record.absent = attendance_record.filter(status="Absent").count()
    daily_record.day_off = attendance_record.filter(status="Day Off").count()
    daily_record.leave = attendance_record.filter(status="On Leave").count()
    daily_record.holiday = attendance_record.filter(status="Holiday").count()
    daily_record.save()
