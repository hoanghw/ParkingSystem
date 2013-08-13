from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from django.template import RequestContext
from parker.forms import RegistrationForm, LoginForm
from parker.models import Parker
from home.models import UID_Transaction,Pub_Transaction,Location

def ParkerRegistration(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/profile/')
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = User.objects.create_user(username=username, email= form.cleaned_data['email'], password=password)
            user.save()
            parker = Parker(user=user, userId=form.cleaned_data['userId'], wwtoken="", cctoken="")
            parker.save()
            user1 = authenticate(username = username, password = password)
            login(request, user1)
            return HttpResponseRedirect('/profile/')
        else:
            return render_to_response('register.html', {'form': form}, context_instance=RequestContext(request))
    else:
        ''' user is not submitting the form, show them a blank registration form '''
        form = RegistrationForm()
        context = {'form': form}
        return render_to_response('register.html', context, context_instance=RequestContext(request))

def LoginRequest(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/profile/')
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            parker = authenticate(username=username, password=password)
            if parker is not None:
                login(request, parker)
                return HttpResponseRedirect('/profile/')
            else:
                return render_to_response('login.html', {'form': form}, context_instance=RequestContext(request))
        else:
            return render_to_response('login.html', {'form': form}, context_instance=RequestContext(request))


    else:
        '''user is not submitting the form, show the login form'''
        form = LoginForm()
        context = {'form': form}
        return render_to_response('login.html', context, context_instance=RequestContext(request))

def LogoutRequest(request):
    logout(request)
    return HttpResponseRedirect('/login/')

def Profile(request):
    if request.user.is_authenticated():
        parker = Parker.objects.get(user=request.user)

        if not parker.cctoken:
            return render_to_response('redirect.html', {'user': parker.user.username})
	
        import datetime
        now = datetime.datetime.now()

	history = UID_Transaction.objects.filter(user=request.user).filter(end__lte=now)
	current=UID_Transaction.objects.filter(user=request.user).filter(end__gte=now)
        
	isCurrentlyParked = current.filter(rate="REGULAR")
        if isCurrentlyParked:
            parking_status = isCurrentlyParked[0]
        else:
            parking_status = "You are not currently parked"

	isPremParking=current.filter(rate="PREMIUM")
	if isPremParking:
	    prem_status=isPremParking[0]
	else:
	    prem_status ="" 

        variables = RequestContext(request, {'parking_history': history, 'parker': parker, 'parking_status': parking_status, 'prem_status':prem_status})
        return render_to_response('profile.html', variables)
    else:
        return HttpResponseRedirect('/login/')

@csrf_exempt
def Receipt(request):
    if request.method == 'POST':
        user = request.POST['merchantDefinedData2']
	try: u = User.objects.get(username=user)
	except User.DoesNotExist: u = None
	if not u: return HttpResponse("User Does Not Exist")

	parker = Parker.objects.get(user=u)
        if request.POST['merchantDefinedData1'] == 'wwtoken':
            parker.wwtoken=request.POST['paySubscriptionCreateReply_subscriptionID']

	elif request.POST['merchantDefinedData1'] == 'cctoken':
	    parker.cctoken=request.POST['paySubscriptionCreateReply_subscriptionID']

	parker.save()
	login(request, parker)
	return HttpResponseRedirect('/profile/')
