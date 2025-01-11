from django.db import models
from django.urls import reverse
from django.utils.text import slugify
import employee.models as employee
from django.contrib.auth.models import User


class Day(models.Model):
    DAYS = (
        ("Monday", "Monday"),
        ("Tuesday", "Tuesday"),
        ("Wednesday", "Wednesday"),
        ("Thursday", "Thursday"),
        ("Friday", "Friday"),
        ("Saturday", "Saturday"),
        ("Sunday", "Sunday"),
    )
    no = models.IntegerField(unique=True)
    name = models.CharField(max_length=100, choices=DAYS)

    def __str__(self):
        return self.name

    # def get_absolute_url(self):
    #     return reverse("overtime:days_detail", args={self.id})


class OvertimeType(models.Model):
    CHOICES = (
        ("OTE", "OTE"),
        ("OTN", "OTN"),
        ("OTH", "OTH"),
        ("OTW", "OTW"),
    )
    days = models.ManyToManyField(Day, related_name="overtime_types", blank=True)
    name = models.CharField(max_length=100)
    pay_item_code = models.CharField(
        max_length=100, choices=CHOICES, null=True, blank=True
    )
    start_time = models.TimeField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)
    day_span = models.IntegerField(default=1)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("overtime:overtime_type_detail", args={self.id})


class Overtime(models.Model):
    employee = models.ForeignKey(
        employee.Employee, on_delete=models.CASCADE, related_name="overtimes"
    )
    reason = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    worked_hours = models.DurationField(null=True, blank=True)
    approved = models.BooleanField(default=False)
    rejected = models.BooleanField(default=False)
    paid = models.BooleanField(default=False)
    approved_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="overtime_approval",
    )
    # total_rate = models.FloatField(null=True, blank=True)
    # total_amount = models.FloatField(null=True, blank=True)

    def get_absolute_url(self):
        return reverse("overtime:overtime_detail", args={self.id})


class Ot(models.Model):

    employee = models.ForeignKey(
        employee.Employee, on_delete=models.CASCADE, related_name="ots"
    )
    overtime_type = models.ForeignKey(
        OvertimeType,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="ots",
    )
    overtime = models.ForeignKey(
        Overtime, null=True, blank=True, on_delete=models.CASCADE, related_name="ots"
    )
    start_date = models.DateField()
    end_date = models.DateField(null=True)
    start_time = models.TimeField()
    end_time = models.TimeField()
    units_worked = models.FloatField()
    have_attendance = models.BooleanField(default=False)
    paid = models.BooleanField(default=False)

    # def __str__(self):
    #     return self.name
