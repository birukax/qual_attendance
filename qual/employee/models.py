import pyodbc
from datetime import date, datetime, timedelta, time
from django.db import models
from django.urls import reverse
import shift.models as shift


class Department(models.Model):
    code = models.CharField(max_length=50)
    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("department:department_detail", args={self.id})

    try:

        def sync_department(self):
            connection = "DRIVER={ODBC Driver 18 for SQL Server};SERVER=172.16.18.23;DATABASE=QualabelsProd_2022_23;TrustServerCertificate=yes;UID=QA;PWD=@F3rdinand1upe"
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

    except Exception as e:
        print(e)


class Employee(models.Model):

    STATUS_CHOICES = [
        ("Active", "Active"),
        ("Inactive", "Inactive"),
        ("Terminated", "Terminated"),
    ]

    employee_id = models.CharField(unique=True, max_length=50)
    name = models.CharField(max_length=150)
    department = models.ForeignKey(
        Department, on_delete=models.CASCADE, related_name="employees", null=True
    )
    pattern = models.ForeignKey(
        shift.Pattern,
        on_delete=models.CASCADE,
        related_name="employees",
        null=True,
        blank=True,
    )
    shift = models.ForeignKey(
        shift.Shift,
        on_delete=models.CASCADE,
        related_name="employees",
        null=True,
    )
    employment_date = models.DateField(null=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default="active")
    last_updated = models.DateField(default=datetime(2024, 1, 1))

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("employee:employee_detail", args={self.id})

    def sync_employee(self):
        connection = "DRIVER={ODBC Driver 18 for SQL Server};SERVER=172.16.18.23;DATABASE=QualabelsProd_2022_23;TrustServerCertificate=yes;UID=QA;PWD=@F3rdinand1upe"
        conn = pyodbc.connect(connection)
        if conn:
            print("successful")
        cursor = conn.cursor()
        employee = cursor.execute(
            "select [No_] as no, [First Name] as fname, [Middle Name] as mname, [Last Name] as lname, [Employment Date] as employment_date, [Status] as status, [Global Dimension 1 Code] as department from [dbo].[QuaLabels Manufacturers$Employee] ORDER BY no"
        )
        emp = cursor.fetchall()

        for e in emp:
            fname = e.fname.replace(" ", "")
            mname = e.mname.replace(" ", "")
            lname = e.lname.replace(" ", "")
            name = f"{fname} {mname} {lname}"
            employment_date = e.employment_date
            department = Department.objects.get(code=e.department)
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
                    status=status,
                )
            else:
                Employee.objects.filter(employee_id=e.no).update(
                    employee_id=e.no,
                    name=name,
                    department=department,
                    employment_date=employment_date,
                    status=status,
                )

        conn.close()
