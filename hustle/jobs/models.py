from django.db import models

from django.contrib.auth.models import User


class JobType(models.Model):
    type = models.CharField(max_length=30, default="Mow Lawn")
    ownerCut = models.DecimalField(max_digits=5, decimal_places=2, default=0.05)
    canceledTime = models.IntegerField(default=24)

    def __str__(self):
        return self.type


class Job(models.Model):
    time_estimate = models.IntegerField(name="time_estimate")
    zip_code = models.CharField(name="zip_code", max_length=10)
    customer = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    accepted_bid = models.ForeignKey("Bid", related_name="accepted_bid", on_delete=models.CASCADE, null=True)
    complete = models.BooleanField(name="complete", default=False)
    completion_window_start = models.DateField(name="completion_window_start")
    completion_window_end = models.DateField(name="completion_window_end")
    type = models.ForeignKey(JobType, on_delete=models.CASCADE)
    claimed_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="claimed_user", null=True)
    cancelled = models.BooleanField(name="cancelled", default=False)

    def request_from_owner(self, request):
        return True
        # return customer == request.user


class Bid(models.Model):
    bid = models.DecimalField(max_digits=100, decimal_places=2)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    selected_job = models.ForeignKey(Job, related_name="selected_job", on_delete=models.CASCADE)
