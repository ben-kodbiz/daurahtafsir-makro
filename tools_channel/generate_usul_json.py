#!/usr/bin/env python3

import json
import os
import re
from pathlib import Path

def extract_title_from_html(session_number):
    """Extract title from HTML file"""
    html_file = f"sesi_{session_number}.html"
    if os.path.exists(html_file):
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()
            # Extract title from the h1 tag
            title_match = re.search(r'<h1 class="surah-title">(.*?)</h1>', content)
            if title_match:
                return title_match.group(1)
    return f"Sesi {session_number} – Usul Dirayat Hadis"

def get_video_id_from_html(session_number):
    """Extract video ID from HTML file"""
    html_file = f"sesi_{session_number}.html"
    if os.path.exists(html_file):
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()
            # Extract video ID from iframe src
            video_match = re.search(r'youtube\.com/embed/([a-zA-Z0-9_-]+)', content)
            if video_match:
                return video_match.group(1)
    return "placeholder_video_id"

def generate_usul_json():
    """Generate the usul_dirayat_hadis.json file"""
    sessions = []
    
    # Generate sessions 1-120
    for i in range(1, 121):
        title = extract_title_from_html(i)
        video_id = get_video_id_from_html(i)
        
        session = {
            "session_number": i,
            "title": title,
            "video_id": video_id,
            "youtube_url": f"https://www.youtube.com/watch?v={video_id}"
        }
        sessions.append(session)
    
    # Create the final JSON structure
    usul_data = {
        "title": "Usul Dirayat Hadis",
        "description": "Comprehensive course on the principles of hadith criticism and authentication",
        "total_sessions": 120,
        "sessions": sessions
    }
    
    # Save to data directory
    data_dir = "../data"
    os.makedirs(data_dir, exist_ok=True)
    
    output_file = os.path.join(data_dir, "usul_dirayat_hadis.json")
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(usul_data, f, indent=2, ensure_ascii=False)
    
    print(f"Generated {output_file} with {len(sessions)} sessions")
    
    # Also create a backup in current directory
    with open("usul_dirayat_hadis.json", 'w', encoding='utf-8') as f:
        json.dump(usul_data, f, indent=2, ensure_ascii=False)
    
    print("Backup created in current directory")
    
    return usul_data

if __name__ == "__main__":
    data = generate_usul_json()
    print(f"\nGenerated JSON with {data['total_sessions']} sessions")
    print(f"First session: {data['sessions'][0]['title']}")
    print(f"Last session: {data['sessions'][-1]['title']}")