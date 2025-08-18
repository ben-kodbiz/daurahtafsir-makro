#!/usr/bin/env python3
"""
Script to update generic "Usul Dirayat Hadis" titles with actual YouTube video titles
for sessions that have real video IDs.
"""

import json
import subprocess
import re
from pathlib import Path

def get_video_title(video_id):
    """
    Extract video title from YouTube using yt-dlp
    """
    try:
        cmd = ['yt-dlp', '--get-title', f'https://www.youtube.com/watch?v={video_id}']
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        if result.returncode == 0:
            return result.stdout.strip()
        else:
            print(f"Error getting title for {video_id}: {result.stderr}")
            return None
    except Exception as e:
        print(f"Exception getting title for {video_id}: {e}")
        return None

def extract_video_id_from_url(youtube_url):
    """
    Extract video ID from YouTube URL
    """
    if youtube_url.startswith('placeholder'):
        return None
    
    # Extract video ID from various YouTube URL formats
    patterns = [
        r'(?:youtube\.com/watch\?v=|youtu\.be/)([a-zA-Z0-9_-]{11})',
        r'youtube\.com/embed/([a-zA-Z0-9_-]{11})'
    ]
    
    for pattern in patterns:
        match = re.search(pattern, youtube_url)
        if match:
            return match.group(1)
    
    return None

def create_specific_title(session_number, youtube_title):
    """
    Create a specific title based on the YouTube video title
    """
    if not youtube_title:
        return f"Sesi {session_number} – Usul Dirayat Hadis"
    
    # Clean up the title and extract meaningful content
    title = youtube_title.strip()
    
    # Remove common prefixes/suffixes
    title = re.sub(r'^\d+\s*[-–]?\s*', '', title)  # Remove leading numbers
    title = re.sub(r'\s*[-–]\s*Usul Dirayat Hadis.*$', '', title, flags=re.IGNORECASE)
    title = re.sub(r'\s*[-–]\s*Usul Dirayah.*$', '', title, flags=re.IGNORECASE)
    title = re.sub(r'\s*Usul Dirayat Hadis\s*[-–]?\s*', '', title, flags=re.IGNORECASE)
    title = re.sub(r'\s*Usul Dirayah\s*[-–]?\s*', '', title, flags=re.IGNORECASE)
    
    # Clean up extra whitespace and dashes
    title = re.sub(r'\s+', ' ', title).strip()
    title = re.sub(r'^[-–]\s*', '', title)
    title = re.sub(r'\s*[-–]$', '', title)
    
    # If title is empty or too generic, use a default
    if not title or len(title) < 3 or title.lower() in ['hadis', 'hadith', 'usul']:
        return f"Sesi {session_number} – Usul Dirayat Hadis"
    
    # Capitalize first letter
    title = title[0].upper() + title[1:] if title else ''
    
    return f"Sesi {session_number} – {title}"

def update_titles():
    """
    Main function to update titles in the JSON file
    """
    json_file = Path('/data/work/dev/daurahtafsir-makro/data/usul_dirayat_hadis.json')
    
    # Load the JSON data
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    updated_count = 0
    total_sessions = len(data['sessions'])
    
    print(f"Processing {total_sessions} sessions...")
    
    for i, session in enumerate(data['sessions']):
        session_num = session['session_number']
        current_title = session['title']
        youtube_url = session['youtube_link']
        
        # Skip if title is already specific (not generic)
        if not current_title.endswith('– Usul Dirayat Hadis'):
            continue
            
        # Skip placeholder videos
        if youtube_url.startswith('placeholder'):
            continue
            
        print(f"Processing Session {session_num}... ", end='')
        
        # Extract video ID
        video_id = extract_video_id_from_url(youtube_url)
        if not video_id:
            print("No valid video ID found")
            continue
            
        # Get video title from YouTube
        youtube_title = get_video_title(video_id)
        if not youtube_title:
            print("Could not fetch title")
            continue
            
        # Create specific title
        new_title = create_specific_title(session_num, youtube_title)
        
        # Update the session
        data['sessions'][i]['title'] = new_title
        updated_count += 1
        
        print(f"Updated: {new_title}")
    
    # Save the updated JSON
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"\nCompleted! Updated {updated_count} session titles.")
    return updated_count

def update_html_files():
    """
    Update HTML files with new titles
    """
    json_file = Path('/data/work/dev/daurahtafsir-makro/data/usul_dirayat_hadis.json')
    html_dir = Path('/data/work/dev/daurahtafsir-makro/usul_dirayat_hadis')
    
    # Load the updated JSON data
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    updated_html_count = 0
    
    for session in data['sessions']:
        session_num = session['session_number']
        title = session['title']
        
        html_file = html_dir / f'sesi_{session_num}.html'
        
        if html_file.exists():
            # Read the HTML file
            with open(html_file, 'r', encoding='utf-8') as f:
                html_content = f.read()
            
            # Update the title in HTML
            # Update page title
            html_content = re.sub(
                r'<title>.*?</title>',
                f'<title>{title}</title>',
                html_content
            )
            
            # Update h1 title
            html_content = re.sub(
                r'<h1>.*?</h1>',
                f'<h1>{title}</h1>',
                html_content
            )
            
            # Write back the updated HTML
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            updated_html_count += 1
    
    print(f"Updated {updated_html_count} HTML files with new titles.")
    return updated_html_count

if __name__ == '__main__':
    print("Starting title update process...")
    
    # Update JSON titles
    json_updates = update_titles()
    
    # Update HTML files
    html_updates = update_html_files()
    
    print(f"\nSummary:")
    print(f"- Updated {json_updates} session titles in JSON")
    print(f"- Updated {html_updates} HTML files")
    print(f"\nTitle update process completed!")