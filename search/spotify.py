import requests
from os import getenv
from dotenv import load_dotenv
import os
import base64
from requests import post, get
import json


load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

def getClientID():
    return client_id

def getClientSecret():
    return client_secret

def getToken():
    """
    Returns a token retrieved from spotify api
    """
    
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

    url = "https://accounts.spotify.com/api/token"

    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"
    }

    data = {"grant_type": "client_credentials"}
    result = post(url, headers =headers, data = data)
    json_result = json.loads(result.content)
    token = json_result["access_token"]
    return token

def getAuthHeader(token):
    return {"Authorization": "Bearer " + token}

def createQuery(**kwargs):
    query="?"
    for key, value in kwargs.items():
        query+= f"{key}={value}&"
    
    ind = query.rfind('&')
    query = query[:ind] + query[ind+1:]
    return query

def searchArtist(token, artist_name):
    endpoint = "https://api.spotify.com/v1/search"

    headers = getAuthHeader(token)
    query = f"?q={artist_name}&type=artist"

    url = endpoint + query
    result = get(url, headers=headers)
    json_result = json.loads(result.content)
    return json_result['artists']['items']



def getArtistInfo(token, artistId) -> json:
   endpoint = "https://api.spotify.com/v1/artists/" + artistId
   headers = getAuthHeader(token)

   result = get(endpoint, headers=headers)
   json_result = json.loads(result.content)
   endpoint = f"https://api.spotify.com/v1/artists/{artistId}/top-tracks"
   result = get(endpoint, headers = headers)
   topTracks = json.loads(result.content)
   json_result.update(topTracks)
   return json_result



if __name__ == "__main__":
    tkn = getToken()
    resCount = 0
    result = getArtistInfo(tkn,"0TnOYISbd1XYRBk9myaseg")
    for album in result['tracks']:
        for key, val in album.items():
            print(f"{key} : {val}")

