#!/usr/bin/env python3

import json
import re
from subprocess import run, PIPE
import time

def get_video_title(video_id):
    """Get video title from YouTube using yt-dlp"""
    try:
        result = run(['yt-dlp', '--dump-json', f'https://www.youtube.com/watch?v={video_id}'], 
                    capture_output=True, text=True, timeout=30)
        if result.returncode == 0:
            data = json.loads(result.stdout)
            return data.get('title', 'Unknown Title')
        else:
            return None
    except Exception as e:
        return None

def extract_session_number_from_title(title):
    """Extract session number from video title with improved patterns"""
    if not title:
        return None
        
    title_lower = title.lower()
    
    # Specific patterns for this series
    patterns = [
        r'sesi\s+(\d+)',  # "Sesi 18"
        r'ke-(\d+)',      # "ke-10"
        r'usul\s+no\.?\s*(\d+)',  # "Usul No 5", "Usul no 36"
        r'usul\s+(\d+)',  # "Usul 5"
        r'^(\d+)\s*-',    # "18 - title"
        r'\b(\d+)\s*(?:th|st|nd|rd)?\s*(?:session|sesi)',  # "18th session"
        r'(?:session|sesi)\s+(\d+)',  # "Session 18"
    ]
    
    for pattern in patterns:
        matches = re.findall(pattern, title_lower)
        for match in matches:
            num = int(match)
            if 1 <= num <= 120:  # Valid session range
                return num
    
    # Look for any number that could be a session (1-120)
    numbers = re.findall(r'\b(\d+)\b', title)
    for num_str in numbers:
        num = int(num_str)
        if 1 <= num <= 120:
            return num
    
    return None

def create_session_mapping():
    """Create mapping of session numbers to video IDs"""
    print("Creating session mapping from all available videos...\n")
    
    # Read all video IDs
    with open('all_usul_video_ids.txt', 'r') as f:
        video_ids = [line.strip() for line in f if line.strip()]
    
    print(f"Processing {len(video_ids)} video IDs...")
    
    session_mapping = {}
    processed = 0
    
    for i, video_id in enumerate(video_ids):
        processed += 1
        print(f"Processing {processed}/{len(video_ids)}: {video_id}")
        
        title = get_video_title(video_id)
        if not title:
            print(f"  ❌ Could not get title")
            continue
            
        print(f"  Title: {title}")
        
        session_num = extract_session_number_from_title(title)
        if session_num:
            if session_num not in session_mapping:
                session_mapping[session_num] = []
            
            session_mapping[session_num].append({
                'video_id': video_id,
                'title': title
            })
            print(f"  ✅ Mapped to session {session_num}")
        else:
            print(f"  ⚠️  No session number detected")
        
        # Add small delay to avoid rate limiting
        if i % 10 == 9:
            print("  Pausing to avoid rate limiting...")
            time.sleep(2)
    
    # Save mapping to file
    with open('session_mapping.json', 'w', encoding='utf-8') as f:
        json.dump(session_mapping, f, indent=2, ensure_ascii=False)
    
    print(f"\nMapping completed!")
    print(f"Found videos for {len(session_mapping)} sessions")
    print(f"Sessions found: {sorted(session_mapping.keys())}")
    
    # Show statistics
    sessions_with_multiple = {k: v for k, v in session_mapping.items() if len(v) > 1}
    if sessions_with_multiple:
        print(f"\nSessions with multiple videos: {len(sessions_with_multiple)}")
        for session, videos in sessions_with_multiple.items():
            print(f"  Session {session}: {len(videos)} videos")
    
    missing_sessions = [i for i in range(1, 121) if i not in session_mapping]
    print(f"\nMissing sessions (1-120): {len(missing_sessions)}")
    if len(missing_sessions) <= 20:
        print(f"Missing: {missing_sessions}")
    else:
        print(f"Missing: {missing_sessions[:10]}... and {len(missing_sessions)-10} more")
    
    return session_mapping

def select_best_video_for_session(videos):
    """Select the best video for a session when multiple are available"""
    if len(videos) == 1:
        return videos[0]
    
    # Prefer videos with "Sesi" in title
    sesi_videos = [v for v in videos if 'sesi' in v['title'].lower()]
    if sesi_videos:
        return sesi_videos[0]
    
    # Prefer videos with "Usul" in title
    usul_videos = [v for v in videos if 'usul' in v['title'].lower()]
    if usul_videos:
        return usul_videos[0]
    
    # Return first video as fallback
    return videos[0]

def update_json_with_mapping():
    """Update the JSON file with the correct video mapping"""
    print("\nUpdating JSON file with correct video mapping...")
    
    # Load session mapping
    with open('session_mapping.json', 'r', encoding='utf-8') as f:
        session_mapping = json.load(f)
    
    # Convert string keys to integers
    session_mapping = {int(k): v for k, v in session_mapping.items()}
    
    # Load current JSON
    with open('../data/usul_dirayat_hadis.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    updated_count = 0
    
    for session in data['sessions']:
        session_num = session['session_number']
        
        if session_num in session_mapping:
            # Select best video for this session
            best_video = select_best_video_for_session(session_mapping[session_num])
            new_url = f"https://www.youtube.com/watch?v={best_video['video_id']}"
            
            if session['youtube_link'] != new_url:
                print(f"Updating session {session_num}: {best_video['video_id']}")
                print(f"  Title: {best_video['title']}")
                session['youtube_link'] = new_url
                updated_count += 1
        else:
            print(f"No video found for session {session_num}")
    
    # Save updated JSON
    with open('../data/usul_dirayat_hadis.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"\nUpdated {updated_count} sessions in JSON file")
    return updated_count

def update_html_files():
    """Update HTML files with correct video IDs"""
    print("\nUpdating HTML files...")
    
    # Load session mapping
    with open('session_mapping.json', 'r', encoding='utf-8') as f:
        session_mapping = json.load(f)
    
    # Convert string keys to integers
    session_mapping = {int(k): v for k, v in session_mapping.items()}
    
    updated_files = 0
    
    for session_num in range(1, 121):
        html_file = f"sesi_{session_num}.html"
        
        if session_num in session_mapping:
            best_video = select_best_video_for_session(session_mapping[session_num])
            video_id = best_video['video_id']
            
            try:
                with open(html_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Update iframe src
                new_content = re.sub(
                    r'src="https://www\.youtube\.com/embed/[^"]*"',
                    f'src="https://www.youtube.com/embed/{video_id}"',
                    content
                )
                
                if new_content != content:
                    with open(html_file, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    print(f"Updated {html_file} with video {video_id}")
                    updated_files += 1
                    
            except FileNotFoundError:
                print(f"HTML file not found: {html_file}")
    
    print(f"\nUpdated {updated_files} HTML files")
    return updated_files

if __name__ == "__main__":
    print("=" * 60)
    print("SESSION MAPPING CREATOR")
    print("=" * 60)
    
    # Create mapping
    mapping = create_session_mapping()
    
    # Update files
    json_updates = update_json_with_mapping()
    html_updates = update_html_files()
    
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"Sessions mapped: {len(mapping)}")
    print(f"JSON sessions updated: {json_updates}")
    print(f"HTML files updated: {html_updates}")
    print("\nMapping completed!")