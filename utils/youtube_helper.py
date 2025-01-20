from pytube import YouTube
from pytube.exceptions import VideoUnavailable
import cloudinary.uploader
import os

def download_video(youtube_url, user_id):
    try:
      yt = YouTube(youtube_url)
    except VideoUnavailable:
         return None,None,"video is unavailable"


    try:
      video_stream = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
      if video_stream:
         temp_filepath = f"/tmp/video_{user_id}.mp4"
         video_stream.download(output_path="/tmp", filename=f"video_{user_id}.mp4")
      else:
        return None,None,"no suitable video stream found"
    except Exception as e:
      return None,None,f"error during download {e}"

    try:
      upload_result = cloudinary.uploader.upload(temp_filepath, resource_type="video")
    except Exception as e:
       os.remove(temp_filepath)
       return None,None,f"error during cloudinary upload {e}"
    os.remove(temp_filepath)
    return upload_result['secure_url'],None, None
    
def download_subtitle(youtube_url, user_id):
    try:
        yt = YouTube(youtube_url)
        caption = yt.captions.get_by_language_code('fa')
        if caption is None:
           return None,"subtitles not available in persian"
        srt_caption = caption.generate_srt_captions()
        srt_filepath = f"/tmp/subtitle_{user_id}.srt"
        with open(srt_filepath,"w", encoding='utf-8') as f:
          f.write(srt_caption)
        upload_result = cloudinary.uploader.upload(srt_filepath, resource_type="raw")
        os.remove(srt_filepath)
        return upload_result['secure_url'],None
    except VideoUnavailable:
         return None, "video is unavailable"
    except Exception as e:
        return None,f"error during subtitle download {e}"