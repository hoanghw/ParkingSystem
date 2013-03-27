from qt.models import Qt_Message
import os,csv, inspect

allMessages = Qt_Message.objects.all()
for i in allMessages:
    i.line1="No Update"
    i.line2="No Update"
    i.save()

currentFrame =inspect.getfile(inspect.currentframe())
path = os.path.join(os.path.dirname(os.path.abspath(currentFrame)),'newMessages')
listDir = os.listdir(path)


for i in listDir:
    currentPath = os.path.join(path,i)
    if os.path.isfile(currentPath):
        with open(currentPath,'rb') as f:
            reader=csv.reader(f)
            for row in reader:
                if row:
                    m=Qt_Message.objects.filter(deviceId=row[0])
                    if m:
                        m[0].line1 = row[1]
                        m[0].line2 = row[2]
                        m[0].save()
                    else:
                        newDevice = Qt_Message.objects.create(deviceId=row[0],line1=row[1],line2=row[2])
                        newDevice.save()

