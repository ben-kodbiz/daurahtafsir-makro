#!/usr/bin/env python3
"""
Script to update video titles in usul_dirayat_hadis.json with actual YouTube video titles
while preserving the session numbers.
"""

import json
import requests
import time
import re
from urllib.parse import urlparse, parse_qs

def get_youtube_title(video_id):
    """
    Get YouTube video title using oembed API (no API key required)
    """
    try:
        url = f"https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v={video_id}&format=json"
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            return data.get('title', '')
    except Exception as e:
        print(f"Error fetching title for video {video_id}: {e}")
    return None

def clean_title(title, session_number):
    """
    Clean the title and ensure it starts with the session number
    """
    if not title:
        return f"Sesi {session_number} – Usul Dirayat Hadis"
    
    # Remove common prefixes that might interfere
    title = re.sub(r'^(Sesi|Session)\s*\d+\s*[-–]?\s*', '', title, flags=re.IGNORECASE)
    title = title.strip()
    
    # Ensure it starts with the correct session number
    return f"Sesi {session_number} – {title}"

def update_video_titles():
    """
    Update video titles in the JSON file
    """
    json_file = 'usul_dirayat_hadis.json'
    
    # Load the JSON file
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"Error: {json_file} not found")
        return
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON in {json_file}")
        return
    
    print(f"Updating titles for {len(data['sessions'])} sessions...")
    
    updated_count = 0
    for i, session in enumerate(data['sessions']):
        session_number = session['session_number']
        video_id = session['video_id']
        current_title = session['title']
        
        # Skip if title is already descriptive (not just "Sesi X – Usul Dirayat Hadis")
        if current_title != f"Sesi {session_number} – Usul Dirayat Hadis":
            print(f"Session {session_number}: Already has descriptive title, skipping")
            continue
        
        print(f"Fetching title for Session {session_number} (Video ID: {video_id})...")
        
        # Get the actual video title
        youtube_title = get_youtube_title(video_id)
        
        if youtube_title:
            # Clean and format the title
            new_title = clean_title(youtube_title, session_number)
            session['title'] = new_title
            updated_count += 1
            print(f"  Updated: {new_title}")
        else:
            print(f"  Failed to fetch title for session {session_number}")
        
        # Add delay to avoid rate limiting
        time.sleep(0.5)
    
    # Save the updated JSON
    try:
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"\nSuccessfully updated {updated_count} video titles in {json_file}")
    except Exception as e:
        print(f"Error saving file: {e}")

if __name__ == "__main__":
    update_video_titles()