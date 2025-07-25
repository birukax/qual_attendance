from django.db import models
from django.conf import settings
from django.urls import reverse


class Profile(models.Model):

    ROLES = (("USER", "USER"), ("HR", "HR"), ("ADMIN", "ADMIN"), ("MANAGER", "MANAGER"))

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLES, default="USER")
    employee = models.ForeignKey(
        "employee.Employee", on_delete=models.CASCADE, null=True, blank=True
    )
    device = models.ForeignKey(
        "device.Device", on_delete=models.CASCADE, blank=True, null=True
    )
    manages = models.ManyToManyField(
        "employee.Department", related_name="managers", blank=True
    )

    class Meta:
        permissions = [("can_approve", "Can Approve")]

    def get_absolute_url(self):
        return reverse("account:user_detail", args={self.id})

    def __str__(self):
        return f"{self.user.username}"
