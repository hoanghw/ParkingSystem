__author__ = 'Hoang'

from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import render_to_response
from django.template import loader, Context, RequestContext
from django.contrib.auth.models import User
from dummyAPIs.models import HistoryTransaction, CurrentTransaction, Participant, FavoriteGarage, LicensePlate
from django.views.decorators.csrf import csrf_exempt
import datetime, time

import simplejson

ACCESS = 'Access-Control-Allow-Origin'
ALLOW = '*'
PER_DAY = 1
PER_HOUR = 2
PER_QUARTER = 3


def verifyuser(request):
    message = {}
    if request.method == 'GET' and 'username' in request.GET and 'password' in request.GET:
        message['user'] = True
    return HttpResponse(simplejson.dumps(message), mimetype='application/json')

def checkout(username):
    u = Participant.objects.filter(username=username)
    if u:
        c = CurrentTransaction.objects.filter(pointer__participant=u[0])
        if c:
            h = c[0].pointer
            #currentTime = datetime.datetime.now()
            #h.endTime = currentTime.strftime('%s')
            h.endTime = int(time.time())
            h.save()
            c[0].delete()


def calEndTime(timestamp, duration, granularity):
    currentTime = datetime.datetime.fromtimestamp(timestamp)
    if granularity == PER_DAY:
        currentTime.replace(hour=23)
        currentTime.replace(minute=59)
        currentTime.replace(second=59)
    elif granularity == PER_HOUR:
        currentTime += datetime.timedelta(hours=duration)
    return time.mktime(currentTime.timetuple())

def ucheckin(request):
    message = {}
    if request.method == 'GET' and 'data' in request.GET:
        json = simplejson.loads(request.GET['data'])
        u = Participant.objects.filter(username=json['username'])
        if u:
            timestamp = int(time.time())
            garage = json['garage']
            granularity = json['granularity']
            duration = json['duration']
            rate = json['rate']
            totalCost = json['totalCost']

            space = json['space']
            if (space == 0):
                space = "N/A"

            c = CurrentTransaction.objects.filter(pointer__participant=u[0])
            if c:
                extend = c.filter(pointer__garage=garage)
                if extend and extend[0].pointer.granularity == str(PER_HOUR):
                    timestamp = extend[0].pointer.endTime

                checkout(json['username'])

            endTime = calEndTime(timestamp, duration, granularity)

            h = HistoryTransaction.objects.create(participant=u[0], garage=garage, space=str(space),
                                                  startTime=int(time.time()), endTime=endTime, rate=rate,
                                                  totalCost=totalCost, granularity=granularity)
            h.save()
            nTrans = CurrentTransaction.objects.create(pointer=h)
            nTrans.save()
    res = HttpResponse(simplejson.dumps(message), mimetype='application/json')
    res[ACCESS] = ALLOW
    return res


def ucheckout(request):
    if request.method == 'GET' and 'username' in request.GET:
        checkout(request.GET['username'])
    return HttpResponse('success')


def getrate(request):
    message = {}
    message['magnitude'] = 7
    message['granularity'] = PER_DAY

    #Quick hack
    if request.method == 'GET' and 'data' in request.GET:
        json = simplejson.loads(request.GET['data'])
        u = Participant.objects.filter(username=json['username'])
        if u:
            message['token'] = u[0].cctoken
            f = FavoriteGarage.objects.filter(participant=u[0], garageName=json['garage'])
            if f:
                message['isFavorite'] = True;
            else:
                message['isFavorite'] = False;

    res = HttpResponse(simplejson.dumps(message), mimetype='application/json');
    res[ACCESS] = ALLOW
    return res


def changelp(request):
    return HttpResponse('success')

def changebilling(request):
    return HttpResponse('success')

def usignin(request):
    message = {}
    # if request.method == 'GET' and 'username' in request.GET and 'password' in request.GET:
    #     if not Participant.objects.filter(username=request.GET['username']):
    #         u = Participant.objects.create(username=request.GET['username'], uid=7777)
    #         u.save()
    #     message['user'] = True
    # else:
    #     message['user'] = False
    if request.method == 'GET' and 'username' in request.GET and 'password' in request.GET:
        u=Participant.objects.filter(username=request.GET['username'])
        if u and u[0].password == request.GET['password']:
            message['user'] = True
        else:
            message['user'] = False
    res = HttpResponse(simplejson.dumps(message), mimetype='application/json')
    res[ACCESS] = ALLOW
    return res

def ulogin(request):
    return render_to_response('main/login.html', context_instance=RequestContext(request))


def uprofile(request):
    return render_to_response('main/profile.html', context_instance=RequestContext(request))

def parkinghistory(request):
    if request.method == 'POST':
        u = Participant.objects.filter(username=request.POST.get('username', ''))
        if u:
            h = HistoryTransaction.objects.filter(participant=u[0])
            return render_to_response('main/history.html', {'history': h}, context_instance=RequestContext(request))
            #return HttpResponseRedirect('/ulogin')
        return HttpResponse("no user: " + request.POST.get('username', ''))
    return HttpResponse("fail")

