from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Location(models.Model):
    garage=models.CharField(max_length=30)
    space=models.IntegerField(default=0)
    def __unicode__(self):
        return self.garage+" #"+unicode(self.space)

class Pub_Transaction(models.Model):
    method_choices=(('CASH','Cash'),('CC','CreditCard'),)
    method=models.CharField(max_length=4,choices=method_choices,default='CASH')
    date=models.DateField()
    start=models.DateTimeField()
    end=models.DateTimeField()
    loc=models.ForeignKey(Location)
    def __unicode__(self):
        return self.method+" - Start:"+self.start.ctime()+" - End:"+self.end.ctime()


class UID_Transaction(models.Model):
    user=models.ForeignKey(User)
    date=models.DateField()
    start=models.DateTimeField()
    end=models.DateTimeField()
    loc=models.ForeignKey(Location)
    def __unicode__(self):
        return self.user.username+" - Start:"+self.start.ctime()+" - End:"+self.end.ctime()

class Person():
