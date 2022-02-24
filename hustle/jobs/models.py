from django.db import models

# Create your models here.

# This is the module for the jobtype object it isn't done yet
class JobType(models.Model):
    typeName = models.CharField(max_length=200)
