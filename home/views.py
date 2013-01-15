# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import render_to_response
from django.template import loader,Context
from django.contrib.auth.models import User
from home.models import UID_Transaction,Pub_Transaction,Location

def pricing(request):
    if 'psi' in request.GET and 'h' in request.GET:
        import datetime
        start=datetime.datetime.now()
        interval=datetime.timedelta(hours=int(request.GET['h']))
        end= start+interval
        loc=Location.objects.get(id=int(request.GET['psi']))
        template=loader.get_template('home/pricing.html')
        context=Context({'loc':loc,'start':start.ctime(),'end':end.ctime()})
        return HttpResponse(template.render(context))
    if 'detail' in request.GET:
        return render_to_response('home/Price_Detail.htm')

def extend_parking(request):
    if request.user.is_authenticated():
        template=loader.get_template('home/extend.html')
        transactions=[]
        context=Context({'user':request.user,'transactions':transactions})
        return HttpResponse(template.render(context))
    else:
        return HttpResponseForbidden()

#/?user=userName&g=garageName&s=spaceNumber&h=hours
def user_check_in(request):
    import datetime
    now=datetime.datetime.now()

    if 'user' in request.GET and 'g' in request.GET and 's' in request.GET and 'h' in request.GET:
        l=Location.objects.filter(garage=request.GET['g']).get(space=int(request.GET['s']))
        u=User.objects.get(username=request.GET['user'])

        if request.GET['h']:
            interval=datetime.timedelta(hours=int(request.GET['h']))
        else:
            interval=datetime.timedelta(hours=1)

        t=UID_Transaction.objects.create(user=u,
            date=datetime.date.today(),
            loc=l,
            start=now,
            end=now+interval)
        t.save()

        message="Parking info: "+unicode(l)+ " "+unicode(t)
        return HttpResponse(message)
    else: return HttpResponseForbidden()

#/?g=garageName&s=spaceNumber&p=paymentType&h=hours
def guest_check_in(request):
    import datetime
    now=datetime.datetime.now()

    if 'g' in request.GET and 's' in request.GET and 'p' in request.GET and 'h' in request.GET:
        l=Location.objects.filter(garage=request.GET['g']).get(space=int(request.GET['s']))

        if request.GET['h']:
            interval=datetime.timedelta(hours=int(request.GET['h']))
        else:
            interval=datetime.timedelta(hours=1)

        t=Pub_Transaction.objects.create(method=request.GET['p'],
            date=datetime.date.today(),
            loc=l,
            start=now,
            end=now+interval)
        t.save()

        message="Parking info: "+unicode(l)+ " "+unicode(t)

        return HttpResponse(message)
    else: return HttpResponseForbidden()

#/?user=userName
def user_check_out(request):
    import datetime
    now=datetime.datetime.now()

    if 'user' in request.GET and request.GET['user']:
        t=UID_Transaction.objects.filter(user__username=request.GET['user']).get(end__gte=now)
        t.end=now
        t.save()

    if request.user.is_authenticated():
        t=UID_Transaction.objects.filter(user_id=request.user.id).get(end__gte=now)
        t.end=now
        t.save()

    message='You have checked out at '+now.ctime()+'.  The total cost of $6 will be deducted from your account.'
    #template=loader.get_template('home/checkout.html')
    #context=Context({'message':message})
    return  HttpResponseRedirect('/profile/')


#/?g=garageName&s=spaceNumber
def guest_check_out(request):
    import datetime
    now=datetime.datetime.now()

    if 'g' in request.GET and 's' in request.GET:
        l=Location.objects.filter(garage=request.GET['g']).get(space=int(request.GET['s']))
        t=Pub_Transaction.objects.filter(loc=l).get(end__gte=now)
        t.end=now
        t.save()

    message='You have checked out at '+now.ctime()+'.  The total cost is $6.'
    #template=loader.get_template('home/checkout.html')
    #context=Context({'message':message})
    return HttpResponse(message)


def parking_status(request):
    import datetime
    now= datetime.datetime.now()
    from home.models import Location, UID_Transaction, Pub_Transaction

    if request.user.is_authenticated and request.user.is_staff:
        locs=Location.objects.all()
        locs_status=[]
        #Should implement better queryset if have enough time
        for i in locs:
            is_in_UID=UID_Transaction.objects.filter(end__gte=now).filter(loc=i.id)
            is_in_Pub=Pub_Transaction.objects.filter(end__gte=now).filter(loc=i.id)
            if is_in_UID:
                locs_status.append([i,is_in_UID[0]])
            elif is_in_Pub:
                locs_status.append([i,is_in_Pub[0]])
            else:
                locs_status.append([i,''])
        template= loader.get_template('home/parkingstatus.html')
        context=Context({'LocStatus':locs_status})
        return HttpResponse(template.render(context))
    else:
        locs=Location.objects.all()
        locs_status=[]
        #Should implement better queryset if have enough time
        for i in locs:
            is_in_UID=UID_Transaction.objects.filter(end__gte=now).filter(loc=i.id)
            is_in_Pub=Pub_Transaction.objects.filter(end__gte=now).filter(loc=i.id)
            if is_in_UID:
                locs_status.append([i,is_in_UID[0]])
            elif is_in_Pub:
                locs_status.append([i,is_in_Pub[0]])
            else:
                locs_status.append([i,'Available'])
        template= loader.get_template('home/parkingstatus.html')
        context=Context({'LocStatus':locs_status})
        return HttpResponse(template.render(context))
