from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Complaint(models.Model):
    REASONS = (
        ('no_show', 'Worker did not show up to complete the job.'),
        ('bad_job', 'Worker did not complete the job satisfactorily.'),
        ('suspicious', 'Worker was acting suspicious while on or around my property.'),
        ('other', 'Other'))

    STATES = (
        ('open', 'Open'),
        ('reimbursed', 'Reimbursed'),
        ('closed', 'Closed')
    )
    
    user = models.ForeignKey(User, on_delete=models.RESTRICT, default=1)
    reason = models.CharField(max_length=100, choices=REASONS)
    other_reason = models.CharField(max_length=100, blank=True)
    description = models.TextField()
    image = models.ImageField(upload_to='complaints/static/complaints')
    state = models.CharField(max_length=30, choices=STATES, default='open')
    create_date = models.DateField(default=timezone.now)
