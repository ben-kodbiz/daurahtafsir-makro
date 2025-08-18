#!/usr/bin/env python3
"""
Video ID Extractor for Usul Dirayat Hadis
This script extracts video IDs from various YouTube sources:
- Individual video URLs
- Channel URLs
- Playlist URLs
- Search results
"""

import json
import re
import subprocess
import sys
from typing import List, Tuple, Dict

def extract_video_id_from_url(url: str) -> str:
    """
    Extract video ID from various YouTube URL formats.
    """
    patterns = [
        r'(?:v=|/)([a-zA-Z0-9_-]{11})',
        r'youtu\.be/([a-zA-Z0-9_-]{11})',
        r'embed/([a-zA-Z0-9_-]{11})'
    ]
    
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    
    return None

def get_channel_videos(channel_url: str, max_videos: int = 200) -> List[Tuple[str, str]]:
    """
    Extract videos from a YouTube channel.
    Returns list of (video_id, title) tuples.
    """
    try:
        cmd = [
            'yt-dlp',
            '--flat-playlist',
            '--playlist-end', str(max_videos),
            '--print', '%(id)s|||%(title)s',
            channel_url
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        
        if result.returncode != 0:
            print(f"Error extracting from channel: {result.stderr}")
            return []
        
        videos = []
        for line in result.stdout.strip().split('\n'):
            if '|||' in line:
                video_id, title = line.split('|||', 1)
                videos.append((video_id.strip(), title.strip()))
        
        return videos
        
    except Exception as e:
        print(f"Error processing channel {channel_url}: {e}")
        return []

def search_youtube_videos(query: str, max_results: int = 50) -> List[Tuple[str, str]]:
    """
    Search YouTube for videos matching the query.
    Returns list of (video_id, title) tuples.
    """
    try:
        cmd = [
            'yt-dlp',
            '--flat-playlist',
            '--playlist-end', str(max_results),
            '--print', '%(id)s|||%(title)s',
            f'ytsearch{max_results}:{query}'
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        
        if result.returncode != 0:
            print(f"Error searching YouTube: {result.stderr}")
            return []
        
        videos = []
        for line in result.stdout.strip().split('\n'):
            if '|||' in line:
                video_id, title = line.split('|||', 1)
                videos.append((video_id.strip(), title.strip()))
        
        return videos
        
    except Exception as e:
        print(f"Error searching YouTube: {e}")
        return []

def filter_videos_by_keywords(videos: List[Tuple[str, str]], keywords: List[str]) -> List[Tuple[str, str]]:
    """
    Filter videos by keywords in their titles.
    """
    filtered = []
    keywords_lower = [kw.lower() for kw in keywords]
    
    for video_id, title in videos:
        title_lower = title.lower()
        if any(keyword in title_lower for keyword in keywords_lower):
            filtered.append((video_id, title))
    
    return filtered

def extract_session_number(title: str) -> int:
    """
    Extract session number from video title.
    """
    patterns = [
        r'sesi\s*(\d+)',
        r'session\s*(\d+)',
        r'\b(\d+)\s*[-–]',
        r'\[(\d+)\]',
        r'part\s*(\d+)',
        r'ep\s*(\d+)',
        r'episode\s*(\d+)'
    ]
    
    title_lower = title.lower()
    for pattern in patterns:
        match = re.search(pattern, title_lower)
        if match:
            return int(match.group(1))
    
    return 0

def save_video_list(videos: List[Tuple[str, str]], filename: str) -> None:
    """
    Save video list to a JSON file for manual review and arrangement.
    """
    video_data = []
    for video_id, title in videos:
        session_num = extract_session_number(title)
        video_data.append({
            'video_id': video_id,
            'title': title,
            'detected_session': session_num if session_num > 0 else None,
            'youtube_url': f'https://www.youtube.com/watch?v={video_id}',
            'assigned_session': None  # For manual assignment
        })
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(video_data, f, ensure_ascii=False, indent=2)
    
    print(f"Saved {len(videos)} videos to {filename}")

def load_manual_assignments(filename: str) -> Dict[int, str]:
    """
    Load manually assigned video IDs from JSON file.
    Returns dict with session_number as key and video_id as value.
    """
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        assignments = {}
        for item in data:
            if item.get('assigned_session'):
                session_num = int(item['assigned_session'])
                video_id = item['video_id']
                assignments[session_num] = video_id
        
        return assignments
        
    except Exception as e:
        print(f"Error loading manual assignments: {e}")
        return {}

def apply_manual_assignments(json_file: str, assignments: Dict[int, str]) -> None:
    """
    Apply manually assigned video IDs to the main JSON file.
    """
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        updated_count = 0
        
        for session in data:
            session_num = session['session']
            
            if session_num in assignments:
                video_id = assignments[session_num]
                old_link = session['link']
                session['link'] = f"https://www.youtube.com/watch?v={video_id}"
                
                if 'placeholder' in old_link:
                    updated_count += 1
                    print(f"Updated Session {session_num} with video {video_id}")
        
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"Applied {updated_count} manual assignments to {json_file}")
        
    except Exception as e:
        print(f"Error applying manual assignments: {e}")

def main():
    """
    Main function for video ID extraction.
    """
    print("Video ID Extractor for Usul Dirayat Hadis")
    print("=" * 40)
    
    # Check if yt-dlp is available
    try:
        subprocess.run(['yt-dlp', '--version'], capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("Error: yt-dlp is not installed or not available in PATH")
        print("Please install it with: pip install yt-dlp")
        sys.exit(1)
    
    print("\nChoose extraction method:")
    print("1. Extract from YouTube channel")
    print("2. Extract from playlist")
    print("3. Search YouTube")
    print("4. Apply manual assignments")
    
    choice = input("\nEnter choice (1-4): ").strip()
    
    videos = []
    
    if choice == '1':
        channel_url = input("Enter YouTube channel URL: ").strip()
        max_videos = int(input("Maximum videos to extract (default 200): ") or "200")
        print(f"\nExtracting videos from channel...")
        videos = get_channel_videos(channel_url, max_videos)
        
    elif choice == '2':
        from auto_playlist_organizer import get_playlist_videos
        playlist_url = input("Enter YouTube playlist URL: ").strip()
        print(f"\nExtracting videos from playlist...")
        videos = get_playlist_videos(playlist_url)
        
    elif choice == '3':
        query = input("Enter search query: ").strip()
        max_results = int(input("Maximum results (default 50): ") or "50")
        print(f"\nSearching YouTube...")
        videos = search_youtube_videos(query, max_results)
        
    elif choice == '4':
        assignments_file = input("Enter assignments JSON file path: ").strip()
        assignments = load_manual_assignments(assignments_file)
        if assignments:
            apply_manual_assignments('usul_dirayat_hadis.json', assignments)
        return
    
    else:
        print("Invalid choice")
        return
    
    if not videos:
        print("No videos extracted.")
        return
    
    print(f"\nExtracted {len(videos)} videos")
    
    # Filter by keywords if desired
    filter_choice = input("\nFilter by keywords? (y/n): ").strip().lower()
    if filter_choice == 'y':
        keywords = input("Enter keywords (comma-separated): ").strip().split(',')
        keywords = [kw.strip() for kw in keywords if kw.strip()]
        if keywords:
            videos = filter_videos_by_keywords(videos, keywords)
            print(f"Filtered to {len(videos)} videos")
    
    # Save for manual review
    output_file = f"extracted_videos_{len(videos)}.json"
    save_video_list(videos, output_file)
    
    # Show summary
    print(f"\nSummary:")
    print(f"Total videos: {len(videos)}")
    
    # Count videos with detected session numbers
    with_sessions = sum(1 for _, title in videos if extract_session_number(title) > 0)
    print(f"Videos with detected session numbers: {with_sessions}")
    print(f"Videos needing manual assignment: {len(videos) - with_sessions}")
    
    print(f"\nNext steps:")
    print(f"1. Review {output_file}")
    print(f"2. Manually assign session numbers in 'assigned_session' field")
    print(f"3. Run this script again with option 4 to apply assignments")

if __name__ == "__main__":
    main()