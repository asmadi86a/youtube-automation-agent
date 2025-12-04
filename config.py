# YouTube Agent Configuration

# 🚀 GEMINI API - Main AI Engine
GEMINI_API_KEY = 'YOUR_GEMINI_API_KEY_HERE'  # Get from https://aistudio.google.com/app/apikey

# 📱 TikTok API (Optional - get from https://developers.tiktok.com/)
TIKTOK_ACCESS_TOKEN = 'YOUR_TIKTOK_ACCESS_TOKEN'  # Free developer account

# 🎥 Pexels API for free stock footage
PEXELS_API_KEY = 'YOUR_PEXELS_API_KEY'  # Get from https://www.pexels.com/api/

# API Settings
YOUTUBE_API_KEY = 'YOUR_API_KEY_HERE'
YOUTUBE_CLIENT_ID = 'YOUR_CLIENT_ID'  # From Google Cloud Console
YOUTUBE_CLIENT_SECRET = 'YOUR_CLIENT_SECRET'  # From Google Cloud Console
CLIENT_SECRET_FILE = 'client_secret.json'

# Upload Schedule
WEEKLY_VIDEOS_COUNT = 2  # Videos per week
DAILY_SHORTS_COUNT = 10  # Shorts per day

# Upload Times
WEEKLY_VIDEO_DAYS = ['monday', 'thursday']  # Days to upload videos
WEEKLY_VIDEO_TIME = '15:00'  # 3 PM

SHORTS_SCHEDULE = [  # Times for 10 shorts/day
    '08:00', '10:00', '12:00', '14:00', '16:00',
    '18:00', '20:00', '22:00', '00:00', '02:00'
]

# Content Settings
DEFAULT_CATEGORY = '22'  # People & Blogs
DEFAULT_PRIVACY = 'public'
DEFAULT_REGION = 'US'

# Queue Settings
VIDEO_FOLDER = './videos/'
SHORTS_FOLDER = './shorts/'
MAX_QUEUE_SIZE = 100

# Trending Topics
TRENDING_CHECK_INTERVAL = 3600  # Check every hour
MIN_VIEWS_THRESHOLD = 100000
