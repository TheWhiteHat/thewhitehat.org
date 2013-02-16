from whauth.backends import AuthBackend
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.template import RequestContext
from django.contrib.auth import logout
from django.contrib.auth import login as djlogin
from whauth.models import NewUserForm, NewFBUserForm, User
from whauth.models import UserManager
from forum.views import json_error, json_success

def login(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/') # to a logged in page

    if request.method == "GET":
        f = AuthBackend()

        if 'token' in request.GET:
            token = request.GET['token']
            user = f.authenticate(token=token)

            if user:
                djlogin(request,user)
                return HttpResponseRedirect('/') # to a logged in page
            else:
                return render(request,"whauth/login.html",{'error':"Error on fb login. Either you aren't registered or facebook is tripping."}) # to a fb login error page

    elif request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        f = AuthBackend()

        user = f.authenticate(username=username,password=password)
        
        if user:
            djlogin(request,user)
            return HttpResponseRedirect('/') # to a logged in page
        else:
            return render(request,"whauth/login.html",{'error':"Error on login. Either you aren't registered or invalid password."}) # to a fb login error page
            
    return render(request,'whauth/login.html')

def logouts(request):
    logout(request)
    return HttpResponseRedirect('/')

def register(request):
    if request.method == 'POST':
        if request.is_ajax(): #a new fbuser.
            form = NewFBUserForm(request.POST)
            if form.is_valid():
                try:
                    User.objects.create_user(username=form.cleaned_data['username'],fbid=form.cleaned_data['fbtoken'])
                    return json_success("user_registered")
                except:
                    return json_error("register_error")
            else:
                return json_error(form.errors)
        else:# a regular username & password login.
            form = NewUserForm(request.POST)
            if form.is_valid():
                try:
                    UserManager.create_user(username=form.cleaned_data['name'],password=form.cleaned_data['password'])
                    return render(request,"whauth/register_success")
                except:
                    return render(request,"whauth/register_error",{'message':"There was an error registering."})
    else:
        form = NewUserForm()
    return render(request,"whauth/register.html",{'form':form})
