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


class Employee(models.Model):
    class Meta:
        ordering = ["name"]

    STATUS_CHOICES = [
        ("Active", "Active"),
        ("Inactive", "Inactive"),
        ("Terminated", "Terminated"),
    ]

    employee_id = models.CharField(unique=True, max_length=50, db_index=True)
    name = models.CharField(max_length=150, db_index=True)
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
    old_rule_balance = models.FloatField(default=0, null=True, blank=True)
    annual_leave_balance = models.FloatField(default=0, null=True, blank=True)
    annual_leave_taken = models.FloatField(default=0, null=True, blank=True)
    annual_leave_remaining = models.FloatField(default=0, null=True, blank=True)
    annual_leave_difference = models.FloatField(default=0, null=True, blank=True)

    def __str__(self):
        return f"{self.name}, {self.employee_id}"

    def get_absolute_url(self):
        return reverse("employee:employee_detail", args={self.id})


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
