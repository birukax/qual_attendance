from .models import *
from datetime import date
from leave.models import *
from holiday.models import *


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
        print(e)


def compile(date):
    employees = Employee.objects.filter(status="Active").order_by("name")
    for employee in employees:
        if employee.shift:
            leave = Leave.objects.filter(employee=employee, active=True)
            holiday = Holiday.objects.filter(date=date, approved=True)
            del_emp_data = Attendance.objects.filter(
                employee=employee, check_in_date=date
            )
            if del_emp_data:
                del_emp_data.delete()
            if employee.shift.continous == False:
                attendance = RawAttendance.objects.filter(
                    date=date, employee=employee
                ).order_by("time")
                if holiday:
                    create_attendance(
                        employee=employee,
                        current_pattern=employee.shift.current_pattern,
                        check_in_date=date,
                        status="Holiday",
                    )
                elif date.isoweekday() == 7:
                    create_attendance(
                        employee=employee,
                        current_pattern=employee.shift.current_pattern,
                        check_in_date=date,
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
                        employee=employee, date=date + timedelta(days=1)
                    ).order_by("time")

                    if attendance.count() == 1 or (
                        attendance.count() >= 2
                        and attendance_last - attendance_first < timedelta(hours=1)
                    ):
                        if employee.shift.current_pattern.day_span == 2 and check_out:

                            create_attendance(
                                employee=employee,
                                device=attendance.first().device,
                                current_pattern=employee.shift.current_pattern,
                                check_in_date=date,
                                check_in_time=attendance.first().time,
                                check_out_date=check_out.first().date,
                                check_out_time=check_out.first().time,
                            )

                        else:
                            create_attendance(
                                employee=employee,
                                device=attendance.first().device,
                                current_pattern=employee.shift.current_pattern,
                                check_in_date=date,
                                check_in_time=attendance.first().time,
                            )
                    elif (
                        attendance.count() >= 2
                        and attendance_last - attendance_first > timedelta(hours=1)
                    ):
                        if employee.shift.current_pattern.day_span == 1:
                            create_attendance(
                                employee=employee,
                                device=attendance.first().device,
                                current_pattern=employee.shift.current_pattern,
                                check_in_date=date,
                                check_in_time=attendance.first().time,
                                check_out_date=attendance.last().date,
                                check_out_time=attendance.last().time,
                            )
                        elif employee.shift.current_pattern.day_span == 2 and check_out:
                            create_attendance(
                                employee=employee,
                                device=attendance.first().device,
                                current_pattern=employee.shift.current_pattern,
                                check_in_date=date,
                                check_in_time=attendance.last().time,
                                check_out_date=check_out.first().date,
                                check_out_time=check_out.first().time,
                            )
                elif leave:
                    create_attendance(
                        employee=employee,
                        current_pattern=employee.shift.current_pattern,
                        check_in_date=date,
                        status="On Leave",
                        leave_type=leave.first().leave_type,
                    )
                else:
                    create_attendance(
                        employee=employee,
                        current_pattern=employee.shift.current_pattern,
                        check_in_date=date,
                        status="Absent",
                    )
            elif employee.shift.continous == True:
                attendance = RawAttendance.objects.filter(
                    date=date, employee=employee
                ).order_by("time")
                if holiday:
                    create_attendance(
                        employee=employee,
                        current_pattern=employee.shift.current_pattern,
                        check_in_date=date,
                        status="Holiday",
                    )
                elif employee.shift.current_pattern.day_span == 0:
                    create_attendance(
                        employee=employee,
                        current_pattern=employee.shift.current_pattern,
                        check_in_date=date,
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
                        employee=employee, date=next_day
                    ).order_by("time")

                    if attendance.count() == 1 or (
                        attendance.count() >= 2
                        and attendance_last - attendance_first < timedelta(hours=1)
                    ):
                        if check_out:
                            create_attendance(
                                employee=employee,
                                device=attendance.first().device,
                                current_pattern=employee.shift.current_pattern,
                                check_in_date=date,
                                check_in_time=attendance.first().time,
                                check_out_date=check_out.first().date,
                                check_out_time=check_out.first().time,
                            )
                        else:
                            create_attendance(
                                employee=employee,
                                device=attendance.first().device,
                                current_pattern=employee.shift.current_pattern,
                                check_in_date=date,
                                check_in_time=attendance.first().time,
                            )
                    elif attendance.count() >= 2 and (
                        attendance_last - attendance_first > timedelta(hours=1)
                    ):
                        if employee.shift.current_pattern.day_span == 2 and check_out:
                            create_attendance(
                                employee=employee,
                                device=attendance.first().device,
                                current_pattern=employee.shift.current_pattern,
                                check_in_date=date,
                                check_in_time=attendance.first().time,
                                check_out_date=check_out.first().date,
                                check_out_time=check_out.first().time,
                            )
                        elif employee.shift.current_pattern.day_span == 1:
                            create_attendance(
                                employee=employee,
                                device=attendance.first().device,
                                current_pattern=employee.shift.current_pattern,
                                check_in_date=date,
                                check_in_time=attendance.first().time,
                                check_out_date=attendance.last().date,
                                check_out_time=attendance.last().time,
                            )
                elif leave:
                    create_attendance(
                        employee=employee,
                        current_pattern=employee.shift.current_pattern,
                        check_in_date=date,
                        status="On Leave",
                        leave_type=leave.first().leave_type,
                    )
                else:
                    create_attendance(
                        employee=employee,
                        current_pattern=employee.shift.current_pattern,
                        check_in_date=date,
                        status="Absent",
                    )
        else:
            pass


def save_data(request, date):
    attendances = Attendance.objects.filter(approved=False)
    shifts = Shift.objects.all()

    for attendance in attendances:
        attendance.approved = True
        attendance.approved_by = request.user
        attendance.save()
        emp = Employee.objects.get(id=attendance.employee.id)
        emp.last_updated = attendance.check_in_date
        emp.save()

        emp_leave = Leave.objects.filter(employee=emp, active=True)
        if emp_leave:
            if emp_leave.first().end_date == attendance.check_in_date:
                emp_leave.update(active=False)
    for shift in shifts:
        if shift.current_pattern.day_span == 0:
            shift.current_pattern = shift.current_pattern.next
            shift.save()
        elif shift.continous:
            shift.current_pattern = shift.current_pattern.next
            shift.save()
        elif date.isoweekday() == 5 and shift.saturday_half:
            shift.current_pattern = shift.current_pattern.next
            shift.save()
        elif date.isoweekday() == 6 and shift.continous == False:
            shift.current_pattern = shift.current_pattern.next
            shift.save()
    rec, created = DailyRecord.objects.update_or_create(
        date=date,
        attendances=attendances.count(),
        late_check_in=attendances.filter(check_in_type="Late").count(),
        late_check_out=attendances.filter(check_out_type="Late").count(),
        early_check_in=attendances.filter(check_in_type="Early").count(),
        early_check_out=attendances.filter(check_out_type="Early").count(),
        absent=attendances.filter(status="Absent").count(),
        day_off=attendances.filter(status="Day Off").count(),
        leave=attendances.filter(status="Leave").count(),
    )
