import requests
import base64
from config import *

class SpotifyAPI:

    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret
        
    def get_access_token():
        url = "https://accounts.spotify.com/api/token"
        headers = {
                "Authorization": "Basic " + base64.b64encode(f"{CLIENT_ID}:{CLIENT_SECRET}".encode()).decode(),
                "Content-Type": "application/x-www-form-urlencoded",
        }
        data = {"grant_type": "client_credentials"}

        response = requests.post(url, headers=headers, data=data)
        response.raise_for_status()  # Raise an error for bad status codes
        return response.json().get("access_token")
    
    def get_ids(self, nbr_ids:int=1, artist:str=None,track:str=None):
        # Get a valid access token
        access_token = self.get_access_token()

        # Use the access token to make the search request
        if artist and track:
            query = f"track:{track} artist:{artist}"
            #query = 'track:Doxy artist:Miles Davis'
        elif artist:
            query = f"artist:{artist}"
            #query = 'artist:Miles Davis'
        elif track:
            query = f"track:{track}"


        url = f'https://api.spotify.com/v1/search?q={query}&type=track'
        headers = {
                'Authorization': f'Bearer {access_token}'
        }

        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an error for bad status codes
        data = response.json()

        arr = data["tracks"]["items"]
        arr = data["tracks"]["items"]
        sorted_arr = sorted(arr, key=lambda x: x['popularity'], reverse=True)

        return [sorted_arr[i]["id"] for i in range(nbr_ids)]