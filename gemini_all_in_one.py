#!/usr/bin/env python3
"""
🚀 GEMINI-ONLY VIRAL VIDEO AGENT - ALMOST FREE!
Generates viral YouTube/TikTok videos using ONLY Gemini + free tools
Cost: $3-10/month (vs $50-110 with Pictory)
"""

import os
import json
import requests
import subprocess
from datetime import datetime
from pathlib import Path
import google.generativeai as genai
from google.cloud import texttospeech
import logging

# Import our existing viral trend detector
from viral_trend_detector import ViralTrendDetector
from config import GEMINI_API_KEY, YOUTUBE_CLIENT_ID, YOUTUBE_CLIENT_SECRET

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GeminiViralAgent:
    """
    All-in-one viral video agent using Gemini AI
    Handles: trend detection, script writing, video creation, and uploading
    """
    
    def __init__(self):
        # Configure Gemini
        genai.configure(api_key=GEMINI_API_KEY)
        self.model = genai.GenerativeModel('gemini-1.5-pro')
        
        # Initialize trend detector
        self.trend_detector = ViralTrendDetector()
        
        # Pexels API for free stock footage
        self.pexels_api_key = os.getenv('PEXELS_API_KEY', 'YOUR_FREE_PEXELS_KEY')
        
        # Setup directories
        self.output_dir = Path('generated_videos')
        self.output_dir.mkdir(exist_ok=True)
        
    def detect_trending_topic(self):
        """
        Step 1: Find viral trending topic
        """
        logger.info("🔍 Detecting trending topics...")
        trends = self.trend_detector.get_all_trends()
        
        if not trends:
            logger.error("No trends found!")
            return None
            
        # Get the top viral trend
        top_trend = trends[0]
        logger.info(f"✅ Found viral topic: {top_trend['topic']} (Score: {top_trend['viral_score']})")
        return top_trend
    
    def generate_viral_script(self, trend):
        """
        Step 2: Use Gemini to create viral video script
        """
        logger.info("📝 Generating viral script with Gemini...")
        
        prompt = f"""
        Create an ENGAGING, VIRAL video script about: {trend['topic']}
        
        Requirements:
        - Duration: 60 seconds for YouTube Shorts/TikTok
        - Hook viewers in first 3 seconds
        - Include trending keywords: {', '.join(trend.get('keywords', []))}
        - Make it shareable and emotional
        - End with strong call-to-action
        
        Format your response as JSON:
        {{
            "title": "Catchy video title with emoji",
            "script": "Full narration script",
            "scenes": [
                {{"duration": 5, "description": "Scene description", "search_query": "Stock footage search term"}},
                ...
            ],
            "hashtags": ["#trending", "#viral", ...]
        }}
        """
        
        response = self.model.generate_content(prompt)
        script_data = json.loads(response.text)
        
        logger.info(f"✅ Script generated: {script_data['title']}")
        return script_data
    
    def download_stock_footage(self, query, duration=5):
        """
        Step 3a: Get FREE stock footage from Pexels
        """
        logger.info(f"🎥 Searching stock footage: {query}")
        
        headers = {'Authorization': self.pexels_api_key}
        url = f"https://api.pexels.com/videos/search?query={query}&per_page=1"
        
        response = requests.get(url, headers=headers)
        data = response.json()
        
        if data.get('videos'):
            video_url = data['videos'][0]['video_files'][0]['link']
            
            # Download video
            filename = f"scene_{query.replace(' ', '_')}.mp4"
            filepath = self.output_dir / filename
            
            video_data = requests.get(video_url).content
            with open(filepath, 'wb') as f:
                f.write(video_data)
            
            logger.info(f"✅ Downloaded: {filename}")
            return filepath
        
        logger.warning(f"⚠️ No footage found for: {query}")
        return None
    
    def generate_voiceover(self, script_text):
        """
        Step 3b: Generate FREE voiceover with Google Text-to-Speech
        """
        logger.info("🎤 Generating voiceover...")
        
        # Using gTTS (free, no API key needed)
        from gtts import gTTS
        
        output_file = self.output_dir / "voiceover.mp3"
        tts = gTTS(text=script_text, lang='en', slow=False)
        tts.save(str(output_file))
        
        logger.info("✅ Voiceover generated")
        return output_file
    
    def compile_video(self, scenes, voiceover_path, title):
        """
        Step 4: Compile video using FREE FFmpeg
        """
        logger.info("🎬 Compiling final video with FFmpeg...")
        
        # Create concat file for FFmpeg
        concat_file = self.output_dir / "concat.txt"
        with open(concat_file, 'w') as f:
            for scene_path in scenes:
                if scene_path:
                    f.write(f"file '{scene_path}'\n")
        
        # Final output filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_filename = f"viral_video_{timestamp}.mp4"
        output_path = self.output_dir / output_filename
        
        # FFmpeg command to merge videos and add voiceover
        cmd = [
            'ffmpeg',
            '-f', 'concat',
            '-safe', '0',
            '-i', str(concat_file),
            '-i', str(voiceover_path),
            '-c:v', 'libx264',
            '-c:a', 'aac',
            '-shortest',
            str(output_path)
        ]
        
        subprocess.run(cmd, check=True)
        logger.info(f"✅ Video compiled: {output_filename}")
        
        return output_path, output_filename
    
    def upload_to_youtube(self, video_path, title, description, tags):
        """
        Step 5a: Upload to YouTube Shorts
        """
        logger.info("📤 Uploading to YouTube...")
        
        # Using google-api-python-client (already in dependencies)
        from googleapiclient.discovery import build
        from googleapiclient.http import MediaFileUpload
        from google.oauth2.credentials import Credentials
        
        # Note: OAuth flow needed for first-time setup
        # This will use stored credentials after first auth
        
        youtube = build('youtube', 'v3', credentials=self._get_youtube_credentials())
        
        body = {
            'snippet': {
                'title': title,
                'description': description,
                'tags': tags,
                'categoryId': '22'  # People & Blogs
            },
            'status': {
                'privacyStatus': 'public',
                'selfDeclaredMadeForKids': False
            }
        }
        
        media = MediaFileUpload(video_path, resumable=True)
        request = youtube.videos().insert(
            part='snippet,status',
            body=body,
            media_body=media
        )
        
        response = request.execute()
        video_id = response['id']
        
        logger.info(f"✅ YouTube upload complete: https://youtube.com/shorts/{video_id}")
        return video_id
    
    def upload_to_tiktok(self, video_path, title, hashtags):
        """
        Step 5b: Upload to TikTok
        """
        logger.info("📤 Uploading to TikTok...")
        
        # Using TikTok Content Posting API
        # Note: Requires TikTok developer account (free)
        
        from tiktok_uploader import upload_video
        
        result = upload_video(
            video_path=video_path,
            title=title,
            hashtags=hashtags
        )
        
        logger.info(f"✅ TikTok upload complete: {result['share_url']}")
        return result
    
    def _get_youtube_credentials(self):
        """
        Helper: Get YouTube OAuth credentials
        """
        # Simplified credential management
        # In production, implement full OAuth2 flow
        from google.oauth2.credentials import Credentials
        
        creds_path = Path('youtube_credentials.json')
        if creds_path.exists():
            with open(creds_path) as f:
                creds_data = json.load(f)
            return Credentials.from_authorized_user_info(creds_data)
        
        raise Exception("YouTube credentials not found. Run setup_youtube_auth.py first")
    
    def create_and_publish_viral_video(self):
        """
        🎯 MAIN FUNCTION: Complete automated video creation pipeline
        """
        logger.info("\n🚀 Starting viral video creation...\n")
        
        try:
            # Step 1: Detect trending topic
            trend = self.detect_trending_topic()
            if not trend:
                return False
            
            # Step 2: Generate viral script with Gemini
            script_data = self.generate_viral_script(trend)
            
            # Step 3: Download stock footage for each scene
            scene_paths = []
            for scene in script_data['scenes']:
                scene_path = self.download_stock_footage(
                    scene['search_query'],
                    scene['duration']
                )
                if scene_path:
                    scene_paths.append(scene_path)
            
            # Step 4: Generate voiceover
            voiceover_path = self.generate_voiceover(script_data['script'])
            
            # Step 5: Compile final video
            video_path, video_filename = self.compile_video(
                scene_paths,
                voiceover_path,
                script_data['title']
            )
            
            # Step 6: Upload to YouTube
            description = f"{script_data['script'][:200]}...\n\n{' '.join(script_data['hashtags'])}"
            youtube_id = self.upload_to_youtube(
                video_path,
                script_data['title'],
                description,
                script_data['hashtags']
            )
            
            # Step 7: Upload to TikTok
            tiktok_result = self.upload_to_tiktok(
                video_path,
                script_data['title'],
                script_data['hashtags']
            )
            
            logger.info("\n🎉 SUCCESS! Viral video published!\n")
            logger.info(f"📺 YouTube: https://youtube.com/shorts/{youtube_id}")
            logger.info(f"📱 TikTok: {tiktok_result['share_url']}")
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Error: {str(e)}")
            return False

if __name__ == "__main__":
    agent = GeminiViralAgent()
    agent.create_and_publish_viral_video()
