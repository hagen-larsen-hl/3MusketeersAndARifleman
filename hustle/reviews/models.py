from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator


class Review(models.Model):    
    worker = models.ForeignKey(User, on_delete=models.RESTRICT, default=1)
    rating = models.IntegerField(default=3, validators=[MaxValueValidator(5), MinValueValidator(1)])
    comments = models.TextField()
