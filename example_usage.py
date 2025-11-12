#!/usr/bin/env python3
"""Example usage of YouTube Automation Agent"""

from youtube_agent import YouTubeAutomationAgent
from trend_analyzer import TrendAnalyzer
from config import YOUTUBE_API_KEY
import os

def main():
    print("\n=== YouTube Automation Agent - Example Usage ===")
    
    # Initialize the agent
    print("\nInitializing YouTube Automation Agent...")
    agent = YouTubeAutomationAgent()
    print("✅ Agent initialized successfully!")
    
    # Get trending topics
    print("\n📊 Fetching trending topics...")
    trending = agent.get_trending_topics(region_code='US', max_results=5)
    print("\n🔥 Top Trending Videos:")
    for i, topic in enumerate(trending, 1):
        print(f"   {i}. {topic['title']} ({topic['views']} views)")
    
    # Add videos to queue
    print("\n📹 Adding videos to queue...")
    if os.path.exists('videos/sample_video.mp4'):
        agent.add_to_video_queue(
            file_path='videos/sample_video.mp4',
            title='Amazing Content - Trending Now',
            description='Check out this viral content!',
            tags=['trending', 'viral', 'youtube']
        )
    else:
        print("   ⚠️ Sample video not found. Skipping video queue example.")
    
    # Add shorts to queue
    print("\n🎬 Adding shorts to queue...")
    if os.path.exists('shorts/sample_short.mp4'):
        agent.add_to_shorts_queue(
            file_path='shorts/sample_short.mp4',
            title='Quick Tip #1',
            description='Learn this trick in 30 seconds!',
            tags=['shorts', 'tips', 'tutorial']
        )
    else:
        print("   ⚠️ Sample short not found. Skipping shorts queue example.")
    
    # Setup automated schedules
    print("\n⏱️ Setting up automated upload schedules...")
    agent.schedule_uploads()
    
    # Use trend analyzer
    print("\n🔍 Using Trend Analyzer...")
    analyzer = TrendAnalyzer(YOUTUBE_API_KEY)
    keywords = analyzer.get_keyword_suggestions('AI technology', max_results=5)
    print(f"\n📝 Trending keywords for 'AI technology': {', '.join(keywords[:5])}")
    
    # Show queue status
    print(f"\n📊 Current Queue Status:")
    print(f"   Videos ready: {len(agent.video_queue)}")
    print(f"   Shorts ready: {len(agent.shorts_queue)}")
    
    print("\n" + "="*50)
    print("To start the automation, call: agent.run()")
    print("This will upload videos and shorts on the schedule.")
    print("="*50 + "\n")

if __name__ == '__main__':
    main()
