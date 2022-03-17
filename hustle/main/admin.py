from django.contrib import admin
from .models import UserData, CustomerData

# Register your models here.
admin.site.register(UserData)
admin.site.register(CustomerData)