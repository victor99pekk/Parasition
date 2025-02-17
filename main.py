from TikAPI import TikAPIWrapper
from GoogleCloud import GCSVideoUploader
from GoogleVideoAnalyzer import GoogleVideoAnalyzer

def analyze_and_process_videos(tikapi, uploader, analyzer, videos, n=3):
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

        video_json = tikapi.get_video_metadata(video_id)
        if not video_json:
            continue

        gcs_url = uploader.upload_tiktok_video_direct(video_json)
        if not gcs_url:
            continue

        labels = analyzer.analyze_video_labels(gcs_url)
        print(f"Labels for video {video_id}: {labels}")


def main():
    tikapi = TikAPIWrapper()
    uploader = GCSVideoUploader()  
    analyzer = GoogleVideoAnalyzer()

    user_title = input("Enter song title: ")
    user_artist = input("Enter artist name: ")

    print("\nSearching for matching music on TikTok...")
    music_list = tikapi.search_music(user_title, user_artist)

    if not music_list:
        print("No songs found.")
        return

    if len(music_list) == 1:
        matched_song = music_list[0]
        print(f"Quick match: Music ID {matched_song}")
    else:
        matched_song = tikapi.find_matching_song(user_title, user_artist, music_list)
        if not matched_song:
            print("No close match found among multiple IDs.")
            return

    print(f"\nFetching videos for Music ID {matched_song}")
    music_videos = tikapi.fetch_music_videos(matched_song, limit=3)

    print("\nUploading & analyzing top videos...")
    analyze_and_process_videos(tikapi, uploader, analyzer, music_videos, n=3)


if __name__ == "__main__":
    main()
