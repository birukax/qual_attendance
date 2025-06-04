from django.db import models
from django.urls import reverse
import employee.models
from datetime import date
from django.contrib.auth.models import User


# Create your models here.
class LeaveType(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=100)
    annual = models.BooleanField(default=False)
    exclude_rest_days = models.BooleanField(default=False)
    description = models.TextField()
    maximum_days = models.PositiveIntegerField(default=0)
    paid = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("leave:leave_type_detail", args={self.id})


class Leave(models.Model):

    employee = models.ForeignKey(
        employee.models.Employee, on_delete=models.CASCADE, related_name="leaves"
    )
    leave_type = models.ForeignKey(
        LeaveType,
        on_delete=models.CASCADE,
        related_name="leaves",
    )
    start_date = models.DateField()
    end_date = models.DateField()
    half_day = models.BooleanField(default=False)
    saturday_half = models.BooleanField(default=False)
    total_days = models.FloatField(default=False)
    active = models.BooleanField(default=False)
    approved = models.BooleanField(default=False)
    rejected = models.BooleanField(default=False)
    approved_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="leave_approval",
    )
    rejected_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="leave_rejection",
    )
    reason = models.TextField(null=True, max_length=250)
    # evidence = models.FileField(null=True, blank=True, upload_to="leave_evidence/")

    def get_absolute_url(self):
        return reverse("leave:leave_detail", args={self.id})

    class Meta:
        ordering = ['-start_date']
