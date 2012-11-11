from whauth.backends import AuthBackend
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth import logout
from django.contrib.auth import login as djlogin

def login(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/') # to a logged in page

    if request.method == "GET":
        f = AuthBackend()

        if 'token' in request.GET:
            token = request.GET['token']
            user = f.authenticate(token=token)

            if user:
                return HttpResponseRedirect('/') # to a logged in page
            else:
                return HttpResponseRedirect('/') # to a fb login error page

    elif request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        f = AuthBackend()

        user = f.authenticate(username=username,password=password)
        
        if user:
            djlogin(request,user)
            return HttpResponseRedirect('/') # to a logged in page
        else:
            return HttpResponseRedirect('/') # to a login error page
            
    return render_to_response('auth/login.html', context_instance=RequestContext(request))

def logouts(request):
    logout(request)
    return HttpResponseRedirect('/')
