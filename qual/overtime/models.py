from django.db import models
from django.urls import reverse
from django.utils.text import slugify
import employee.models as employee
from django.contrib.auth.models import User


class OvertimeType(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    rate = models.FloatField()
    description = models.TextField()
    day_span = models.IntegerField(default=1)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("overtime:overtime_type_detail", args={self.id})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Overtime(models.Model):
    employee = models.ForeignKey(
        employee.Employee, on_delete=models.CASCADE, related_name="overtimes"
    )
    overtime_type = models.ForeignKey(
        OvertimeType, on_delete=models.CASCADE, related_name="overtimes"
    )
    reason = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    start_time_expected = models.TimeField()
    end_time_expected = models.TimeField()
    start_time_actual = models.TimeField(null=True, blank=True)
    end_time_actual = models.TimeField(null=True, blank=True)
    worked_hours = models.DurationField(null=True, blank=True)
    approved = models.BooleanField(default=False)
    rejected = models.BooleanField(default=False)
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
