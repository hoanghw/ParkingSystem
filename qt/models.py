from django.db import models
from django.contrib.auth.models import User

class Qt_Message(models.Model):
    user = models.OneToOneField(User)
    line1 = models.CharField(max_length=40)
    line2 = models.CharField(max_length=40)
    line3 = models.CharField(max_length=40)
    line4 = models.CharField(max_length=40)