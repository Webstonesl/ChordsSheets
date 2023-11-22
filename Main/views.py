from django.shortcuts import render
from django.http import HttpRequest, HttpResponse, FileResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth import forms, login, logout, decorators
from Shows.models import *
from datetime import datetime # TODO DATETIME
from django.urls import path

# from django.contrib.
# Create your views here.

def home(req:HttpRequest):
    events = Event.objects.all().filter(eventrole__user=req.user,start__gte=datetime.today()).order_by('start')
    
    g = {'Today':[],'This Week':[], 'This Month': [], 'This Year':[], 'Even Later':[] }
    for event in events:
        if (event.start.date() == datetime.today().date()):
            g['Today'].append(event)
        elif (event.start.year == datetime.today().year):
            if (event.start.month == datetime.today().month):
                g['This Month'].append(event)
            else:
                g['This Year'].append(event)
        else:
            g['Even Later'].append(event)

    groups = [{'title':k,'events':g[k]} for k in g if len(g[k])>0]
    return render(req,'home.html', {'title': 'Home', 'events' : groups})



def login_page(req:HttpRequest):
    if (req.user.is_authenticated):
        return HttpResponseRedirect('/')
    if (req.method == "GET"):
        return render(req,'login.html',{'form':forms.AuthenticationForm(),'title': 'Login'})
    else:
        form = forms.AuthenticationForm(req,data=req.POST)

        if form.is_valid():
            login(req, form.get_user())
            return HttpResponseRedirect('/')
        else:
            
            return render(req,'login.html',{'form':form, 'title':'Login'})

def create_account_page(req:HttpRequest):
    if (req.user.is_authenticated):
        return HttpResponseRedirect('/')
    if (req.method == "GET"):
        return render(req,'create_account.html',{'form':forms.UserCreationForm(),'title': 'Login'})
    else:
        form = forms.UserCreationForm(req.POST)

        if form.is_valid():
            form.save()


            return HttpResponseRedirect('/login')
        else:
            
            return render(req,'create_account.html',{'form':form, 'title':'Login'})


def logout_page(req:HttpRequest):
    logout(req)
    return HttpResponseRedirect('/')
    
@decorators.login_required
def checkforuser(req:HttpRequest): 
    if len(User.objects.filter(username=req.GET.get('username')))==1:
        return JsonResponse({'type':'user'})
    elif len(Group.objects.filter(name=req.GET.get('group')))==1:
        return JsonResponse({'type':'group'})
    else:
        return JsonResponse({'type':'none'})
        

def getFileView(filename, filepath = '/Users/webstones/Code/ChordsServer/Files'):
    import os
    filepath = os.path.join(filepath,filename)
    def fileview(req:HttpRequest) -> HttpResponse:
        return FileResponse(open(filepath,'rb'), filename=filename)
    return fileview

def getFileViews():
    l = []
    import os
    ROOT = '/Users/webstones/Code/ChordsServer/Files'
    print(ROOT)
    for root, dirs, files in os.walk(ROOT):

        for filename in files:
            l.append(path(filename, getFileView(os.path.relpath(os.path.join(root, filename),ROOT))))
            
    return l