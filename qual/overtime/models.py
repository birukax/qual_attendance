from django.db import models
from django.urls import reverse
from django.utils.text import slugify
import employee.models as employee


class OvertimeType(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    rate = models.DecimalField(max_digits=10, decimal_places=2)
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
    employee = models.ForeignKey(employee.Employee, on_delete=models.CASCADE)
    overtime_type = models.ForeignKey(OvertimeType, on_delete=models.CASCADE)
    reason = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    start_time_expected = models.TimeField()
    end_time_expected = models.TimeField()
    start_time_actual = models.TimeField(null=True, blank=True)
    end_time_actual = models.TimeField(null=True, blank=True)
    worked_hours = models.DurationField(null=True, blank=True)
    approved = models.BooleanField(default=False)
    total_rate = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )

    def get_absolute_url(self):
        return reverse("overtime:overtime_detail", args={self.id})