def ugethistory(request):
    message = {}
    if request.method == 'GET' and 'username' in request.GET:
        u = Participant.objects.filter(username=request.GET['username'])
        if u:
            h = HistoryTransaction.objects.filter(participant=u[0])

@csrf_exempt
def ureceipt(request):
    if request.method =='POST' and request.POST['orderPage_transactionType'] == "subscription_authorization":
        return render_to_response('main/profile.html',context_instance=RequestContext(request))

    if request.method == 'POST' and 'merchantDefinedData2' in request.POST:
        user = request.POST['merchantDefinedData2']
        u = Participant.objects.filter(username=user)
        if u:
            if request.POST['merchantDefinedData1'] == 'wwtoken':
                u[0].wwtoken = request.POST['paySubscriptionCreateReply_subscriptionID']
            elif request.POST['merchantDefinedData1'] == 'cctoken':
                u[0].cctoken = request.POST['paySubscriptionCreateReply_subscriptionID']
            u[0].save()
            return render_to_response('main/login.html', context_instance=RequestContext(request))
    return HttpResponseRedirect('/uregistration/')

def ugetfavandtokenandstatus(request):
    message = {}
    if request.method == 'GET' and 'data' in request.GET:
        json = simplejson.loads(request.GET['data'])
        u = Participant.objects.filter(username=json['username'])
        if u:
            message['token'] = u[0].cctoken
            message['favorite'] = [i.garageName for i in u[0].favoritegarage_set.all()]
            lps = u[0].licenseplate_set.filter(isActive=True);
            if lps:
                message['lp'] = lps[0].text
            message['isParking'] = {}
            c = CurrentTransaction.objects.filter(pointer__participant=u[0])
            if c:
                if c[0].pointer.endTime > time.time():
                    message['isParking']['garage'] = c[0].pointer.garage
                    message['isParking']['endTime'] = c[0].pointer.endTime
                    message['isParking']['rate'] = c[0].pointer.rate
                else:
                    for i in c:
                        i.delete()

    res = HttpResponse(simplejson.dumps(message), mimetype='application/json')
    res[ACCESS] = ALLOW
    return res


def uupdatefav(request):
    message = {}
    if request.method == 'GET' and 'data' in request.GET:
        json = simplejson.loads(request.GET['data'])
        u = Participant.objects.filter(username=json['username'])
    if u:
        if json['isFavorite']:
            f = FavoriteGarage.objects.create(participant=u[0], garageName=json['garage'])
            f.save()
        else:
            f = FavoriteGarage.objects.filter(participant=u[0], garageName=json['garage'])
            if f:
                for i in f:
                    i.delete()

    res = HttpResponse(simplejson.dumps(message), mimetype='application/json')
    res[ACCESS] = ALLOW
    return res

def uregistration(request):
    return render_to_response('main/registration.html', context_instance=RequestContext(request))

def uverifyreg(request):
    error = {}
    hasError = False

    if request.method == 'GET':
        un = request.GET.get('username', '')
        pw1 = request.GET.get('password1', '')
        pw2 = request.GET.get('password2', '')

        if not un:
            hasError = True
            error['unEmpty'] = "Please enter a username"
        if not pw1 or not pw2:
            hasError = True
            error['pwEmpty'] = "Please enter valid password"
        if pw1 != pw2:
            hasError = True
            error['pwMatch'] = "Please verify password again"

        u = Participant.objects.filter(username=un)
        if u:
            hasError = True
            error['username'] = "This username is already taken"

        if not request.GET.get('licenseplate', ''):
            hasError = True
            error['lpEmpty'] = "Please enter your license plate"

        if not request.GET.get('permit',''):
            hasError = True
            error['pmEmpty'] = "Please select a permit"

        if hasError:
            return HttpResponse(simplejson.dumps(error), mimetype='application/json')
        else:
            u = Participant.objects.create(username=un, uid=6677)
            u.password = pw1
            u.firstName = request.GET.get('firstname','')
            u.lastName = request.GET.get('lastname','')
            u.email = request.GET.get('email','')
            u.permit = request.GET.get('permit','')
            u.save()
            l = LicensePlate.objects.create(text=request.GET.get('licenseplate',''), participant= u, isActive=True, timestamp = time.time())
            l.save()
            error['noerror'] = True
            return HttpResponse(simplejson.dumps(error), mimetype='application/json')

    return HttpResponse(simplejson.dumps(error), mimetype='application/json')

def uedit(request):
    return render_to_response('main/edit.html', context_instance=RequestContext(request))

def uchangelp(request):
    message = {}
    if request.method == 'GET' and 'data' in request.GET:
        json = simplejson.loads(request.GET['data'])
        u = Participant.objects.filter(username=json['username'])
        if u:
            lps = u[0].licenseplate_set.all()
            for i in lps:
                i.isActive = False;
            lp = LicensePlate.objects.create(participant=u[0],text=json['newlp'],isActive=True,timestamp=time.time())
            lp.save()
            message['error'] = "success"
        else:
            message['error'] = "no user"
    else:
        message['error'] = "wrong request"
    return HttpResponse(simplejson.dumps(message), mimetype='application/json')
