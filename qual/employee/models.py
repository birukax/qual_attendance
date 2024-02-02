import pyodbc
import datetime
from datetime import date, datetime, timedelta, time
from django.db import models
from django.urls import reverse
import shift.models

class Employee(models.Model):
    employee_id = models.CharField(unique=True)
    name = models.CharField(
        max_length=150,
    )
    pattern = models.ForeignKey(shift.models.Pattern, on_delete=models.CASCADE, related_name='employees', null=True, blank=True)
    shift = models.ForeignKey(
        shift.models.Shift, on_delete=models.CASCADE, related_name="employees", null=True
    )
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
            "select [No_] as no, [First Name] as fname, [Middle Name] as mname, [Last Name] as lname from [dbo].[QuaLabels Manufacturers$Employee] ORDER BY no"
        )
        emp = cursor.fetchall()

        for e in emp:
            fname = e.fname.replace(" ", "")
            mname = e.mname.replace(" ", "")
            lname = e.lname.replace(" ", "")
            name = f"{fname} {mname} {lname}"
            try:
                Employee.objects.update_or_create(
                    employee_id=e.no,
                    name=name,
                )
            except:
                pass
            # employee.save()

        conn.close()
