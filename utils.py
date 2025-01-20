import os
import tempfile
from pytube import YouTube
import cloudinary
import cloudinary.uploader
from moviepy.editor import VideoFileClip

def download_and_upload_video(youtube_url, db_client, cloudinary_config):
    try:
        yt = YouTube(youtube_url)
        stream = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()

        if stream:
            temp_file = tempfile.NamedTemporaryFile(suffix=".mp4", delete=False)
            stream.download(output_path=os.path.dirname(temp_file.name), filename=os.path.basename(temp_file.name))
            temp_file.close()
            
            cloudinary.config(cloud_name=cloudinary_config['cloud_name'],
                    api_key=cloudinary_config['api_key'],
                    api_secret=cloudinary_config['api_secret'])
            
            upload_result = cloudinary.uploader.upload(temp_file.name, resource_type="video")
            
            db = db_client.get_database('youtube_downloader')
            videos_collection = db.get_collection('videos')

            video_data = {
                "youtube_url": youtube_url,
                "cloudinary_url": upload_result['secure_url'],
                "title": yt.title
            }

            videos_collection.insert_one(video_data)


            os.remove(temp_file.name)
            return upload_result['secure_url']
        else:
            return None

    except Exception as e:
        print(f"An error occurred: {e}")
        return None


def download_and_upload_subtitle(youtube_url, db_client):
     try:
            yt = YouTube(youtube_url)
            caption = yt.captions.get_by_language_code('en') # or your desired language

            if caption:
                subtitle_content = caption.generate_srt_captions()
                
                db = db_client.get_database('youtube_downloader')
                subtitles_collection = db.get_collection('subtitles')
                
                subtitle_data = {
                    "youtube_url": youtube_url,
                    "subtitle_text": subtitle_content,
                     "title": yt.title
                }
                
                subtitles_collection.insert_one(subtitle_data)

                return subtitle_content
            else:
                 return None
     except Exception as e:
        print(f"An error occurred: {e}")
        return None