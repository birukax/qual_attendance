from django.db import models
from django.urls import reverse
import employee.models
from datetime import date

# Create your models here.
class LeaveType(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100)
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
    is_half_day = models.BooleanField(default=False)
    start_date = models.DateField(default=date.today)
    end_date = models.DateField(default=date.today)
    leave_type = models.ForeignKey(LeaveType, on_delete=models.CASCADE)
    reason = models.TextField(null=True, max_length=250)
    evidence = models.FileField(null=True, blank=True, upload_to="leave_evidence/")
    
    def get_absolute_url(self):
        return reverse("leave:leave_detail", args={self.id})