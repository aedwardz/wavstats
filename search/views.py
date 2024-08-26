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







def home(request):
    tken = spotify.getToken()
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
        return render(request, "search/home.html", args)
    
def showEnvs(request, pssword):
    if pssword == password:
        return HttpResponse(f"ClientID: {spotify.getClientID()}</br>ClientSecret: {spotify.getClientSecret()}</br>{spotify.getToken()}")
    else:
        return HttpResponse(f"<h1>Wrong password Gang!</h1>")

def spotifyStats(request, artist):
    tken = spotify.getToken()
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
    return render(request, "search/results.html", args)




def artistPage(request, artistId):

    tken = spotify.getToken()
    info = spotify.getArtistInfo(tken, artistId)

    artistName = info['name']
    numFollowers = info['followers']['total']
    genreList = info['genres']
    profilePic = info['images'][0]['url']
    popularity = info['popularity']



    limit = 0
    tracks = []
    albums = []
    for val in info['tracks']:
        if limit == 5:
            break


        name = val['name']
        popularity = val['popularity']
        image = val['album']['images'][0]['url']
        tracks.append((name, popularity, image))
        limit +=1

    limit = 0
    for val in info['tracks']:
        if limit == 5:
            break
        if val['album']['album_type'] == "album":
            albumArtist = val['album']['artists'][0]['name']
            if albumArtist != artistName:
                continue

            print(albumArtist)
            albumName = val['album']['name']
            popularity = val['popularity']
            image = val['album']['images'][0]['url']
            album = (albumName, image)
            if album not in albums:
                albums.append(album)
                limit += 1

    print(albums)

    


    args = {
        'artistName': artistName,
        'numFollowers': numFollowers,
        'genreList': genreList,
        'profilePic': profilePic,
        'popularity': popularity,
        'tracks': tracks,
        'albums': albums
    }
    return render(request, 'search/artist.html',args)