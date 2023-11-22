from django.shortcuts import render
from django.shortcuts import render
from django.http import *
from .models import *
from django.contrib.auth.models import User
# Create your views here.
def list_songs(req:HttpRequest):
    sheets = ChordSheet.objects.filter(chordsheetroles__user=req.user).order_by('chordsheetroles__lastupdate')
    return render(req,'list_songs.html',{'title': 'Chordsheets','sheets':sheets})

def edit_song(req:HttpRequest, pk= None):
    cs = {'bpm':60,'key':'A','mod':'m','metre_1':4,'metre_2':4, 'content':[]}
    if (pk != None):
        cs = ChordSheet.objects.get(pk=pk)

    return render(req,'chordsheet_editor.html',{'title': 'Chordsheets','cs':cs})