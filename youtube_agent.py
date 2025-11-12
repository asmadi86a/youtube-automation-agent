import os
import time
from datetime import datetime, timedelta
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import schedule
import pickle

class YouTubeAutomationAgent:
    def __init__(self):
        self.SCOPES = ['https://www.googleapis.com/auth/youtube.upload',
                       'https://www.googleapis.com/auth/youtube.readonly']
        self.youtube = self.authenticate()
        self.video_queue = []
        self.shorts_queue = []
        
    def authenticate(self):
        """Authenticate with YouTube API"""
        creds = None
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
                
        if not creds or not creds.valid:
            flow = InstalledAppFlow.from_client_secrets_file(
                'client_secret.json', self.SCOPES)
            creds = flow.run_local_server(port=0)
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)
                
        return build('youtube', 'v3', credentials=creds)
    
    def upload_video(self, file_path, title, description, tags, category_id='22', 
                     privacy_status='public', is_short=False):
        """Upload video to YouTube"""
        
        # Add #Shorts to title/description for shorts
        if is_short:
            if '#Shorts' not in title and '#Shorts' not in description:
                description = f"{description}\n\n#Shorts"
        
        body = {
            'snippet': {
                'title': title,
                'description': description,
                'tags': tags,
                'categoryId': category_id
            },
            'status': {
                'privacyStatus': privacy_status,
                'selfDeclaredMadeForKids': False
            }
        }
        
        media = MediaFileUpload(file_path, 
                               chunksize=-1, 
                               resumable=True,
                               mimetype='video/*')
        
        request = self.youtube.videos().insert(
            part=','.join(body.keys()),
            body=body,
            media_body=media
        )
        
        response = None
        while response is None:
            status, response = request.next_chunk()
            if status:
                print(f"Upload {int(status.progress() * 100)}% complete")
                
        print(f"Video uploaded! ID: {response['id']}")
        return response['id']
    
    def get_trending_topics(self, region_code='US', max_results=10):
        """Fetch trending videos for content ideas"""
        request = self.youtube.videos().list(
            part='snippet,statistics',
            chart='mostPopular',
            regionCode=region_code,
            maxResults=max_results,
            videoCategoryId='0'  # All categories
        )
        response = request.execute()
        
        trending = []
        for item in response['items']:
            trending.append({
                'title': item['snippet']['title'],
                'tags': item['snippet'].get('tags', []),
                'views': item['statistics']['viewCount'],
                'category': item['snippet']['categoryId']
            })
        return trending
    
    def schedule_uploads(self):
        """Set up automated upload schedules"""
        
        # Schedule 2 regular videos per week (Monday & Thursday at 3 PM)
        schedule.every().monday.at("15:00").do(self.upload_weekly_video)
        schedule.every().thursday.at("15:00").do(self.upload_weekly_video)
        
        # Schedule 10 shorts daily (every 2.4 hours starting at 8 AM)
        hours = [8, 10, 12, 14, 16, 18, 20, 22, 0, 2]
        for hour in hours:
            schedule.every().day.at(f"{hour:02d}:00").do(self.upload_daily_short)
        
        print("✅ Upload schedule initialized!")
        print("📹 2 regular videos/week: Monday & Thursday at 3 PM")
        print("🎬 10 shorts/day: Every 2.4 hours")
        
    def upload_weekly_video(self):
        """Upload weekly regular video"""
        if self.video_queue:
            video_data = self.video_queue.pop(0)
            print(f"\n📹 Uploading weekly video: {video_data['title']}")
            self.upload_video(**video_data, is_short=False)
        else:
            print("⚠️ No videos in queue!")
            
    def upload_daily_short(self):
        """Upload daily short"""
        if self.shorts_queue:
            short_data = self.shorts_queue.pop(0)
            print(f"\n🎬 Uploading short: {short_data['title']}")
            self.upload_video(**short_data, is_short=True)
        else:
            print("⚠️ No shorts in queue!")
    
    def add_to_video_queue(self, file_path, title, description, tags, category_id='22'):
        """Add video to upload queue"""
        self.video_queue.append({
            'file_path': file_path,
            'title': title,
            'description': description,
            'tags': tags,
            'category_id': category_id,
            'privacy_status': 'public'
        })
        print(f"✅ Added to video queue: {title}")
        
    def add_to_shorts_queue(self, file_path, title, description, tags):
        """Add short to upload queue"""
        self.shorts_queue.append({
            'file_path': file_path,
            'title': title,
            'description': description,
            'tags': tags,
            'category_id': '22',
            'privacy_status': 'public'
        })
        print(f"✅ Added to shorts queue: {title}")
    
    def run(self):
        """Start the automation agent"""
        print("\n🚀 YouTube Automation Agent Started!")
        print(f"📊 Videos in queue: {len(self.video_queue)}")
        print(f"🎬 Shorts in queue: {len(self.shorts_queue)}")
        
        while True:
            schedule.run_pending()
            time.sleep(60)  # Check every minute

# Example usage
if __name__ == "__main__":
    agent = YouTubeAutomationAgent()
    
    # Get trending topics for content ideas
    trending = agent.get_trending_topics()
    print("\n🔥 Trending Topics:")
    for i, topic in enumerate(trending[:5], 1):
        print(f"{i}. {topic['title']} ({topic['views']} views)")
    
    # Set up schedules
    agent.schedule_uploads()
    
    # Start automation
    agent.run()
