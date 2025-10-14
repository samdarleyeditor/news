from flask import Flask, request
import requests
from google.cloud import storage

app = Flask(__name__)

@app.route("/", methods=["GET"])
def download_and_upload_news():
    news_url = "https://video.news.sky.com/snr/news/snrnews.mp3"
    bucket_name = "blockytime"
    destination_blob_name = "RADIO STATION/News/snrnews.mp3"

    response = requests.get(news_url, stream=True)
    if response.status_code != 200:
        return f"Failed to download Sky News MP3: {response.status_code}", 500

    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_string(response.content, content_type="audio/mpeg")
    blob.make_public()

    return f"Uploaded news file to: {blob.public_url}", 200

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
