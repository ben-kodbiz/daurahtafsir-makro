#!/usr/bin/env python3

import json
import os
import re

def read_video_ids(filename):
    """Read video IDs from file"""
    with open(filename, 'r') as f:
        return [line.strip() for line in f if line.strip()]

def update_json_file(json_file, video_ids):
    """Update the JSON file with real video IDs"""
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Update sessions with real video IDs
    for i, session in enumerate(data['sessions']):
        if i < len(video_ids):
            # Replace placeholder with real YouTube URL
            data['sessions'][i]['youtube_link'] = f"https://www.youtube.com/watch?v={video_ids[i]}"
        else:
            # If we don't have enough video IDs, keep the placeholder
            print(f"Warning: No video ID available for session {i+1}")
    
    # Write updated JSON back to file
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"Updated {json_file} with {min(len(video_ids), len(data['sessions']))} video IDs")

def update_html_files(video_ids):
    """Update HTML session files with real video IDs"""
    updated_count = 0
    
    for i, video_id in enumerate(video_ids):
        session_num = i + 1
        html_file = f"sesi_{session_num}.html"
        
        if os.path.exists(html_file):
            with open(html_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Replace placeholder video ID with real one
            # Pattern: placeholder followed by number or just placeholder
            placeholder_pattern = r'placeholder\d*'
            updated_content = re.sub(placeholder_pattern, video_id, content)
            
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(updated_content)
            
            updated_count += 1
            print(f"Updated {html_file} with video ID: {video_id}")
    
    print(f"Updated {updated_count} HTML files")

def main():
    # Read video IDs from file
    video_ids = read_video_ids('usul_dirayat_video_ids.txt')
    print(f"Found {len(video_ids)} video IDs")
    
    # Update JSON file (in data directory)
    update_json_file('../data/usul_dirayat_hadis.json', video_ids)
    
    # Update HTML files
    update_html_files(video_ids)
    
    print("\nUpdate completed successfully!")
    print(f"Total video IDs processed: {len(video_ids)}")

if __name__ == "__main__":
    main()