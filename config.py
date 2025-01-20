import os
from dotenv import load_dotenv

load_dotenv()

# MongoDB Atlas Config
MONGODB_URI = os.getenv("MONGODB_URI")
DATABASE_NAME = os.getenv("DATABASE_NAME", "youtube_downloader_db")

# Cloudinary Config
CLOUDINARY_CLOUD_NAME = os.getenv("CLOUDINARY_CLOUD_NAME")
CLOUDINARY_API_KEY = os.getenv("CLOUDINARY_API_KEY")
CLOUDINARY_API_SECRET = os.getenv("CLOUDINARY_API_SECRET")

# Other Settings
DEBUG = os.getenv("DEBUG", "False") == "True"
PORT = int(os.getenv("PORT", 5000))