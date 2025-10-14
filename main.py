import logging
import hashlib
from flask import Flask
import requests
from google.cloud import storage

app = Flask(__name__)

@app.route("/", methods=["GET"])
def download_and_upload_news():
    try:
        news_url = "https://video.news.sky.com/snr/news/snrnews.mp3"
        bucket_name = "blockytime"
        destination_blob_name = "RADIO STATION/News/snrnews.mp3"

        # Force fresh download from Sky CDN
        headers = {"Cache-Control": "no-cache"}
        response = requests.get(news_url, headers=headers)
        if response.status_code != 200:
            logging.error(f"Failed to download news file: {response.status_code}")
            return f"Failed to download Sky News MP3: {response.status_code}", 500

        # Compute MD5 for verification
        file_hash = hashlib.md5(response.content).hexdigest()
        logging.info(f"Downloaded Sky MP3: {len(response.content)} bytes, MD5: {file_hash}")

        # Upload to GCS
        client = storage.Client()
        bucket = client.bucket(bucket_name)
        blob = bucket.blob(destination_blob_name)

        # Prevent caching
        blob.cache_control = "no-cache"
        blob.upload_from_string(response.content, content_type="audio/mpeg")
        blob.patch()  # Apply metadata immediately

        logging.info(f"File uploaded successfully to GCS: {destination_blob_name}")

        return f"Uploaded news file to: https://storage.googleapis.com/{bucket_name}/{destination_blob_name} (MD5: {file_hash})", 200

    except Exception as e:
        logging.exception("Error in download_and_upload_news:")
        return f"Internal Server Error: {str(e)}", 500


if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
