from qt.models import Qt_Message
import os,csv, inspect

allMessages = Qt_Message.objects.all()
for i in allMessages:
    i.line1=""
    i.line2=""
    i.line3=""
    i.line4=""
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
                    m=Qt_Message.objects.filter(user__username=row[0])
                    if m:
                        m[0].line1 = row[1]
                        m[0].line2 = row[2]
                        m[0].line3 = row[3]
                        m[0].line4 = row[4]
                        m[0].save()
                    #else:
                        #newDevice = Qt_Message.objects.create(deviceId=row[0],line1=row[1],line2=row[2],line3=row[3],line4=row[4])
                        #newDevice.save()

