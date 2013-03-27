from django.db import models
from django.contrib.auth.models import User

class Parker(models.Model):
    user    = models.OneToOneField(User)
    userId  = models.PositiveIntegerField()

    def __unicode__(self):
        return self.user.username


class LicensePlate(models.Model):
    user = models.ForeignKey(User)
    lp = models.CharField(max_length=14)
    def __unicode__(self):
        return self.lp