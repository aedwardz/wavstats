from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.template.loader import render_to_string
import sys
from dotenv import load_dotenv
import os
from . import spotify
from django.urls import reverse
from .forms import text_form

load_dotenv()


password = os.getenv("PASSWORD")
# Create your views here.


tken = spotify.getToken()




def home(request):
    if request.method == 'POST':
        form = text_form(request.POST)
        if form.is_valid():
            query = form.cleaned_data['artist']
            redirectUrl = reverse("spotify_stats",args=[query])
            return HttpResponseRedirect(redirectUrl)
    else:
        form = text_form()
        args = {
            'form': form,      
        }
        return render(request, "challenges/home.html", args)
    

def index(request):
    return HttpResponseNotFound("This does not work!!")

def func(request):
    
    return HttpResponse(f"{x}\n" for x in sys.__dict__)

def games(request, game):
    return HttpResponse(f"<h1>{game} is my favorite game</h1>")

def showEnvs(request, pssword):
    if pssword == password:
        return HttpResponse(f"ClientID: {spotify.getClientID()}</br>ClientSecret: {spotify.getClientSecret()}</br>{spotify.getToken()}")
    else:
        return HttpResponse(f"<h1>Wrong password Gang!</h1>")

def spotifyStats(request, artist):
    result = spotify.searchArtist(tken, artist)
    resCount = 0

    for thing in result:
        resCount += 1

    info = dict(result[0].items())

    images: list = info['images']
    images = [x['url'] for x in images]
    
    
    args = {
        "search_data": result,
        "resultCount": resCount,
        "artistName": artist
    }
    return render(request, "challenges/results.html", args)