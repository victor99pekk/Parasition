import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from config import *
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=CLIENT_ID,
                                                           client_secret=CLIENT_SECRET))

def get_similar_songs(track_name, artist_name):
    # Search for the track
    results = sp.search(q=f"track:{track_name} artist:{artist_name}", type="track", limit=1)
    if not results['tracks']['items']:
        return "Song not found."
    
    track_id = results['tracks']['items'][0]['id']
    
    # Get recommendations based on the track
    recommendations = sp.recommendations(seed_tracks=[track_id], limit=5)
    
    # Extract song names and artists
    similar_songs = [(track['name'], track['artists'][0]['name']) for track in recommendations['tracks']]
    
    return similar_songs

# Example usage
similar_songs = get_similar_songs("Blinding Lights", "The Weeknd")
for song, artist in similar_songs:
    print(f"{song} by {artist}")
