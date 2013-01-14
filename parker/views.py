from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from parker.forms import RegistrationForm, LoginForm
from parker.models import Parker

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
            parker = Parker(user=user, userId=form.cleaned_data['userId'],)
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
    return HttpResponseRedirect('/register/')

def Profile(request):
    if request.user.is_authenticated():
        variables = RequestContext(request, {'user': request.user })
        return render_to_response('profile.html', variables)
    else:
        return HttpResponseRedirect('/login/')
