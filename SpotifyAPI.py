import requests
import base64
from config import *

class SpotifyAPI:

    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret
        self.access_token = self.get_access_token()
        
    def get_access_token(self):
        url = "https://accounts.spotify.com/api/token"
        headers = {
                "Authorization": "Basic " + base64.b64encode(f"{self.client_id}:{self.client_secret}".encode()).decode(),
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
    
    def get_recommendations(self, track_id, artist_id=None, genre=None, limit=5):
        url = "https://api.spotify.com/v1/recommendations"
        headers = {"Authorization": f"Bearer {self.access_token}"}
        
        params = {
            "seed_tracks": track_id,
            "limit": limit
        }

        # Add artist or genre if provided
        if artist_id:
            params["seed_artists"] = artist_id
        if genre:
            params["seed_genres"] = genre

        print(f"Request URL: {url}")
        print(f"Params: {params}")

        response = requests.get(url, headers=headers, params=params)
        response = requests.get('https://api.spotify.com/v1/recommendations?seed_artists=4NHQUGzhtTLFvgF5SZesLK&seed_genres=classical%2Ccountry&seed_tracks=0c6xIDDpzE81m2q797ordA', headers=headers)

        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            print(f"Error Response: {response.text}")
            raise e

        data = response.json()
        return [track["name"] + " - " + track["artists"][0]["name"] for track in data["tracks"]]





# Initialize API with credentials
spofity = SpotifyAPI(CLIENT_ID, CLIENT_SECRET)

# Fetch track ID based on artist name
track_ids = spofity.get_ids(artist="Justin Bieber")
print(track_ids[0])
if track_ids:
    recommended_songs = spofity.get_recommendations(track_ids[0])
    print("\nRecommended Songs:")
    for song in recommended_songs:
        print(song)
else:
    print("No tracks found for this artist.")