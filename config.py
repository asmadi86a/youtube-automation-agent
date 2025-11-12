# YouTube Agent Configuration
# API Settings
YOUTUBE_API_KEY = 'YOUR_API_KEY_HERE'
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
