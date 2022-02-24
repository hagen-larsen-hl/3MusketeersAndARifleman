from django.db import models
from django.contrib.auth.models import User


class JobType(models.Model):
    type = models.CharField(name="type")


class Job(models.Model):
    time_estimate = models.DurationField(name="time_estimate")
    zip_code = models.CharField(name="zip_code", max_length=10)
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    bid = models.DecimalField(max_digits=2, decimal_places=2)
    complete = models.BooleanField
    completion_window_start = models.DateField(name="completion_window_start")
    completion_window_end = models.DateField(name="completion_window_end")
    type = models.ForeignKey(JobType, on_delete=models.CASCADE)


