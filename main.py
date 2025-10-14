import logging
from flask import Flask, request
import requests
from google.cloud import storage

app = Flask(__name__)

@app.route("/", methods=["GET"])
def download_and_upload_news():
    try:
        news_url = "https://video.news.sky.com/snr/news/snrnews.mp3"
        bucket_name = "blockytime"
        destination_blob_name = "RADIO STATION/News/snrnews_test.mp3"

        response = requests.get(news_url, stream=True)
        if response.status_code != 200:
            logging.error(f"Failed to download news file: {response.status_code}")
            return f"Failed to download Sky News MP3: {response.status_code}", 500

        client = storage.Client()
        bucket = client.bucket(bucket_name)
        blob = bucket.blob(destination_blob_name)

        blob.upload_from_string(response.content, content_type="audio/mpeg")

        # Removed blob.make_public() as bucket is already public

        return f"Uploaded news file to: https://storage.googleapis.com/{bucket_name}/{destination_blob_name}", 200

    except Exception as e:
        logging.exception("Error in download_and_upload_news:")
        return f"Internal Server Error: {str(e)}", 500

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
