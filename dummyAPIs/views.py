__author__ = 'Hoang'

from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import render_to_response
from django.template import loader,Context,RequestContext
from django.contrib.auth.models import User
from dummyAPIs.models import HistoryTransaction, CurrentTransaction, Participant
from django.views.decorators.csrf import csrf_exempt

import simplejson
ACCESS= 'Access-Control-Allow-Origin'
ALLOW= '*'
def verifyuser(request):
    message = {}
    if request.method == 'GET' and 'username' in request.GET and 'password' in request.GET:
        message['user'] = True
    return HttpResponse(simplejson.dumps(message), mimetype='application/json')

import datetime, time
def checkout(username):
    u = Participant.objects.filter(username=username)
    if u:
        c = CurrentTransaction.objects.filter(pointer__participant=u[0])
        if c:
            h = c[0].pointer
            #currentTime = datetime.datetime.now()
            #h.endTime = currentTime.strftime('%s')
            h.endTime = int(time.time())
            c[0].delete()

def calEndTime(timestamp,duration,granularity):
    currentTime = datetime.datetime.fromtimestamp(timestamp)
    if granularity == PER_DAY:
        currentTime.replace(hour = 23)
        currentTime.replace(minute = 59)
        currentTime.replace(second = 59)
    elif granularity == PER_HOUR:
        currentTime += datetime.timedelta(hours = duration)
    return time.mktime(currentTime.timetuple())

def ucheckin(request):
    message = {}
    if request.method == 'GET' and 'data' in request.GET:
        json = simplejson.loads(request.GET['data'])
        u = Participant.objects.filter(username=json['username'])
        if u:
            c = CurrentTransaction.objects.filter(pointer__participant=u[0])
            if c:
                checkout(json['username'])

            timestamp = int(time.time())
            granularity = json['granularity']
            duration = json['duration']
            rate = json['rate']
            totalCost = json['totalCost']
            endTime = calEndTime(timestamp,duration,granularity)
            h = HistoryTransaction.objects.create(participant=u[0],garage=json['garage'],space="N/A",startTime=timestamp,endTime=endTime,rate=rate,totalCost=totalCost,granularity=granularity)
            h.save()
            n = CurrentTransaction.objects.create(pointer=h)
            n.save()
    res = HttpResponse(simplejson.dumps(message), mimetype='application/json')
    res[ACCESS] = ALLOW
    return res

def ucheckout(request):
    if request.method == 'GET' and 'username' in request.GET:
        checkout(request.GET['username'])
    return HttpResponse('success')

PER_DAY = 1
PER_HOUR = 2
PER_QUARTER = 3
def getrate(request):
    message = {}
    message['magnitude'] = 7
    message['granularity'] = PER_HOUR
    res = HttpResponse(simplejson.dumps(message), mimetype='application/json');
    res[ACCESS]= ALLOW
    return res

def changelp(request):
    return HttpResponse('success')

def changebilling(request):
    return HttpResponse('success')

def usignin(request):
    message={}
    if request.method=='GET' and 'username' in request.GET and 'password' in request.GET:
        if not Participant.objects.filter(username=request.GET['username']):
            u = Participant.objects.create(username=request.GET['username'], uid=7777)
            u.save()
        message['user']= True
    else:
        message['user']= False
    res= HttpResponse(simplejson.dumps(message),mimetype='application/json')
    res[ACCESS]= ALLOW
    return res

def ulogin(request):
    return render_to_response('main/login.html',context_instance=RequestContext(request))

def uprofile(request):
    return render_to_response('main/profile.html',context_instance=RequestContext(request))