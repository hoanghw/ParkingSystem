from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Location(models.Model):
    garage=models.CharField(max_length=30)
    space=models.IntegerField

class Pub_Transaction(models.Model):
    method=models.CharField(max_length=30)
    date=models.DateField
    start=models.DateTimeField
    end=models.DateTimeField
    loc=models.ForeignKey(Location)

class UID_Transaction(models.Model):
    user=models.ForeignKey(User)
    date=models.DateField
    start=models.DateTimeField
    end=models.DateTimeField
    loc=models.ForeignKey(Location)

class Person():