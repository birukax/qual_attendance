from django.db import models
from django.urls import reverse
from django.utils.text import slugify

class Shift(models.Model):
    name = models.CharField(max_length=150)
    slug = models.SlugField(unique=True)
    continous = models.BooleanField(default=False)
    saturday_half = models.BooleanField(default=False)
    
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
    slug = models.SlugField(unique=True)
    day_span = models.IntegerField(default=1)
    shift = models.ForeignKey(Shift, on_delete=models.CASCADE, related_name="patterns")
    start_time = models.TimeField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)
    tolerance = models.IntegerField(default=15)   
    next = models.ForeignKey("self", on_delete=models.CASCADE, related_name='pattern' , null=True, blank=True)
    
    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    def get_absolute_url(self):
        return reverse("shift:pattern_detail", args={self.id})
    
