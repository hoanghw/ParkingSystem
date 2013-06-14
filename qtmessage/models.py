from django.db import models
from django.contrib.auth.models import User
from parkingsystem.local_settings import STATICFILES_DIRS as STATIC_DIRS

# Create your models here.
class Message(models.Model):
    user=models.OneToOneField(User)
    widget=models.TextField()
    raw_timetrigger=models.TextField()
    timetrigger=models.TextField()
    raw_loctrigger=models.TextField()
    loctrigger=models.TextField()
    group=models.CharField(max_length=20)
    password=models.CharField(max_length=60)

class InitFile(models.Model):
    doc = models.FileField(upload_to=STATIC_DIRS[0]+'file/')
