from django.db import models
from django.urls import reverse
from django.utils.text import slugify
import datetime


class Shift(models.Model):
    name = models.CharField(max_length=150)
    device = models.ForeignKey(
        "device.Device",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="shifts",
    )
    slug = models.SlugField(unique=True)
    continous = models.BooleanField(default=False)
    saturday_half = models.BooleanField(default=False)

    current_pattern = models.ForeignKey(
        "shift.Pattern",
        on_delete=models.CASCADE,
        null=True,
        related_name="current_shift",
        blank=True,
    )
    last_updated = models.DateField(default=datetime.datetime(2024, 1, 1))

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("shift:shift_detail", args={self.id})


class Pattern(models.Model):
    name = models.CharField(max_length=150)
    day_span = models.IntegerField(default=1)
    shift = models.ForeignKey(Shift, on_delete=models.CASCADE, related_name="patterns")
    start_time = models.TimeField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)
    tolerance = models.IntegerField(default=15)
    next = models.ForeignKey(
        "self", on_delete=models.CASCADE, related_name="pattern", null=True, blank=True
    )

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("shift:pattern_detail", args={self.id})
