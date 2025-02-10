import pylast

class LastfmAPI:

    def __init__(self, API_KEY, API_SECRET):
        self.API_KEY = API_KEY
        self.API_SECRET = API_SECRET
        self.access_token = self.get_access_token()
        self.network = pylast.LastFMNetwork(api_key=API_KEY, api_secret=API_SECRET)

    def get_similar_tracks(self, song, artist):
        track = self.network.get_track(artist, song)
        similar_tracks = track.get_similar(limit=5)
        
        return [(t.item.title, t.item.artist.name) for t in similar_tracks]

# similar_tracks = get_similar_tracks("billie jean", "micheal jackson")
# for song, artist in similar_tracks:
#     print(f"{song} by {artist}")