# YouTube Automation Agent - Complete Setup Guide

## Step 1: Get YouTube API Credentials

### 1a. Create a Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Click **"Select a Project"** at the top
3. Click **"NEW PROJECT"**
4. Enter project name: `youtube-automation-agent`
5. Click **CREATE**
6. Wait for project to be created

### 1b. Enable YouTube Data API v3

1. In the Cloud Console, go to **APIs & Services > Library**
2. Search for "YouTube Data API v3"
3. Click on **YouTube Data API v3**
4. Click **ENABLE**
5. Wait for API to be enabled (takes ~30 seconds)

### 1c. Create OAuth 2.0 Credentials

1. Go to **APIs & Services > Credentials**
2. Click **+ CREATE CREDENTIALS**
3. Select **OAuth client ID**
4. If prompted, configure OAuth consent screen:
   - Click **CONFIGURE CONSENT SCREEN**
   - Select **External** user type
   - Click **CREATE**
   - Fill in required fields:
     - App name: `YouTube Automation Agent`
     - User support email: [Your email]
     - Developer contact: [Your email]
   - Click **SAVE AND CONTINUE**
   - Skip optional scopes, click **SAVE AND CONTINUE**
   - Click **BACK TO DASHBOARD**

5. Now create credentials:
   - Go back to **Credentials**
   - Click **+ CREATE CREDENTIALS**
   - Select **OAuth client ID**
   - Choose **Desktop application**
   - Name: `YouTube Agent`
   - Click **CREATE**

6. Download the credentials:
   - You'll see the credentials created
   - Click the download icon (down arrow)
   - Save as `client_secret.json` in your project root

## Step 2: Set Up Local Environment

### 2a. Clone and Setup

```bash
# Clone the repository
git clone https://github.com/asmadi86a/youtube-automation-agent.git
cd youtube-automation-agent

# Run automated setup
chmod +x setup.sh
./setup.sh
```

### 2b. Place Credentials

1. Copy your `client_secret.json` to the project root
2. The first run will:
   - Open a browser for authentication
   - Ask permission to manage your YouTube channel
   - Create `token.pickle` automatically

## Step 3: Configure the Agent

### 3a. Edit .env File

```bash
cp .env.example .env
```

Edit `.env` and fill in:

```env
# After first run, these will be auto-populated
YOUTUBE_API_KEY=your_api_key_here
YOUTUBE_CLIENT_ID=your_client_id.apps.googleusercontent.com
YOUTUBE_CLIENT_SECRET=your_client_secret_here
YOUTUBE_REFRESH_TOKEN=your_refresh_token_here

# Upload paths
VIDEOS_FOLDER=./videos
SHORTS_FOLDER=./shorts
LOGS_FOLDER=./logs

# Schedule settings (2 videos/week, 10 shorts/day)
WEEKLY_VIDEOS_COUNT=2
DAILY_SHORTS_COUNT=10
VIDEO_UPLOAD_DAY_1=monday
VIDEO_UPLOAD_TIME_1=15:00
VIDEO_UPLOAD_DAY_2=thursday
VIDEO_UPLOAD_TIME_2=15:00
```

### 3b. Add Video Content

Create folders and add your content:

```bash
# Create content directories if not exists
mkdir -p videos shorts

# Add your videos
# Place .mp4 files in videos/ folder
# Place .mp4 short files in shorts/ folder

# Example structure:
# videos/
#   ├── weekly_video_1.mp4
#   └── weekly_video_2.mp4
# shorts/
#   ├── short_1.mp4
#   ├── short_2.mp4
#   └── ...(up to 10 shorts)
```

## Step 4: Run the Agent

### 4a. Activate Virtual Environment

```bash
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 4b. Start the Agent

```bash
# First run - will authenticate
python youtube_agent.py

# Follow prompts to authorize access to your YouTube channel
# Browser window will open automatically
```

### 4c. Run with Docker (Alternative)

```bash
# Build and run
docker-compose up --build

# View logs
docker-compose logs -f youtube-agent

# Stop
docker-compose down
```

## Step 5: Monitor Execution

### 5a. Check Logs

```bash
# View real-time logs
tail -f logs/agent.log

# View all logs
cat logs/agent.log
```

### 5b. Verify in YouTube Studio

1. Go to [YouTube Studio](https://studio.youtube.com)
2. Check **Content > Uploads** for scheduled videos
3. Check **Shorts** for scheduled shorts
4. Verify timestamps match your config

### 5c. Check Database Queue

```bash
# View queue database
python -c "import sqlite3; db=sqlite3.connect('queue.db'); cursor=db.cursor(); cursor.execute('SELECT * FROM uploads'); print(cursor.fetchall())"
```

## Troubleshooting

### "Invalid Credentials"
- Re-run first step to get new `client_secret.json`
- Delete `token.pickle` and re-authenticate

### "API Quota Exceeded"
- YouTube API has quota limits
- Default is 10,000 units/day
- Each upload uses ~1,500 units
- Reduce upload frequency if needed

### "Videos Not Uploading"
- Check file format (.mp4 recommended)
- Verify video quality and duration
- Check YouTube channel restrictions
- Review logs for specific errors

### "Authentication Fails"
1. Delete `token.pickle`
2. Delete `client_secret.json`
3. Get new credentials from Google Cloud Console
4. Place new `client_secret.json` in project root
5. Run agent again

## API Credentials Location

- **Client Secret**: `./client_secret.json` (obtained from Google Cloud)
- **Token Pickle**: `./token.pickle` (auto-created on first run)
- **Environment Variables**: `./.env` (user configuration)

## Security Notes

⚠️ **IMPORTANT**: Never commit these files to Git:
- `.env` (add to .gitignore)
- `client_secret.json` (add to .gitignore)
- `token.pickle` (add to .gitignore)

They're already in `.gitignore` - verify with:

```bash
cat .gitignore
```

## Next Steps

1. ✅ Get API credentials (this guide)
2. ✅ Configure agent (.env file)
3. ✅ Add video content
4. ✅ Run the agent
5. ✅ Monitor execution

For issues, check README.md or create a GitHub issue.
