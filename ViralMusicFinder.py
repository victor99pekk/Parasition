from LastfmAPI import LastfmAPI

class ViralMusicFinder:
    def __init__(self, API_KEY, API_SECRET):
        self.API_KEY = API_KEY
        self.API_SECRET = API_SECRET
        self.music_api = LastfmAPI(API_KEY, API_SECRET)
    