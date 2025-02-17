import requests
from google.cloud import storage
from config import *
class GCSVideoUploader:
    def __init__(self):
        self.storage_client = storage.Client()
        self.bucket_name = bucket_name1
        self.bucket = self.storage_client.bucket(self.bucket_name)

    def upload_tiktok_video_direct(self, video_json, blob_name=None):
        try:
            video_info = video_json.get('itemInfo', {}).get('itemStruct', {}).get('video', {})
            video_url = video_info.get('downloadAddr')
            video_headers = video_json.get('$other', {}).get('videoLinkHeaders', {})

            if not blob_name:
                video_id = video_json.get('itemInfo', {}).get('itemStruct', {}).get('id', 'unknown_video')
                blob_name = f"tikapi_videos/{video_id}.mp4"

            if not video_url:
                print("No downloadAddr found in video JSON")
                return None

            resp = requests.get(video_url, headers=video_headers, stream=True)
            resp.raise_for_status()

            blob = self.bucket.blob(blob_name)
            blob.upload_from_string(resp.content, content_type='video/mp4')

            gcs_url = f"gs://{self.bucket.name}/{blob_name}"
            print(f" Video uploaded to {gcs_url}")
            return gcs_url

        except requests.exceptions.RequestException as re:
            print(f"Error downloading video content: {re}")
        except Exception as ex:
            print(f"Error uploading video: {ex}")

        return None
