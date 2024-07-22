from datetime import datetime, timedelta, date
from dateutil.relativedelta import relativedelta
from PyAstronomy import pyasl
from employee.models import Employee
from .models import Leave
from dateutil.rrule import rrule, DAILY, WEEKLY
from holiday.models import Holiday


def get_all_sundays(start_date, end_date):
    total_sundays = rrule(
        WEEKLY, dtstart=start_date, until=end_date, byweekday=6
    ).count()
    return total_sundays


def get_all_holidays(start_date, end_date):
    total_holidays = Holiday.objects.filter(
        date__range=(start_date, end_date), approved=True
    ).count()
    return total_holidays


# from pandas import timedelta_range
def calculate_total_leave_days(id):
    try:
        leave = Leave.objects.get(id=id)
        dates = rrule(DAILY, dtstart=leave.start_date, until=leave.end_date)
        total_sundays = get_all_sundays(leave.start_date, leave.end_date)
        total_holidays = get_all_holidays(leave.start_date, leave.end_date)
        if leave.leave_type.annual:
            leave.total_days = dates.count() - total_sundays - total_holidays
        else:
            leave.total_days = dates.count()
        leave.save()
        if leave.half_day:
            leave.total_days = leave.total_days - 0.5
            leave.save()
    except Exception as e:
        print(e)
    return leave.total_days


def calculate_total_days(start_date, end_date, annual=False):
    dates = rrule(DAILY, dtstart=start_date, until=end_date)
    total_sundays = get_all_sundays(start_date, end_date)
    total_holidays = get_all_holidays(start_date, end_date)
    if annual:
        total_days = dates.count() - total_sundays - total_holidays
    else:
        total_days = dates.count()
    return total_days


def calculate_annual_leaves(end_date=date):
    employees = Employee.objects.filter(status="Active").order_by("employment_date")
    for e in employees:
        employment_date = datetime.combine(e.employment_date, datetime.min.time())
        leaves = Leave.objects.filter(
            employee=e,
            approved=True,
            leave_type__annual=True,
        )
        e.annual_leave_taken = 0
        for l in leaves:
            calculate_total_leave_days(l.id)
            # if l.end_date > end_date:
            #     leave_days = end_date.day - l.start_date.day + 1
            # else:
            #     leave_days = l.end_date.day - l.start_date.day + 1
            # print(f"{e.name}  {leave_days}")
            # if l.end_date > end_date:
            #     leave_days = calculate_total_days(
            #         l.start_date,
            #         end_date,
            #         l.leave_type.annual,
            #     )
            # else:
            leave_days = l.total_days
            # if l.half_day:
            #     leave_days = leave_days - 0.5
            e.annual_leave_taken = e.annual_leave_taken + leave_days

            e.save()
        # print(leaves)
        if employment_date < datetime(2016, 1, 1):
            pass
        else:
            total = 0
            # if e.status == "Terminated" and e.termination_date > datetime(2016, 1, 1):
            #     end_date = e.termination_date
            # else:
            end_date = end_date
            total_years = relativedelta(end_date, employment_date)
            years = total_years.years
            decimal_years = pyasl.decimalYear(
                datetime.combine(end_date, datetime.min.time())
            ) - pyasl.decimalYear(employment_date)
            # print(decimal_years)
            years = years + 1
            for year in range(years):
                balance = 16
                add = int((year - 1) / 2)
                if add > 14:
                    add = 14
                total = total + balance + add
            # print(total)
            y = decimal_years
            # print(y)

            t = total / years

            # print(float(t * y))
            e.calculate_date = end_date
            e.annual_leave_taken = e.annual_leave_taken + e.annual_leave_difference
            e.annual_leave_balance = round(float(t * y), 2)
            e.annual_leave_remaining = round(
                float(e.annual_leave_balance - e.annual_leave_taken),
                2,
            )
            e.save()
