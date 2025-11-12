# 🎬 YouTube Automation Agent

**Fully automated YouTube channel management system** that uploads 2 regular videos weekly and 10 shorts daily with trending content detection and smart scheduling.

## ✨ Features

✅ **Automated Upload Scheduling**
- 2 regular videos per week (Monday & Thursday at 3 PM)
- 10 shorts per day (distributed throughout the day every 2.4 hours)
- Customizable upload times and frequencies

✅ **Trending Content Detection**
- Real-time YouTube trending topics analysis
- Category and keyword trending detection
- Hashtag-based content search
- Related video discovery

✅ **Smart Queue Management**
- Add videos and shorts to upload queues
- Automatic scheduling and processing
- Queue size management (max 100 items)
- Upload progress tracking

✅ **SEO Optimization**
- Automatic #Shorts hashtag detection
- Metadata optimization
- YouTube API v3 integration for uploads
- OAuth 2.0 authentication

## 📋 Requirements

- Python 3.8+
- Google Account with YouTube channel
- YouTube Data API v3 enabled
- OAuth 2.0 credentials

## 🚀 Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Get YouTube API Credentials

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project
3. Enable **YouTube Data API v3**
4. Create **OAuth 2.0 credentials** (Desktop application)
5. Download credentials as JSON
6. Save as `client_secret.json` in the project root

### 3. Configure Settings

Edit `config.py` with your settings:

```python
# API Settings
YOUTUBE_API_KEY = 'YOUR_API_KEY'
CLIENT_SECRET_FILE = 'client_secret.json'

# Upload Schedule
WEEKLY_VIDEOS_COUNT = 2
DAILY_SHORTS_COUNT = 10

# Upload Times
WEEKLY_VIDEO_DAYS = ['monday', 'thursday']
WEEKLY_VIDEO_TIME = '15:00'
```

### 4. Prepare Content

Create folder structure:

```
project/
├── videos/           # Place .mp4 videos here
├── shorts/           # Place short videos (< 60 seconds) here
├── youtube_agent.py
├── config.py
├── requirements.txt
└── client_secret.json
```

## 💻 Usage

### Basic Example

```python
from youtube_agent import YouTubeAutomationAgent

# Initialize agent
agent = YouTubeAutomationAgent()

# Add regular video to queue
agent.add_to_video_queue(
    file_path='videos/my_video.mp4',
    title='Amazing YouTube Video',
    description='Check out this viral content!',
    tags=['viral', 'trending', 'youtube']
)

# Add short to queue
agent.add_to_shorts_queue(
    file_path='shorts/quick_clip.mp4',
    title='Quick Tip #1',
    description='30-second tutorial!',
    tags=['shorts', 'tips', 'tutorial']
)

# Set up automatic schedules
agent.schedule_uploads()

# Start the automation
agent.run()
```

### Get Trending Topics

```python
agent = YouTubeAutomationAgent()

# Get trending videos
trending = agent.get_trending_topics(region_code='US', max_results=10)

for topic in trending[:5]:
    print(f"{topic['title']} - {topic['views']} views")
```

### Use Trend Analyzer

```python
from trend_analyzer import TrendAnalyzer
from config import YOUTUBE_API_KEY

analyzer = TrendAnalyzer(YOUTUBE_API_KEY)

# Get keyword suggestions
keywords = analyzer.get_keyword_suggestions('AI technology')
print(f"Trending keywords: {keywords}")

# Search by hashtag
results = analyzer.search_by_hashtag('#viral', max_results=10)
for video in results:
    print(f"{video['title']} by {video['channel']}")
```

## 📁 Project Structure

```
youtube-automation-agent/
├── youtube_agent.py          # Main automation agent
├── trend_analyzer.py         # Trending content analyzer
├── config.py                 # Configuration settings
├── requirements.txt          # Python dependencies
├── README.md                 # This file
├── videos/                   # Regular videos folder
└── shorts/                   # Shorts videos folder
```

## 🔧 File Descriptions

### youtube_agent.py
Main agent class with:
- OAuth 2.0 authentication
- Video/short upload methods
- Scheduling system
- Queue management
- Trending content detection

### trend_analyzer.py
Analyzer class for:
- Trending category analysis
- Keyword suggestions
- Related video discovery
- Hashtag-based searching

### config.py
Configuration file with:
- API settings
- Schedule times
- Content folders
- Queue limits
- Trending detection intervals

## 📊 Upload Schedule

**Regular Videos**: 2 per week
- Monday at 3:00 PM
- Thursday at 3:00 PM

**Shorts**: 10 per day at
- 8:00 AM, 10:00 AM, 12:00 PM, 2:00 PM, 4:00 PM
- 6:00 PM, 8:00 PM, 10:00 PM, 12:00 AM, 2:00 AM

## ⚠️ Important Notes

1. **Video Requirements**
   - Regular videos: Any format, any length
   - Shorts: Under 60 seconds, vertical format (9:16)

2. **API Quotas**
   - YouTube API has daily quota limits
   - Each upload costs ~1,600 quota units
   - Free tier: 10,000 quota/day

3. **Authentication**
   - First run requires browser login
   - Token saved in `token.pickle`
   - Re-authenticate if token expires

4. **Content Policy**
   - Follow YouTube Community Guidelines
   - Avoid copyright violations
   - Use original or licensed content

## 🐛 Troubleshooting

**"Authentication failed"**
- Delete `token.pickle`
- Delete `client_secret.json`
- Re-download credentials from Google Cloud Console

**"Video not uploading"**
- Check video file format (.mp4 recommended)
- Verify file path is correct
- Ensure sufficient API quota

**"Schedule not running"**
- Keep script running 24/7 (use PM2, Docker, etc.)
- Verify system time is correct
- Check for Python errors in logs

## 📝 License

MIT License - Feel free to use and modify

## 🤝 Contributing

Pull requests welcome! For major changes, open an issue first.

## 📧 Support

For issues and questions, create a GitHub issue or email: support@example.com
