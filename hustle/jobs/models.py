from django.db import models

# Create your models here.

class JobType(models.Model):
    typeName = models.CharField(max_length=200)
