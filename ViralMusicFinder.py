from GoogleVideoAnalyzer import GoogleVideoAnalyzer
from LastfmAPI import LastfmAPI
from TikAPI import TikAPIWrapper
from config import *
from GoogleCloud import *

class ViralMusicFinder:
    def __init__(self, API_KEY, API_SECRET):
        self.API_KEY = API_KEY
        self.API_SECRET = API_SECRET
        self.music_api = LastfmAPI(API_KEY, API_SECRET)
        self.tiktok_api = TikAPIWrapper()
        self.Uploader = GCSVideoUploader()
        self.Analyzer = GoogleVideoAnalyzer()

    def find_tiktoks(self, song:str=None, artist:str=None) -> None:
        # song and artist are two strings
        song, artist = self.music_api.get_similar_tracks(song=song, artist=artist, limit=5)[0]

        print(f"\nsimilar artist: {artist}\nsimilar song: {song}\n\n")

        music_list = self.tiktok_api.search_music(song, artist)
    
        matched_song = self.tiktok_api.find_matching_song(song, artist, music_list)
        music_videos = self.tiktok_api.fetch_music_videos(matched_song, limit=3)
        self.analyze_and_process_videos(music_videos)


    def analyze_and_process_videos(self, videos, n=3):
        """
        Process the top `n` videos: upload them to GCS, then run analysis.
        """
        if not videos:
            print("No videos found for analysis.")
            return

        for i, video in enumerate(videos[:n], start=1):
            video_id = video.get("id")
            if not video_id:
                continue

            print(f"\nProcessing Video {i}/{n} (ID: {video_id})")

            video_json = self.tiktok_api.get_video_metadata(video_id)
            if not video_json:
                continue

            gcs_url = self.Uploader.upload_tiktok_video_direct(video_json)
            if not gcs_url:
                continue

            labels = self.Analyzer.analyze_video_labels(gcs_url)
            print(f"Labels for video {video_id}: {labels}")


# för att testa klassen
if __name__ == "__main__":
    music_find = ViralMusicFinder(API_KEY, API_SECRET)

    # Get similar tracks
    music_find.find_tiktoks(song="homecoming")
    
