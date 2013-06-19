from django.contrib.auth.models import User
from qtmessage.models import Message, InitFile
from django.http import HttpResponse
import simplejson
from django.views.decorators.csrf import csrf_exempt
import TriggerParser
import datetime
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

from lxml import etree as ET
@csrf_exempt
def create_experiment(request):
    message =''
    if request.method == 'POST' and request.FILES['data']:
        f = InitFile.objects.create(doc=request.FILES['data'])
        f.save()
        tree = ET.parse(f.doc)
        if tree:
            userset = tree.find('allusers')
            for i in userset.findall('group'):
                group = i.attrib['id']
                for j in i.findall('user'):
                    username = j.attrib['id']
                    if 'password' in j.attrib:
                        password = j.attrib['password']
                    else: password = ''
                    u = User.objects.create(username=username,password='',email=username)
                    u.set_password(password)
                    u.save()
                    m = Message.objects.create(user=u,group=group,password=password)
                    m.save()

            for i in userset.findall('user'):
                username = i.attrib['id']
                if 'password' in i.attrib:
                    password = i.attrib['password']
                else: password = ''
                u = User.objects.create(username=username,password='',email=username)
                u.set_password(password)
                u.save()
                m = Message.objects.create(user=u,group='',password=password)
                m.save()

            for i in tree.findall('survey'):
                #surveyname= i.attrib['description']
                xform = i.find('xform').attrib['id']
                trigger_list=TriggerParser.collectXMLTriggers(i)

                now = datetime.datetime.now()
                today = '%02d' % now.month+ '%02d' % now.day
                timetriggers = {}
                timetriggers[xform]=TriggerParser.getTimeTriggersForOneDay(TriggerParser.getTimeTriggersFromSurvey(trigger_list),today)

                loctriggers = {}
                loctriggers[xform]=TriggerParser.getLocTriggersFromSurveys(trigger_list)

                for k in i.findall('group'):
                    group = k.attrib['ref']
                    m = Message.objects.filter(group=group)
                    for t in m:
                        if t.timetrigger:
                            current = simplejson.loads(t.timetrigger)
                            if xform in current:
                                current[xform] = current[xform]+' '+timetriggers[xform]
                            else:
                                current[xform] = timetriggers[xform]
                            t.timetrigger = simplejson.dumps(current)
                            t.save()
                        else:
                            t.timetrigger = simplejson.dumps(timetriggers)
                            t.save()

                        if t.loctrigger:
                            current = simplejson.loads(t.loctrigger)
                            if xform in current:
                                current[xform].update(loctriggers[xform])
                            else:
                                current[xform] = loctriggers[xform]
                            t.loctrigger = simplejson.dumps(current)
                            t.save()
                        else:
                            t.loctrigger = simplejson.dumps(loctriggers)
                            t.save()

                for l in i.findall('user'):
                    m = Message.objects.filter(user__username=l.attrib['ref'])
                    for t in m:
                        if t.timetrigger:
                            current = simplejson.loads(t.timetrigger)
                            if xform in current:
                                current[xform] = current[xform]+' '+timetriggers[xform]
                            else:
                                current[xform] = timetriggers[xform]
                            t.timetrigger = simplejson.dumps(current)
                            t.save()
                        else:
                            t.timetrigger = simplejson.dumps(timetriggers)
                            t.save()

                        if t.loctrigger:
                            current = simplejson.loads(t.loctrigger)
                            if xform in current:
                                current[xform].update(loctriggers[xform])
                            else:
                                current[xform] = loctriggers[xform]
                            t.loctrigger = simplejson.dumps(current)
                            t.save()
                        else:
                            t.loctrigger = simplejson.dumps(loctriggers)
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

def clear_experiment(request):
    message="Nothing happened"
    if request.method == 'GET':
        if 'admin' in request.GET and 'password' in request.GET:
            if request.GET['admin'] == 'hoang' and request.GET['password'] == 'hoang':
                User.objects.all().delete()
                Message.objects.all().delete()
                InitFile.objects.all().delete()
                message="Success"

    return HttpResponse(message)