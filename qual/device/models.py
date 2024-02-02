from django.urls import reverse
from django.utils.text import slugify
from django.db import models

class Device(models.Model):
    name = models.CharField(max_length=150)
    slug = models.SlugField()
    ip = models.GenericIPAddressField(
        unique=True,
    )
    port = models.IntegerField(default=4370)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    def get_absolute_url(self):
        return reverse("device:device_detail", args={self.id})
