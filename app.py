from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
import config
from utils import youtube_helper
import cloudinary
from datetime import datetime

app = Flask(__name__)

# Database setup
client = MongoClient(config.MONGODB_URI)
db = client[config.DATABASE_NAME]

# Cloudinary setup
cloudinary.config(
  cloud_name = config.CLOUDINARY_CLOUD_NAME,
  api_key = config.CLOUDINARY_API_KEY,
  api_secret = config.CLOUDINARY_API_SECRET
)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        youtube_url = request.form.get("youtube_url")
        download_type = request.form.get("download_type")
        user_id = datetime.now().timestamp()
        if download_type == "video":
            video_url,error_text,error_message= youtube_helper.download_video(youtube_url,user_id)
            if video_url:
                db.downloads.insert_one({'user_id':user_id, 'youtube_url':youtube_url, 'file_url':video_url, 'type': 'video', 'timestamp':datetime.now()})
                return render_template("download_result.html", file_url=video_url,error=error_text)
            else:
                return render_template("index.html", error=error_message)

        elif download_type == "subtitle":
            subtitle_url,error_message=youtube_helper.download_subtitle(youtube_url, user_id)
            if subtitle_url:
              db.downloads.insert_one({'user_id':user_id,'youtube_url':youtube_url, 'file_url':subtitle_url, 'type': 'subtitle', 'timestamp':datetime.now()})
              return render_template("download_result.html", file_url=subtitle_url,error=error_message)
            else:
               return render_template("index.html", error=error_message)
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=config.DEBUG, host="0.0.0.0", port=config.PORT)