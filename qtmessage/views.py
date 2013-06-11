from django.contrib.auth.models import User
from qtmessage.models import Message
from django.http import HttpResponse
import simplejson
from django.views.decorators.csrf import csrf_exempt
# Create your views here.

@csrf_exempt
def set_loc_trigger(request):
    if request.method=='POST':
        json = simplejson.loads(request.body)
        if 'group' in json:
            users = Message.objects.filter(group=json['group'])
            for u in users:
                u.loctrigger = simplejson.dumps(json['data'])
                u.save()
            message = json['group']+' '+simplejson.dumps(json['data'])
        else:
            users = Message.objects.all()
            for u in users:
                u.loctrigger = simplejson.dumps(json['data'])
                u.save()
            message = 'All Groups '+simplejson.dumps(json['data'])
        return HttpResponse(message)

def get_loc_trigger(request):
    if 'u' in request.GET and request.GET['u']:
        message = {}
        user = Message.objects.filter(user__username=request.GET['u'])
        if user and user[0].loctrigger:
            message = simplejson.loads(user[0].loctrigger)
        return HttpResponse(simplejson.dumps(message), mimetype='application/json')

def get_time_trigger(request):
    if 'u' in request.GET and request.GET['u']:
        message = {}
        user = Message.objects.filter(user__username=request.GET['u'])
        if user and user[0].timetrigger:
            message = simplejson.loads(user[0].timetrigger)
        return HttpResponse(simplejson.dumps(message), mimetype='application/json')

@csrf_exempt #without form
def set_time_trigger(request):
    if request.method=='POST':
        json = simplejson.loads(request.body)
        if 'group' in json:
            users = Message.objects.filter(group=json['group'])
            for u in users:
                u.timetrigger = simplejson.dumps(json['data'])
                u.save()
            message = json['group']+' '+simplejson.dumps(json['data'])
        else:
            users = Message.objects.all()
            for u in users:
                u.timetrigger = simplejson.dumps(json['data'])
                u.save()
            message = 'All Groups '+simplejson.dumps(json['data'])
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

import xml.etree.ElementTree as ET
@csrf_exempt
def create_experiment(request):
    message =''
    if request.method == 'POST' and request.FILES['data']:
        tree = ET.parse(request.FILES['data'])
        if tree:
            userset = tree.find('userset')
            for i in userset.findall('group'):
                group = i.attrib['name']
                for j in i.findall('user'):
                    username = j.attrib['name']
                    password = j.findtext('password')
                    u = User.objects.create(username=username,password='',email=username)
                    u.set_password(password)
                    u.save()
                    m = Message.objects.create(user=u,group=group,password=password)
                    m.save()

            for i in userset.findall('user'):
                u = User.objects.create(username=username,password='',email=username)
                u.set_password(password)
                u.save()
                m = Message.objects.create(user=u,group='',password=password)
                m.save()

            for i in tree.findall('survey'):
                surveyname= i.attrib['name']
                xform = i.find('XForm').text

                timetrigger = {}
                timetrigger[xform]=''
                for j in i.findall('trigger'):
                    if j.attrib['type'] == 'timetrigger':
                        minute = j.findtext('minute')
                        hour = j.findtext('hour')
                        day = j.findtext('day')
                        month = j.findtext('month')
                        year = j.findtext('year')
                        if timetrigger[xform]:
                            timetrigger[xform] = timetrigger[xform]+' '+hour+minute
                        else:
                            timetrigger[xform] = hour+minute

                for k in i.findall('group'):
                    group = k.attrib['ref']
                    m = Message.objects.filter(group=group)
                    for t in m:
                        if t.timetrigger:
                            current = simplejson.loads(t.timetrigger)
                            if xform in current:
                                current[xform] = current[xform]+' '+timetrigger[xform]
                            else:
                                current[xform] = timetrigger[xform]
                            t.timetrigger = simplejson.dumps(current)
                            t.save()
                        else:
                            t.timetrigger = simplejson.dumps(timetrigger)
                            t.save()

                for l in i.findall('user'):
                    m = Message.objects.filter(group='')
                    for t in m:
                        if t.timetrigger:
                            current = simplejson.loads(t.timetrigger)
                            if xform in current:
                                current[xform] = current[xform]+' '+timetrigger[xform]
                            else:
                                current[xform] = timetrigger[xform]
                            t.timetrigger = simplejson.dumps(current)
                            t.save()
                        else:
                            t.timetrigger = simplejson.dumps(timetrigger)
                            t.save()

            message ='success'
    return HttpResponse(message)

def to_json(s):
    message ={}
    triggers = s.split(',')
    for t in triggers:
        if t:
            j = t.split(":")
            message[j[0].strip()] = j[1].strip()
    return message
