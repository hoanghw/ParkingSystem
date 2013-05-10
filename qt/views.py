from qt.models import Qt_Message
import simplejson
from django.http import HttpResponse,HttpResponseForbidden
from parkingsystem.settings import STATICFILES_DIRS as STATIC_DIRS

def get_messages(request):
    if 'id' in request.GET and request.GET['id']:
        d = Qt_Message.objects.filter(deviceId = int(request.GET['id']))
        if d:
            message = {'LINE1': d[0].line1 , 'LINE2': d[0].line2, 'LINE3': d[0].line3, 'LINE4': d[0].line4}
        else: message = {'ERROR': 'This device has not been registered'}
        return HttpResponse(simplejson.dumps(message), mimetype='application/json')
    else: return HttpResponseForbidden

def get_time_trigger(request):
    if 'id' in request.GET and request.GET['id']:
        message = {}
        with open(STATIC_DIRS[0]+'file/timetrigger.txt','r') as f:
            for l in f.readlines():
                t = l.split(" ")
                message[t[0].strip()]=t[1].strip()

        return HttpResponse(simplejson.dumps(message), mimetype='application/json')