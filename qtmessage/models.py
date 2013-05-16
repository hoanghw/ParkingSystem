from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Message(models.Model):
    user=models.ForeignKey(User)
    widget=models.TextField()
    timetrigger=models.TextField()
    password=models.CharField(max_length=60)
