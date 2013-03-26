#Delete the old database and follow these:
#run manage.py shell 
#import sys
#execfile('generateData.py')

from home.models import UID_Transaction, Pub_Transaction, Location
from django.contrib.auth.models import User

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
