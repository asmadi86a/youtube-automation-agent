# Viral Trend Detector
# Detects trending topics from YouTube and TikTok daily

import requests
import json
from datetime import datetime
from config import YOUTUBE_API_KEY, YOUTUBE_TRENDING_REGION, TIKTOK_TRENDING_REGION


class ViralTrendDetector:
    def __init__(self):
        self.youtube_api_key = YOUTUBE_API_KEY
        self.youtube_region = YOUTUBE_TRENDING_REGION
        self.tiktok_region = TIKTOK_TRENDING_REGION
        self.trending_data = []
    
    def get_youtube_trending(self, max_results=50):
        """Fetch trending videos from YouTube"""
        url = "https://www.googleapis.com/youtube/v3/videos"
        params = {
            'part': 'snippet,statistics,contentDetails',
            'chart': 'mostPopular',
            'regionCode': self.youtube_region,
            'maxResults': max_results,
            'key': self.youtube_api_key
        }
        
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            
            trending_videos = []
            for item in data.get('items', []):
                video = {
                    'platform': 'youtube',
                    'title': item['snippet']['title'],
                    'description': item['snippet']['description'],
                    'tags': item['snippet'].get('tags', []),
                    'category_id': item['snippet']['categoryId'],
                    'views': int(item['statistics'].get('viewCount', 0)),
                    'likes': int(item['statistics'].get('likeCount', 0)),
                    'comments': int(item['statistics'].get('commentCount', 0)),
                    'video_id': item['id'],
                    'published_at': item['snippet']['publishedAt'],
                    'trending_score': self._calculate_trending_score(item['statistics'])
                }
                trending_videos.append(video)
            
            # Sort by trending score
            trending_videos.sort(key=lambda x: x['trending_score'], reverse=True)
            print(f"✅ Found {len(trending_videos)} trending YouTube videos")
            return trending_videos
            
        except Exception as e:
            print(f"❌ Error fetching YouTube trends: {e}")
            return []
    
    def get_tiktok_trending_hashtags(self, limit=50):
        """Fetch trending hashtags from TikTok
        Note: Uses RapidAPI or similar service for TikTok trends
        You'll need to sign up for a TikTok trending API service
        """
        # Example using a TikTok trending hashtag API
        # Replace with your actual TikTok API endpoint and key
        
        # Placeholder implementation - you'll need to use actual TikTok API
        trending_hashtags = [
            {'hashtag': '#fyp', 'views': 7700000000, 'posts': 5000000},
            {'hashtag': '#viral', 'views': 3200000000, 'posts': 2000000},
            {'hashtag': '#trending', 'views': 2100000000, 'posts': 1500000},
            {'hashtag': '#foryou', 'views': 5100000000, 'posts': 3000000},
        ]
        
        print(f"✅ Found {len(trending_hashtags)} trending TikTok hashtags")
        return trending_hashtags
    
    def _calculate_trending_score(self, stats):
        """Calculate viral potential score based on engagement"""
        views = int(stats.get('viewCount', 0))
        likes = int(stats.get('likeCount', 0))
        comments = int(stats.get('commentCount', 0))
        
        # Weighted score: views + (likes * 10) + (comments * 20)
        score = views + (likes * 10) + (comments * 20)
        return score
    
    def analyze_trending_topics(self, youtube_data):
        """Extract and rank trending topics from video data"""
        topic_scores = {}
        
        for video in youtube_data:
            # Extract keywords from title
            title_words = video['title'].lower().split()
            
            # Score topics based on video engagement
            score = video['trending_score']
            
            for word in title_words:
                if len(word) > 3:  # Skip short words
                    topic_scores[word] = topic_scores.get(word, 0) + score
            
            # Add tags as topics
            for tag in video['tags']:
                topic_scores[tag.lower()] = topic_scores.get(tag.lower(), 0) + score
        
        # Sort topics by score
        ranked_topics = sorted(topic_scores.items(), key=lambda x: x[1], reverse=True)
        return ranked_topics[:20]  # Top 20 trending topics
    
    def get_daily_trends(self):
        """Get complete trending data for the day"""
        print("\n🔥 Fetching Daily Trending Data...")
        
        # Get YouTube trends
        youtube_trends = self.get_youtube_trending(max_results=50)
        
        # Get TikTok trends
        tiktok_trends = self.get_tiktok_trending_hashtags()
        
        # Analyze topics
        trending_topics = self.analyze_trending_topics(youtube_trends)
        
        daily_report = {
            'date': datetime.now().strftime('%Y-%m-%d'),
            'youtube_videos': youtube_trends[:10],  # Top 10
            'tiktok_hashtags': tiktok_trends[:10],  # Top 10
            'trending_topics': trending_topics[:10],  # Top 10
        }
        
        print(f"\n📊 Top 5 Trending Topics:")
        for i, (topic, score) in enumerate(trending_topics[:5], 1):
            print(f"{i}. {topic} (Score: {score:,.0f})")
        
        return daily_report
    
    def save_trends_to_file(self, daily_report):
        """Save daily trends to JSON file"""
        filename = f"trends_{daily_report['date']}.json"
        with open(filename, 'w') as f:
            json.dump(daily_report, f, indent=2)
        print(f"\n💾 Trends saved to {filename}")


# Example usage
if __name__ == "__main__":
    detector = ViralTrendDetector()
    daily_trends = detector.get_daily_trends()
    detector.save_trends_to_file(daily_trends)
