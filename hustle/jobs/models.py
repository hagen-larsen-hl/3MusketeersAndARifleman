from django.db import models


class User(models.Model):
    pass


class JobType(models.Model):
    pass


class Job(models.Model):
    time_estimate = models.DurationField
    zip_code = models.CharField
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    bid = models.DecimalField(decimal_places=2)
    complete = models.BooleanField
    completion_window_start = models.DateField
    completion_window_end = models.DateField
    type = models.ForeignKey(JobType, on_delete=models.CASCADE)


