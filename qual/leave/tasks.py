from datetime import datetime, timedelta, date
from dateutil.relativedelta import relativedelta
from PyAstronomy import pyasl
from employee.models import Employee
from .models import Leave

# from pandas import timedelta_range


def calculate_annual_leaves():
    employees = Employee.objects.filter(status="Active").order_by("employment_date")
    for e in employees:
        employment_date = datetime.combine(e.employment_date, datetime.min.time())
        leaves = Leave.objects.filter(
            employee=e, approved=True, leave_type__annual=True
        )
        e.annual_leave_taken = 0
        for l in leaves:
            leave_days = l.end_date.day - l.start_date.day + 1
            if l.half_day:
                leave_days = leave_days - 0.5
            print(f"{e.name}  {leave_days}")
            e.annual_leave_taken = e.annual_leave_taken + leave_days
            e.save()
        # print(leaves)
        if employment_date < datetime(2016, 1, 1):
            pass
        else:
            total = 0
            if e.status == "Terminated":
                end_date = e.termination_date
            else:
                end_date = datetime.today()
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

            print(float(t * y))
            e.annual_leave_balance = round(float(t * y), 2)
            e.annual_leave_remaining = round(
                float(
                    e.annual_leave_balance
                    - e.annual_leave_difference
                    - e.annual_leave_taken
                ),
                2,
            )
            e.save()
