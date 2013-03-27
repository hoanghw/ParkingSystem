from qt.models import Qt_Message
import simplejson
from django.http import HttpResponse,HttpResponseForbidden

def get_messages(request):
    if 'id' in request.GET and request.GET['id']:
        d = Qt_Message.objects.filter(deviceId = int(request.GET['id']))
        if d:
            message = {'LINE1': d[0].line1 , 'LINE2': d[0].line2}
        else: message = {'ERROR': 'This device has not been registered'}
        return HttpResponse(simplejson.dumps(message), mimetype='application/json')
    else: return HttpResponseForbidden