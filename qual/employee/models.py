import pyodbc
from datetime import date, datetime, timedelta, time
from django.db import models
from django.urls import reverse
import shift.models

class Employee(models.Model):
    
    STATUS_CHOICES = [
        ("Active", "Active"),
        ("Inactive", "Inactive"),
        ("Terminated", "Terminated"),
    ]
    
    employee_id = models.CharField(unique=True)
    name = models.CharField(max_length=150)
    pattern = models.ForeignKey(shift.models.Pattern, on_delete=models.CASCADE, related_name='employees', null=True, blank=True)
    shift = models.ForeignKey(
        shift.models.Shift, 
        on_delete=models.CASCADE, 
        related_name="employees", 
        null=True
    )
    employment_date = models.DateField(null=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default="active") 
    last_updated = models.DateField(default=datetime(2024,1,1))
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("employee:employee_detail", args={self.id})

    def sync_employee(self):
        connection = (
            "DRIVER={SQL Server};SERVER=172.16.18.23;DATABASE=QualabelsProd_2022_23;"
        )
        conn = pyodbc.connect(connection)
        if conn:
            print("successful")
        cursor = conn.cursor()
        employee = cursor.execute(
            "select [No_] as no, [First Name] as fname, [Middle Name] as mname, [Last Name] as lname, [Employment Date] as employment_date, [Status] as status from [dbo].[QuaLabels Manufacturers$Employee] ORDER BY no"
        )
        emp = cursor.fetchall()

        for e in emp:
            fname = e.fname.replace(" ", "")
            mname = e.mname.replace(" ", "")
            lname = e.lname.replace(" ", "")
            name = f"{fname} {mname} {lname}"
            employment_date = e.employment_date
            status = e.status
            if status == 0:
                status = "Active"
            elif status == 1:
                status = "Inactive"
            elif status == 2:
                status = "Terminated"
            try:
                emp, created = Employee.objects.filter(employee_id=e.no).update_or_create(
                    employee_id=e.no,
                    name=name,
                    employment_date=employment_date,
                    status=status,
                )
            except:
                pass

        conn.close()
