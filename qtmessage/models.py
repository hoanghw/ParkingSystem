from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Message(models.Model):
    user=models.OneToOneField(User)
    widget=models.TextField()
    timetrigger=models.TextField()
    group=models.CharField(max_length=20)
    password=models.CharField(max_length=60)
