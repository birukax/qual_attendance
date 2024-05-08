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


class DeviceUser(models.Model):
    uid = models.IntegerField(null=True)
    name = models.CharField(max_length=150)
    privilege = models.CharField(max_length=150)
    group_id = models.CharField(max_length=150)
    user_id = models.CharField(max_length=150)
    card = models.CharField(max_length=150)
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    employee = models.ForeignKey(
        "employee.Employee", on_delete=models.CASCADE, null=True, blank=True
    )

    def __str__(self):
        return self.name

    # def get_absolute_url(self):
    #     return reverse("device:device_detail", args={self.id})
