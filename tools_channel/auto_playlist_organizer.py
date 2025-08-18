#!/usr/bin/env python3
"""
Automatic Playlist Organizer for Usul Dirayat Hadis
This script automatically groups videos into playlists by session numbers
and extracts video IDs for correct placement in sessions.
"""

import json
import re
import subprocess
import sys
from collections import defaultdict
from typing import Dict, List, Tuple

def extract_session_number(title: str) -> int:
    """
    Extract session number from video title.
    Handles various formats like 'Sesi 1', 'Session 1', etc.
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
    
    return 0  # Return 0 if no session number found

def get_video_info_from_url(url: str) -> Tuple[str, str]:
    """
    Extract video ID and title from YouTube URL using yt-dlp.
    Returns (video_id, title)
    """
    try:
        # Extract video ID from URL
        video_id_match = re.search(r'(?:v=|/)([a-zA-Z0-9_-]{11})', url)
        if not video_id_match:
            return None, None
        
        video_id = video_id_match.group(1)
        
        # Get video title using yt-dlp
        cmd = ['yt-dlp', '--get-title', f'https://www.youtube.com/watch?v={video_id}']
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            title = result.stdout.strip()
            return video_id, title
        else:
            print(f"Warning: Could not get title for {video_id}: {result.stderr}")
            return video_id, f"Video {video_id}"
            
    except Exception as e:
        print(f"Error processing URL {url}: {e}")
        return None, None

def get_playlist_videos(playlist_url: str) -> List[Tuple[str, str]]:
    """
    Extract all video IDs and titles from a YouTube playlist.
    Returns list of (video_id, title) tuples.
    """
    try:
        cmd = [
            'yt-dlp',
            '--flat-playlist',
            '--print', '%(id)s|||%(title)s',
            playlist_url
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        
        if result.returncode != 0:
            print(f"Error extracting playlist: {result.stderr}")
            return []
        
        videos = []
        for line in result.stdout.strip().split('\n'):
            if '|||' in line:
                video_id, title = line.split('|||', 1)
                videos.append((video_id.strip(), title.strip()))
        
        return videos
        
    except Exception as e:
        print(f"Error processing playlist {playlist_url}: {e}")
        return []

def organize_videos_by_session(videos: List[Tuple[str, str]]) -> Dict[int, List[Tuple[str, str]]]:
    """
    Organize videos by session number based on their titles.
    Returns dictionary with session_number as key and list of (video_id, title) as value.
    """
    session_groups = defaultdict(list)
    unmatched_videos = []
    
    for video_id, title in videos:
        session_num = extract_session_number(title)
        if session_num > 0 and session_num <= 120:
            session_groups[session_num].append((video_id, title))
        else:
            unmatched_videos.append((video_id, title))
    
    # Print summary
    print(f"\nOrganization Summary:")
    print(f"Total videos processed: {len(videos)}")
    print(f"Videos organized into sessions: {sum(len(v) for v in session_groups.values())}")
    print(f"Unmatched videos: {len(unmatched_videos)}")
    print(f"Sessions with videos: {len(session_groups)}")
    
    if unmatched_videos:
        print(f"\nUnmatched videos:")
        for video_id, title in unmatched_videos[:10]:  # Show first 10
            print(f"  - {video_id}: {title}")
        if len(unmatched_videos) > 10:
            print(f"  ... and {len(unmatched_videos) - 10} more")
    
    return dict(session_groups)

def update_json_with_organized_videos(json_file: str, session_groups: Dict[int, List[Tuple[str, str]]]) -> None:
    """
    Update the JSON file with organized video IDs and titles.
    """
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        updated_count = 0
        
        for session in data:
            session_num = session['session']
            
            if session_num in session_groups:
                videos_for_session = session_groups[session_num]
                
                if videos_for_session:
                    # Use the first video if multiple videos for same session
                    video_id, title = videos_for_session[0]
                    
                    # Update the session
                    old_link = session['link']
                    session['link'] = f"https://www.youtube.com/watch?v={video_id}"
                    session['title'] = f"Sesi {session_num} – {title.replace(f'Sesi {session_num}', '').replace('–', '').strip()}"
                    
                    if 'placeholder' in old_link:
                        updated_count += 1
                        print(f"Updated Session {session_num}: {title}")
                    
                    # If multiple videos for same session, report it
                    if len(videos_for_session) > 1:
                        print(f"Warning: Multiple videos found for Session {session_num}:")
                        for vid_id, vid_title in videos_for_session:
                            print(f"  - {vid_id}: {vid_title}")
                        print(f"  Using first one: {video_id}")
        
        # Save updated JSON
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"\nUpdated {updated_count} sessions in {json_file}")
        
    except Exception as e:
        print(f"Error updating JSON file: {e}")

def main():
    """
    Main function to orchestrate the automatic playlist organization.
    """
    print("Automatic Playlist Organizer for Usul Dirayat Hadis")
    print("=" * 50)
    
    # Check if yt-dlp is available
    try:
        subprocess.run(['yt-dlp', '--version'], capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("Error: yt-dlp is not installed or not available in PATH")
        print("Please install it with: pip install yt-dlp")
        sys.exit(1)
    
    # Get playlist URLs from user
    playlist_urls = []
    print("\nEnter YouTube playlist URLs (one per line, empty line to finish):")
    
    while True:
        url = input("Playlist URL: ").strip()
        if not url:
            break
        if 'playlist' in url or 'list=' in url:
            playlist_urls.append(url)
        else:
            print("Warning: This doesn't look like a playlist URL. Added anyway.")
            playlist_urls.append(url)
    
    if not playlist_urls:
        print("No playlist URLs provided. Exiting.")
        sys.exit(1)
    
    # Extract videos from all playlists
    all_videos = []
    for i, playlist_url in enumerate(playlist_urls, 1):
        print(f"\nProcessing playlist {i}/{len(playlist_urls)}...")
        videos = get_playlist_videos(playlist_url)
        all_videos.extend(videos)
        print(f"Extracted {len(videos)} videos from playlist {i}")
    
    if not all_videos:
        print("No videos extracted from playlists. Exiting.")
        sys.exit(1)
    
    print(f"\nTotal videos extracted: {len(all_videos)}")
    
    # Organize videos by session
    print("\nOrganizing videos by session numbers...")
    session_groups = organize_videos_by_session(all_videos)
    
    # Update JSON file
    json_file = 'usul_dirayat_hadis.json'
    print(f"\nUpdating {json_file}...")
    update_json_with_organized_videos(json_file, session_groups)
    
    # Generate report
    print("\n" + "=" * 50)
    print("ORGANIZATION REPORT")
    print("=" * 50)
    
    sessions_with_videos = sorted(session_groups.keys())
    print(f"Sessions with videos found: {sessions_with_videos}")
    
    missing_sessions = []
    for i in range(1, 121):
        if i not in session_groups:
            missing_sessions.append(i)
    
    if missing_sessions:
        print(f"\nSessions still missing videos: {missing_sessions[:20]}")
        if len(missing_sessions) > 20:
            print(f"... and {len(missing_sessions) - 20} more")
    
    print(f"\nTotal sessions filled: {len(sessions_with_videos)}/120")
    print(f"Completion rate: {len(sessions_with_videos)/120*100:.1f}%")
    
    print("\nDone! Check the updated usul_dirayat_hadis.json file.")

if __name__ == "__main__":
    main()