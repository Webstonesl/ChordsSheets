from django.shortcuts import render
from django.http import *
from .models import Event, EventRole
from django.contrib.auth import decorators
from django.utils import dateparse
from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.contrib.auth.models import User

RoleChoices = {
    0: 'Owner',
    1: 'Manager',
    2: 'Cast / Crew',
    3: 'Attendee'
}
# Create your views here.
@decorators.login_required
def new_show(req: HttpRequest, pk=None):
    event = Event()
    myrole = EventRole(event=event,user=req.user,role=0)
    if pk != None:
        try:
            event = Event.objects.get(pk=pk)
            try:
                myrole = EventRole.objects.filter(user=req.user, event=event).get()
            except ObjectDoesNotExist:
                return HttpResponseForbidden()
            except MultipleObjectsReturned:
                roles = EventRole.objects.filter(user=req.user,event=event).order_by('role')
                myrole = roles[0]
                for role in roles[1:]:
                    role.delete()

                
        except ObjectDoesNotExist:
            return HttpResponseNotFound()

    if req.method == "GET":
        return render(
            req,
            "edit_show.html",
            {
                "title": "New Show",
                "event": event,
                "roles": [{"user": req.user.username, "role": {'name': RoleChoices[0],'value':0}, 'editable':False}]
                if pk is None
                else [{'user':role.user.username, 'role':{'value':role.role, 'name':RoleChoices[role.role]}, 'editable': (role.role>0)and(myrole.role==0)} for role in EventRole.objects.filter(event=event).order_by('role')],
                "roleNames": [{'value':k,'label':RoleChoices[k]} for k in RoleChoices],
                'editroles': True
            },
        )
    elif req.method == 'POST':

        import re
        event = Event()
        if pk != None:
            event = Event.objects.get(pk=pk)
        if req.POST.get('delete') == 'True':
            event.delete()
            return HttpResponseRedirect('/')
        event.title = str(req.POST.get("title"))

        event.start = datetime.strptime(req.POST.get("start"), "%Y-%m-%dT%H:%M")
        event.save()
        uns = []
        for key in req.POST.keys():
            m = re.match(r'^(.*?)_role$',key)

            if (m is not None):
                r = int(req.POST.get(key))
                username = m.group(1)
                uns.append(username)
                role = None 
                try:
                    role = EventRole.objects.filter(event=event,user__username=username).get()
                    role.role = r
                    role.save()
                except ObjectDoesNotExist:
                    role = EventRole()
                    role.event = event
                    role.user = User.objects.get(username=username)
                    role.role = r
                    role.save()
        for role in EventRole.objects.filter(event=event):
            if (role.user.username not in uns):
                role.delete()
            
        
        if len(EventRole.objects.filter(user=req.user, event=event)) == 0:
            EventRole.objects.create(user=req.user, event=event, role=0)
        return HttpResponseRedirect("/")
