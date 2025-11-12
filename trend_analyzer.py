from googleapiclient.discovery import build
import json

class TrendAnalyzer:
    def __init__(self, youtube_api_key):
        self.api_key = youtube_api_key
        self.youtube = build('youtube', 'v3', developerKey=youtube_api_key)
        
    def analyze_trending_categories(self, region_code='US'):
        """Analyze which categories are trending"""
        categories = {}
        
        request = self.youtube.videos().list(
            part='snippet,statistics',
            chart='mostPopular',
            regionCode=region_code,
            maxResults=50
        )
        response = request.execute()
        
        for video in response['items']:
            cat_id = video['snippet']['categoryId']
            views = int(video['statistics']['viewCount'])
            
            if cat_id not in categories:
                categories[cat_id] = {'count': 0, 'total_views': 0}
            
            categories[cat_id]['count'] += 1
            categories[cat_id]['total_views'] += views
        
        return categories
    
    def get_keyword_suggestions(self, topic, max_results=20):
        """Get keyword suggestions for SEO optimization"""
        request = self.youtube.search().list(
            part='snippet',
            q=topic,
            type='video',
            maxResults=max_results,
            order='viewCount'
        )
        response = request.execute()
        
        keywords = set()
        for item in response['items']:
            title = item['snippet']['title']
            tags = item['snippet'].get('tags', [])
            keywords.update(tags)
        
        return list(keywords)
    
    def get_related_videos(self, video_id, max_results=10):
        """Get videos related to a specific video for content ideas"""
        request = self.youtube.search().list(
            part='snippet',
            relatedToVideoId=video_id,
            type='video',
            maxResults=max_results
        )
        response = request.execute()
        
        related = []
        for item in response['items']:
            related.append({
                'title': item['snippet']['title'],
                'video_id': item['id']['videoId'],
                'thumbnail': item['snippet']['thumbnails']['default']['url']
            })
        
        return related
    
    def search_by_hashtag(self, hashtag, max_results=15):
        """Search for videos by hashtag to find trending content"""
        request = self.youtube.search().list(
            part='snippet',
            q=hashtag,
            type='video',
            maxResults=max_results,
            order='relevance'
        )
        response = request.execute()
        
        results = []
        for item in response['items']:
            results.append({
                'title': item['snippet']['title'],
                'description': item['snippet']['description'],
                'channel': item['snippet']['channelTitle'],
                'video_id': item['id']['videoId']
            })
        
        return results
