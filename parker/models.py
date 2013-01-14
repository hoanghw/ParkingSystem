from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

class Parker(models.Model):
    user    = models.OneToOneField(User)
    userId  = models.PositiveIntegerField()

    def __unicode__(self):
        return self.user.username

#def create_parker_user_callback(sender, instance, **kwargs):
#    parker, new = Parker.objects.get_or_create(user=instance)
#post_save.connect(create_parker_user_callback, User)