from django.db import models
from django.contrib.auth.models import User

class UserData(models.Model):
    user = models.OneToOneField(User, verbose_name="User",primary_key=True ,related_name="data", on_delete=models.CASCADE)
    money = models.DecimalField(max_digits=10,decimal_places=2,default=0.0)
# Create your models here.
