#!/usr/bin/env python3

import json
import os
import re
from subprocess import run, PIPE

def get_video_title(video_id):
    """Get video title from YouTube using yt-dlp"""
    try:
        result = run(['yt-dlp', '--dump-json', f'https://www.youtube.com/watch?v={video_id}'], 
                    capture_output=True, text=True, timeout=30)
        if result.returncode == 0:
            data = json.loads(result.stdout)
            return data.get('title', 'Unknown Title')
        else:
            return f"Error: {result.stderr.strip()}"
    except Exception as e:
        return f"Exception: {str(e)}"

def extract_session_number_from_title(title):
    """Extract session number from video title"""
    # Look for patterns like "Sesi 1", "Session 1", "ke-1", etc.
    patterns = [
        r'[Ss]esi\s+(\d+)',
        r'[Ss]ession\s+(\d+)',
        r'ke-(\d+)',
        r'(\d+)\s*-',
        r'\b(\d+)\b'
    ]
    
    for pattern in patterns:
        match = re.search(pattern, title)
        if match:
            return int(match.group(1))
    return None

def test_video_placement():
    """Test if video IDs are correctly placed according to session numbers"""
    print("Testing video ID placement...\n")
    
    # Read JSON file
    with open('../data/usul_dirayat_hadis.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    mismatches = []
    correct_placements = []
    errors = []
    
    for session in data['sessions']:
        session_num = session['session_number']
        youtube_link = session['youtube_link']
        session_title = session['title']
        
        # Skip placeholder links
        if 'placeholder' in youtube_link:
            continue
            
        # Extract video ID from URL
        video_id_match = re.search(r'[?&]v=([^&]+)', youtube_link)
        if not video_id_match:
            video_id_match = re.search(r'/watch\?v=([^&]+)', youtube_link)
        
        if video_id_match:
            video_id = video_id_match.group(1)
            
            print(f"Checking Session {session_num}: {session_title}")
            print(f"Video ID: {video_id}")
            
            # Get actual video title
            actual_title = get_video_title(video_id)
            print(f"Actual video title: {actual_title}")
            
            if "Error" in actual_title or "Exception" in actual_title:
                errors.append({
                    'session': session_num,
                    'video_id': video_id,
                    'error': actual_title
                })
                print(f"❌ Error getting video title\n")
                continue
            
            # Extract session number from actual video title
            actual_session_num = extract_session_number_from_title(actual_title)
            
            if actual_session_num and actual_session_num == session_num:
                correct_placements.append({
                    'session': session_num,
                    'video_id': video_id,
                    'title': actual_title
                })
                print(f"✅ Correctly placed\n")
            else:
                mismatches.append({
                    'expected_session': session_num,
                    'actual_session': actual_session_num,
                    'video_id': video_id,
                    'actual_title': actual_title,
                    'session_title': session_title
                })
                print(f"❌ Mismatch: Expected session {session_num}, found session {actual_session_num}\n")
        else:
            print(f"❌ Could not extract video ID from: {youtube_link}\n")
    
    # Summary
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    print(f"Total sessions checked: {len([s for s in data['sessions'] if 'placeholder' not in s['youtube_link']])}")
    print(f"Correctly placed: {len(correct_placements)}")
    print(f"Mismatched: {len(mismatches)}")
    print(f"Errors: {len(errors)}")
    
    if mismatches:
        print("\nMISMATCHED VIDEOS:")
        for mismatch in mismatches:
            print(f"  Session {mismatch['expected_session']}: {mismatch['video_id']}")
            print(f"    Expected: Session {mismatch['expected_session']}")
            print(f"    Actual: Session {mismatch['actual_session']} - {mismatch['actual_title']}")
            print()
    
    if errors:
        print("\nERRORS:")
        for error in errors:
            print(f"  Session {error['session']}: {error['video_id']} - {error['error']}")
    
    return {
        'correct': correct_placements,
        'mismatches': mismatches,
        'errors': errors
    }

def check_available_videos():
    """Check how many videos we have and what sessions they represent"""
    print("\nChecking available video IDs...")
    
    if not os.path.exists('usul_dirayat_video_ids.txt'):
        print("Video IDs file not found!")
        return
    
    with open('usul_dirayat_video_ids.txt', 'r') as f:
        video_ids = [line.strip() for line in f if line.strip()]
    
    print(f"Total video IDs available: {len(video_ids)}")
    
    # Check what sessions these videos represent
    session_mapping = {}
    for i, video_id in enumerate(video_ids[:10]):  # Check first 10 to avoid rate limiting
        print(f"Checking video {i+1}/{min(10, len(video_ids))}: {video_id}")
        title = get_video_title(video_id)
        session_num = extract_session_number_from_title(title)
        if session_num:
            session_mapping[session_num] = {
                'video_id': video_id,
                'title': title
            }
        print(f"  Title: {title}")
        print(f"  Detected session: {session_num}")
    
    print(f"\nDetected sessions from first 10 videos: {sorted(session_mapping.keys())}")
    return session_mapping

if __name__ == "__main__":
    print("=" * 60)
    print("VIDEO PLACEMENT TEST SCRIPT")
    print("=" * 60)
    
    # Test current placement
    results = test_video_placement()
    
    # Check available videos
    available_sessions = check_available_videos()
    
    print("\nTest completed!")