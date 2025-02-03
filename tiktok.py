import os
import sys
from TikTokApi import TikTokApi

def find_most_viral_videos_for_song(song_query, max_videos=30):
    """
    Given a song query (e.g. song title), this function:
      1. Searches for matching audio on TikTok.
      2. Retrieves videos that use that sound.
      3. Sorts those videos by a virality metric (using likes).
    Returns a list of videos (as JSON objects).
    """
    # Initialize the TikTokApi session
    with TikTokApi() as api:
        # 1. Search for music matching the query.
        search_results = api.search_for_music(query=song_query, count=1)
        if not search_results or 'musics' not in search_results:
            print("No music found for query:", song_query)
            return []

        # Assume the first result is the desired audio.
        music_info = search_results['musics'][0]
        music_id = music_info.get('id')
        if not music_id:
            print("Failed to get music ID from search results.")
            return []

        # 2. Retrieve videos using this music ID
        videos_data = api.music(music_id, count=max_videos)
        if not videos_data:
            print(f"No videos found for music ID: {music_id}")
            return []

        # 3. Sort videos by like count (using 'diggCount' as the virality metric)
        sorted_videos = sorted(
            videos_data, 
            key=lambda x: x.get('stats', {}).get('diggCount', 0),
            reverse=True
        )
        return sorted_videos

if __name__ == "__main__":
    if len(sys.argv) > 1:
        song_query = " ".join(sys.argv[1:])
    else:
        print("Usage: python tiktok_music_lookup.py '<song name>'")
        sys.exit(1)

    results = find_most_viral_videos_for_song(song_query, max_videos=50)
    
    print(f"Found {len(results)} videos for song '{song_query}':")
    for i, video in enumerate(results[:10], start=1):
        stats = video.get("stats", {})
        likes = stats.get("diggCount", 0)
        shares = stats.get("shareCount", 0)
        comments = stats.get("commentCount", 0)
        video_id = video.get("id", "N/A")
        print(f"{i}. Video ID: {video_id} | Likes: {likes}, Shares: {shares}, Comments: {comments}")

