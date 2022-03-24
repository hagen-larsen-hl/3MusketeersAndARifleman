from django.contrib import admin
from .models import UserData, CustomerData, BlackList

# Register your models here.
admin.site.register(UserData)
admin.site.register(CustomerData)
admin.site.register(BlackList)