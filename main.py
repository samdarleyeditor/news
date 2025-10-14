import requests
from google.cloud import storage

def download_and_upload_news(request):
    news_url = "https://video.news.sky.com/snr/news/snrnews.mp3"
    bucket_name = "your-bucket-name"  # <-- CHANGE THIS
    destination_blob_name = "news/snrnews.mp3"

    response = requests.get(news_url, stream=True)
    if response.status_code != 200:
        return f"Failed to download: {response.status_code}", 500

    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_string(response.content, content_type="audio/mpeg")
    blob.make_public()

    return f"Uploaded news file: {blob.public_url}", 200
