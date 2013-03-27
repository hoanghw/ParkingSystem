#Delete the old database and follow these:
#run manage.py shell 
#import sys
#execfile('generateData.py')

from home.models import UID_Transaction, Pub_Transaction, Location
from parker.models import Parker,LicensePlate
from django.contrib.auth.models import User
import random,string

def lp_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for x in range(size))

for i in range(1,11):
   l=Location.objects.create(garage="Hearst", space=i)
   l.save()

for i in range(1,6):
   l=Location.objects.create(garage="RSF", space=i)
   l.save()

for i in range(1,11):
   u=User.objects.create(username="user"+str(i),email="username@fake.com",password='')
   u.set_password('user')
   u.save()
   p=Parker.objects.create(user=u,userId=i)
   p.save()
   lp = LicensePlate.objects.create(user=u,lp=lp_generator())
   lp.save()

import datetime
interval=datetime.timedelta(hours=1)
for i in range(1,3):
   start_time=datetime.datetime.now()
   p=Pub_Transaction.objects.create(method='CASH',date=datetime.date.today(),start=start_time,end=start_time+interval,loc=Location.objects.get(id=i))
   p.save()

for i in range(3,7):
   start_time=datetime.datetime.now()
   u=UID_Transaction.objects.create(user=User.objects.get(id=i-2),date=datetime.date.today(),start=start_time,end=start_time+interval,loc=Location.objects.get(id=i),rate='REGULAR')
   u.save()
