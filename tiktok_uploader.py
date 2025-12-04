#!/usr/bin/env python3
"""
📱 TikTok Uploader - FREE uploads using TikTok Content Posting API
No browser automation needed - official API
"""

import os
import json
import requests
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

class TikTokUploader:
    """
    Uploads videos to TikTok using official Content Posting API
    Requires TikTok developer account (free): https://developers.tiktok.com/
    """
    
    def __init__(self, access_token=None):
        self.access_token = access_token or os.getenv('TIKTOK_ACCESS_TOKEN')
        self.base_url = "https://open.tiktokapis.com/v2/"
        
        if not self.access_token:
            raise ValueError("TikTok access token required. Get one from https://developers.tiktok.com/")
    
    def upload_video(self, video_path, title, hashtags, privacy="PUBLIC_TO_EVERYONE"):
        """
        Upload video to TikTok
        
        Args:
            video_path: Path to video file (must be mp4, max 60s for most accounts)
            title: Video title/caption
            hashtags: List of hashtags
            privacy: "PUBLIC_TO_EVERYONE", "MUTUAL_FOLLOW_FRIENDS", or "SELF_ONLY"
        
        Returns:
            dict with share_url and video_id
        """
        logger.info(f"📤 Uploading to TikTok: {title}")
        
        # Step 1: Initialize upload
        init_response = self._initialize_upload()
        upload_url = init_response['data']['upload_url']
        
        # Step 2: Upload video file
        self._upload_file(upload_url, video_path)
        
        # Step 3: Publish video
        caption = f"{title}\n\n{' '.join(hashtags)}"
        publish_response = self._publish_video(
            upload_url=upload_url,
            caption=caption,
            privacy=privacy
        )
        
        result = {
            'share_url': publish_response['data']['share_url'],
            'video_id': publish_response['data']['publish_id']
        }
        
        logger.info(f"✅ TikTok upload successful: {result['share_url']}")
        return result
    
    def _initialize_upload(self):
        """
        Step 1: Initialize the upload and get upload URL
        """
        url = f"{self.base_url}post/publish/video/init/"
        headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json'
        }
        
        data = {
            'post_info': {
                'title': 'Upload',
                'privacy_level': 'PUBLIC_TO_EVERYONE',
                'disable_duet': False,
                'disable_comment': False,
                'disable_stitch': False,
                'video_cover_timestamp_ms': 1000
            },
            'source_info': {
                'source': 'FILE_UPLOAD',
                'video_size': 0,
                'chunk_size': 10000000,
                'total_chunk_count': 1
            }
        }
        
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        return response.json()
    
    def _upload_file(self, upload_url, video_path):
        """
        Step 2: Upload the actual video file
        """
        with open(video_path, 'rb') as video_file:
            video_data = video_file.read()
        
        headers = {
            'Content-Type': 'video/mp4',
            'Content-Length': str(len(video_data))
        }
        
        response = requests.put(upload_url, headers=headers, data=video_data)
        response.raise_for_status()
        return response
    
    def _publish_video(self, upload_url, caption, privacy):
        """
        Step 3: Publish the uploaded video
        """
        url = f"{self.base_url}post/publish/status/fetch/"
        headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json'
        }
        
        data = {
            'publish_id': upload_url.split('/')[-1]
        }
        
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        return response.json()


def upload_video(video_path, title, hashtags):
    """
    Simple wrapper function for easy imports
    
    Usage:
        from tiktok_uploader import upload_video
        result = upload_video('video.mp4', 'My Video', ['#viral', '#trending'])
    """
    uploader = TikTokUploader()
    return uploader.upload_video(video_path, title, hashtags)


if __name__ == "__main__":
    # Test upload
    result = upload_video(
        video_path="test_video.mp4",
        title="Test upload from automation agent",
        hashtags=["#test", "#automation"]
    )
    print(f"Success! Video URL: {result['share_url']}")
