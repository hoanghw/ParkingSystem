# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.template import loader,Context
from django.contrib.auth.models import User

def extend_parking(request):
    if request.user.is_authenticated():
        template=loader.get_template('home/extend.html')
        transactions=[]
        context=Context({'user':request.user,'transactions':transactions})
        return HttpResponse(template.render(context))
    else:
        return HttpResponseForbidden()

def check_in(request):
    if request.user.is_authenticated():
        template=loader.get_template('home/checkin.html')

        return HttpResponseRedirect('home/checkin.html')
    else:
        return HttpResponseForbidden()

def check_out(request):
    if request.user.is_authenticated():
        return  HttpResponseRedirect('home/checkout.html')
    else:
        return  HttpResponseForbidden()

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
