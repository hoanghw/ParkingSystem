from django.db import models

class Qt_Message(models.Model):
    deviceId = models.IntegerField(unique=True)
    line1 = models.CharField(max_length=20)
    line2 = models.CharField(max_length=20)