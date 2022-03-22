from django.db import models
from django.contrib.auth.models import User
from localflavor.us.models import USZipCodeField, USStateField

class UserData(models.Model):
    user = models.OneToOneField(User, verbose_name="User", related_name="data", on_delete=models.CASCADE, primary_key=True)
    phone_number = models.CharField(max_length=16, unique=True, default="0000000000")
    money = models.DecimalField(max_digits=10,decimal_places=2,default=0.0)

class CustomerData(models.Model):
    user = models.OneToOneField(User, verbose_name="User", related_name="customer_data", on_delete=models.CASCADE, primary_key=True)
    # Address
    street = models.CharField(max_length=128)
    street2 = models.CharField(max_length=16)
    city = models.CharField(max_length=32)
    state = USStateField()
    zip_code = USZipCodeField()

class WorkerData(models.Model):
    user = models.OneToOneField(User, verbose_name="User", related_name="worker_data", on_delete=models.CASCADE, primary_key=True)
