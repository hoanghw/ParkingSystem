from django.contrib.auth.models import User
from qtmessage.models import Message
from django.http import HttpResponse
import simplejson
# Create your views here.

def get_time_trigger(request):
    if 'u' in request.GET and request.GET['u']:
        message = {}
        user = Message.objects.filter(user__username=request.GET['u'])
        if user:
            triggers = user[0].timetrigger.split('\n')
            for t in triggers:
                if t:
                    j = t.split(":")
                    message[j[0].strip()] = j[1].strip()
        return HttpResponse(simplejson.dumps(message), mimetype='application/json')

from django.views.decorators.csrf import csrf_exempt
@csrf_exempt #without form
def set_time_trigger(request):
    if request.method=='POST' and request.POST['data']:
        message = ''
        user = Message.objects.filter(user__username=request.POST['user'])
        if user:
            lines = request.POST['data'].split(',')
            for l in lines:
                message+=l.strip()+'\n'
            u = user[0]
            u.timetrigger = message
            u.save()

        message = request.POST['user'] + ' ' + message
        return HttpResponse(message)

def check_user(request):
    if 'u' in request.GET and request.GET['u'] and 'p' in request.GET and request.GET['p']:
        message = {}
        user = User.objects.filter(username=request.GET['u'])
        if user and user[0].check_password(request.GET['p']):
            message["user"] = "true"
        else:
            message["user"] = "false"
        return HttpResponse(simplejson.dumps(message), mimetype='application/json')