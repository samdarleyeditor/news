import requests
from google.cloud import storage

def download_and_upload_news(request):
    # URL of the Sky News MP3 file
    news_url = "https://video.news.sky.com/snr/news/snrnews.mp3"

    # Google Cloud Storage settings
    bucket_name = "blockytime"
    destination_blob_name = "RADIO STATION/News/snrnews.mp3"  # <-- new filename

    # Download the MP3
    response = requests.get(news_url, stream=True)
    if response.status_code != 200:
        return f"Failed to download Sky News MP3: {response.status_code}", 500

    # Upload to Google Cloud Storage
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_string(response.content, content_type="audio/mpeg")
    blob.make_public()  # Optional: make it publicly accessible

    return f"Uploaded news file to: {blob.public_url}", 200
