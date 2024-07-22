import pyodbc
from datetime import date, datetime, timedelta, time
from django.db import models
from django.urls import reverse
from decouple import config


class Department(models.Model):
    code = models.CharField(max_length=50)
    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("department:department_detail", args={self.id})

    try:

        def sync_department(self):
            server = config("NAV_SERVER")
            database = config("NAV_SERVER_DATABASE")
            uid = config("NAV_SERVER_UID")
            password = config("NAV_SERVER_PASSWORD")
            connection = (
                "DRIVER={ODBC Driver 18 for SQL Server};"
                + f"SERVER={server};DATABASE={database};TrustServerCertificate=yes;UID={uid};PWD={password}"
            )
            # connection = "DRIVER={ODBC Driver 18 for SQL Server};SERVER=172.16.18.23;DATABASE=QualabelsProd_2022_23;TrustServerCertificate=yes;Trusted_Connection=yes"
            conn = pyodbc.connect(connection)

            # conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=yourserver;DATABASE=yourdb;UID=username;PWD=password')

            if conn:
                print("successful")
            cursor = conn.cursor()
            department = cursor.execute(
                "SELECT [Code] as code, [Name] as name from [dbo].[QuaLabels Manufacturers$Dimension Value] WHERE [Dimension Code]='COST CODE' and [Blocked]='0' "
            )
            dep = cursor.fetchall()

            for d in dep:
                code = d.code
                name = d.name
                if not Department.objects.filter(code=code).exists():
                    Department.objects.create(code=code, name=name)
                else:
                    Department.objects.filter(code=code).update(name=name)

    except Exception as e:
        print(e)


class Employee(models.Model):
    class Meta:
        ordering = ["name"]

    STATUS_CHOICES = [
        ("Active", "Active"),
        ("Inactive", "Inactive"),
        ("Terminated", "Terminated"),
    ]

    employee_id = models.CharField(unique=True, max_length=50)
    name = models.CharField(max_length=150)
    department = models.ForeignKey(
        Department,
        on_delete=models.CASCADE,
        related_name="employees",
        null=True,
        blank=True,
    )
    device = models.ForeignKey(
        "device.Device",
        on_delete=models.CASCADE,
        related_name="employees",
        null=True,
        blank=True,
    )
    shift = models.ForeignKey(
        "shift.Shift",
        on_delete=models.CASCADE,
        related_name="employees",
        null=True,
        blank=True,
    )
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default="Active")
    employment_date = models.DateField(null=True)
    termination_date = models.DateField(null=True)
    calculate_date = models.DateField(null=True)
    annual_leave_balance = models.FloatField(default=0, null=True, blank=True)
    annual_leave_taken = models.FloatField(default=0, null=True, blank=True)
    annual_leave_remaining = models.FloatField(default=0, null=True, blank=True)
    annual_leave_difference = models.FloatField(default=0, null=True, blank=True)

    def __str__(self):
        return f"{self.name}, {self.employee_id}"

    def get_absolute_url(self):
        return reverse("employee:employee_detail", args={self.id})

    def sync_employee(self):
        server = config("NAV_SERVER")
        database = config("NAV_SERVER_DATABASE")
        uid = config("NAV_SERVER_UID")
        password = config("NAV_SERVER_PASSWORD")
        connection = (
            "DRIVER={ODBC Driver 18 for SQL Server};"
            + f"SERVER={server};DATABASE={database};TrustServerCertificate=yes;UID={uid};PWD={password}"
        )
        conn = pyodbc.connect(connection)
        if conn:
            print("successful")
        cursor = conn.cursor()
        employee = cursor.execute(
            "select [No_] as no, [First Name] as fname, [Middle Name] as mname, [Last Name] as lname, [Employment Date] as employment_date, [Termination Date] as termination_date, [Status] as status, [Global Dimension 1 Code] as department from [dbo].[QuaLabels Manufacturers$Employee] ORDER BY no"
        )
        emp = cursor.fetchall()

        for e in emp:
            fname = e.fname.replace(" ", "")
            mname = e.mname.replace(" ", "")
            lname = e.lname.replace(" ", "")
            name = f"{fname} {mname} {lname}"
            employment_date = e.employment_date
            termination_date = e.termination_date
            try:
                department = Department.objects.get(code=e.department)
            except Exception as exc:
                print(exc)
                department = None
            status = e.status
            if status == 0:
                status = "Active"
            elif status == 1:
                status = "Inactive"
            elif status == 2:
                status = "Terminated"
            if not Employee.objects.filter(employee_id=e.no).exists():
                Employee.objects.create(
                    employee_id=e.no,
                    name=name,
                    department=department,
                    employment_date=employment_date,
                    termination_date=termination_date,
                    status=status,
                )
            else:
                Employee.objects.filter(employee_id=e.no).update(
                    employee_id=e.no,
                    name=name,
                    department=department,
                    employment_date=employment_date,
                    termination_date=termination_date,
                    status=status,
                )

        conn.close()


# class Salary(models.Model):
#     employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
#     salary = models.FloatField()
#     end_date = models.DateField(null=True, blank=True)
#     effective_date = models.DateField()
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"{self.employee.name} - {self.salary}"
#         # return f"{self.employee.name} - {self.salary} - {self.effective_date}"
#         # return f"{self.employee.name} - {self.salary} - {self.effective_date} - {self.created_at}"
#         # return f"{self.employee.name} - {self.salary} - {self.effective_date} - {self.created_at} - {self.updated_at}"
#         # return f"{self.employee.name} - {self.salary} - {self.effective_date} - {self.created_at} - {self.updated_at} - {self.id}"

#     def update_salary(self):
#         connection = "DRIVER={ODBC Driver 18 for SQL Server};SERVER=172.16.18.23;DATABASE=QualabelsProd_2022_23;TrustServerCertificate=yes;UID=QA;PWD=@F3rdinand1upe"
#         conn = pyodbc.connect(connection)
#         if conn:
#             print("successful")
#         cursor = conn.cursor()
#         salarys = cursor.execute(
#             "SELECT [PersonID] as id, [DefaultValue] as salary, [EndDate] as end_date, [EffectiveDate] as effective_date from [dbo].[QuaLabels Manufacturers$PayrollPersonPayItem] WHERE [PayrollItemCode]='SALARY' ORDER BY [EffectiveDate]"
#         )
#         # "SELECT [Code] as code, [Name] as name from [dbo].[QuaLabels Manufacturers$Dimension Value] WHERE [Dimension Code]='COST CODE' and [Blocked]='0' "

#         sal = cursor.fetchall()

#         for s in sal:
#             employee = Employee.objects.get(employee_id=s.id)
#             Salary.objects.update_or_create(
#                 employee=employee,
#                 salary=s.salary,
#                 end_date=s.end_date,
#                 effective_date=s.effective_date,
#             )

#         conn.close()
