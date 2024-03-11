from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from datetime import date


class Holiday(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    date = models.DateField()
    approved = models.BooleanField(default=False)
    description = models.TextField()

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("holiday:holiday_detail", args={self.id})
