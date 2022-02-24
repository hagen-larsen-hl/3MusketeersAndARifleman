from django.db import models
from django.contrib.auth.models import User

class UserData(models.Model):
    user = models.OneToOneField(User, verbose_name="User", related_name="data", on_delete=models.CASCADE)

# Create your models here.
