from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User

from jobs.models import Job


class Survey(models.Model):    
    customer = models.ForeignKey(User, on_delete=models.RESTRICT, default=1)
    job = models.ForeignKey(Job, on_delete=models.RESTRICT, default=1)
    duration_notes = models.TextField("Did the job take more or less time than the customer anticipated?")
    complexity_notes = models.TextField("Was the job more or less difficult than the customer anticipated?")
    notes = models.TextField("What else should other workers know about this customer?")
    create_date = models.DateField(default=timezone.now)
