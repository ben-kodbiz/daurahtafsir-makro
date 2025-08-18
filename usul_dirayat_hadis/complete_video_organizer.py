#!/usr/bin/env python3
"""
Complete Video Organizer for Usul Dirayat Hadis
This script provides a comprehensive solution for:
1. Automatically grouping videos into playlists by session numbers
2. Extracting video IDs correctly
3. Arranging IDs into session placeholders
4. Updating HTML files
"""

import json
import re
import subprocess
import sys
import os
from collections import defaultdict
from typing import Dict, List, Tuple, Optional

class VideoOrganizer:
    def __init__(self, json_file: str = 'usul_dirayat_hadis.json'):
        self.json_file = json_file
        self.data = self.load_json()
        
    def load_json(self) -> List[Dict]:
        """Load the main JSON file."""
        try:
            with open(self.json_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading {self.json_file}: {e}")
            return []
    
    def save_json(self) -> None:
        """Save the updated JSON file."""
        try:
            with open(self.json_file, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, ensure_ascii=False, indent=2)
            print(f"Saved updates to {self.json_file}")
        except Exception as e:
            print(f"Error saving {self.json_file}: {e}")
    
    def extract_session_number(self, title: str) -> int:
        """Extract session number from video title with improved patterns."""
        patterns = [
            r'sesi\s*(\d+)',
            r'session\s*(\d+)',
            r'\b(\d+)\s*[-–]',
            r'\[(\d+)\]',
            r'part\s*(\d+)',
            r'ep\s*(\d+)',
            r'episode\s*(\d+)',
            r'\b(\d+)\s*\.',
            r'\b(\d+)\s*:',
            r'usul\s*dirayat\s*hadis\s*(\d+)',
            r'hadis\s*(\d+)',
            r'\b(\d{1,3})\s*(?:st|nd|rd|th)?\s*(?:sesi|session|part|ep)'
        ]
        
        title_lower = title.lower()
        for pattern in patterns:
            match = re.search(pattern, title_lower)
            if match:
                num = int(match.group(1))
                if 1 <= num <= 120:  # Valid session range
                    return num
        
        return 0
    
    def get_playlist_videos(self, playlist_url: str) -> List[Tuple[str, str]]:
        """Extract all videos from a YouTube playlist."""
        try:
            cmd = [
                'yt-dlp',
                '--flat-playlist',
                '--print', '%(id)s|||%(title)s|||%(duration)s',
                playlist_url
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
            
            if result.returncode != 0:
                print(f"Error extracting playlist: {result.stderr}")
                return []
            
            videos = []
            for line in result.stdout.strip().split('\n'):
                if '|||' in line:
                    parts = line.split('|||')
                    if len(parts) >= 2:
                        video_id = parts[0].strip()
                        title = parts[1].strip()
                        videos.append((video_id, title))
            
            return videos
            
        except Exception as e:
            print(f"Error processing playlist {playlist_url}: {e}")
            return []
    
    def get_channel_videos(self, channel_url: str, max_videos: int = 300) -> List[Tuple[str, str]]:
        """Extract videos from a YouTube channel."""
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
    
    def organize_videos_by_session(self, videos: List[Tuple[str, str]]) -> Dict[int, List[Tuple[str, str]]]:
        """Organize videos by session number with smart matching."""
        session_groups = defaultdict(list)
        unmatched_videos = []
        
        for video_id, title in videos:
            session_num = self.extract_session_number(title)
            if session_num > 0:
                session_groups[session_num].append((video_id, title))
            else:
                unmatched_videos.append((video_id, title))
        
        # Try to match unmatched videos using fuzzy logic
        for video_id, title in unmatched_videos:
            best_match = self.find_best_session_match(title, session_groups)
            if best_match:
                session_groups[best_match].append((video_id, title))
        
        return dict(session_groups)
    
    def find_best_session_match(self, title: str, existing_groups: Dict[int, List]) -> Optional[int]:
        """Find the best session match for unmatched videos using keywords."""
        title_lower = title.lower()
        
        # Keywords that might indicate specific sessions
        keyword_patterns = {
            'pengenalan': [1, 2],
            'definisi': [1, 2, 3],
            'sejarah': [3, 4, 5],
            'klasifikasi': [6, 7, 8],
            'sanad': [10, 11, 12],
            'matan': [13, 14, 15],
            'sahih': [20, 21, 22],
            'hasan': [23, 24, 25],
            'dhaif': [26, 27, 28],
            'maudhu': [29, 30],
            'mutawatir': [31, 32],
            'ahad': [33, 34],
            'masyhur': [35, 36],
            'aziz': [37, 38],
            'gharib': [39, 40]
        }
        
        for keyword, possible_sessions in keyword_patterns.items():
            if keyword in title_lower:
                # Find the first available session in the range
                for session_num in possible_sessions:
                    if session_num not in existing_groups or len(existing_groups[session_num]) == 0:
                        return session_num
        
        return None
    
    def select_best_video_for_session(self, videos: List[Tuple[str, str]], session_num: int) -> Tuple[str, str]:
        """Select the best video for a session when multiple videos are available."""
        if len(videos) == 1:
            return videos[0]
        
        # Scoring system for video selection
        scored_videos = []
        
        for video_id, title in videos:
            score = 0
            title_lower = title.lower()
            
            # Prefer videos with exact session number match
            if f'sesi {session_num}' in title_lower or f'session {session_num}' in title_lower:
                score += 10
            
            # Prefer videos with 'usul dirayat hadis' in title
            if 'usul dirayat hadis' in title_lower:
                score += 5
            
            # Prefer longer titles (more descriptive)
            score += len(title) * 0.01
            
            # Avoid videos with certain keywords that indicate they might be wrong
            avoid_keywords = ['trailer', 'preview', 'intro', 'outro', 'announcement']
            if any(keyword in title_lower for keyword in avoid_keywords):
                score -= 5
            
            scored_videos.append((score, video_id, title))
        
        # Return the highest scored video
        scored_videos.sort(reverse=True)
        return (scored_videos[0][1], scored_videos[0][2])
    
    def update_sessions_with_videos(self, session_groups: Dict[int, List[Tuple[str, str]]]) -> int:
        """Update the JSON data with organized videos."""
        updated_count = 0
        
        for session in self.data:
            session_num = session['session']
            
            if session_num in session_groups:
                videos_for_session = session_groups[session_num]
                
                if videos_for_session:
                    # Select the best video for this session
                    video_id, title = self.select_best_video_for_session(videos_for_session, session_num)
                    
                    # Update the session
                    old_link = session['link']
                    session['link'] = f"https://www.youtube.com/watch?v={video_id}"
                    
                    # Clean and update title
                    clean_title = self.clean_video_title(title, session_num)
                    session['title'] = f"Sesi {session_num} – {clean_title}"
                    
                    if 'placeholder' in old_link:
                        updated_count += 1
                        print(f"✓ Updated Session {session_num}: {clean_title}")
                    
                    # Report if multiple videos were available
                    if len(videos_for_session) > 1:
                        print(f"  ℹ Multiple videos available for Session {session_num}, selected best match")
        
        return updated_count
    
    def clean_video_title(self, title: str, session_num: int) -> str:
        """Clean video title for better presentation."""
        # Remove session number from title if it's already there
        patterns_to_remove = [
            rf'sesi\s*{session_num}\s*[-–]?\s*',
            rf'session\s*{session_num}\s*[-–]?\s*',
            rf'\b{session_num}\s*[-–]\s*',
            r'usul\s*dirayat\s*hadis\s*[-–]?\s*',
            r'^[-–]\s*',
            r'\s*[-–]\s*$'
        ]
        
        cleaned = title
        for pattern in patterns_to_remove:
            cleaned = re.sub(pattern, '', cleaned, flags=re.IGNORECASE)
        
        # Clean up extra spaces and dashes
        cleaned = re.sub(r'\s+', ' ', cleaned).strip()
        cleaned = re.sub(r'^[-–]\s*', '', cleaned)
        cleaned = re.sub(r'\s*[-–]$', '', cleaned)
        
        return cleaned if cleaned else title
    
    def update_html_files(self) -> None:
        """Update all HTML files with new session data."""
        try:
            for session in self.data:
                session_num = session['session']
                html_file = f"session_{session_num}.html"
                
                if os.path.exists(html_file):
                    with open(html_file, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # Update video ID in HTML
                    video_id_match = re.search(r'v=([a-zA-Z0-9_-]{11})', session['link'])
                    if video_id_match:
                        new_video_id = video_id_match.group(1)
                        
                        # Replace video ID in iframe src
                        content = re.sub(
                            r'(src="[^"]*/)([a-zA-Z0-9_-]{11}|placeholder\d+)',
                            rf'\1{new_video_id}',
                            content
                        )
                        
                        # Update title in HTML
                        content = re.sub(
                            r'(<title>)[^<]*(</title>)',
                            rf'\1{session["title"]}\2',
                            content
                        )
                        
                        with open(html_file, 'w', encoding='utf-8') as f:
                            f.write(content)
            
            print("✓ Updated all HTML files")
            
        except Exception as e:
            print(f"Error updating HTML files: {e}")
    
    def generate_report(self, session_groups: Dict[int, List[Tuple[str, str]]]) -> None:
        """Generate a comprehensive report of the organization process."""
        print("\n" + "=" * 60)
        print("COMPLETE VIDEO ORGANIZATION REPORT")
        print("=" * 60)
        
        # Count current status
        total_sessions = len(self.data)
        sessions_with_real_videos = sum(1 for s in self.data if 'placeholder' not in s['link'])
        sessions_with_placeholders = total_sessions - sessions_with_real_videos
        
        print(f"Total sessions: {total_sessions}")
        print(f"Sessions with real videos: {sessions_with_real_videos}")
        print(f"Sessions with placeholders: {sessions_with_placeholders}")
        print(f"Completion rate: {sessions_with_real_videos/total_sessions*100:.1f}%")
        
        # Show sessions that were updated
        updated_sessions = sorted(session_groups.keys())
        if updated_sessions:
            print(f"\nSessions updated in this run: {len(updated_sessions)}")
            print(f"Updated sessions: {updated_sessions}")
        
        # Show remaining placeholders
        remaining_placeholders = [s['session'] for s in self.data if 'placeholder' in s['link']]
        if remaining_placeholders:
            print(f"\nRemaining placeholder sessions: {len(remaining_placeholders)}")
            if len(remaining_placeholders) <= 20:
                print(f"Sessions: {remaining_placeholders}")
            else:
                print(f"Sessions: {remaining_placeholders[:20]} ... and {len(remaining_placeholders)-20} more")
        
        print("\n" + "=" * 60)

def main():
    """Main function for complete video organization."""
    print("Complete Video Organizer for Usul Dirayat Hadis")
    print("=" * 50)
    
    # Check if yt-dlp is available
    try:
        subprocess.run(['yt-dlp', '--version'], capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("Error: yt-dlp is not installed or not available in PATH")
        print("Please install it with: pip install yt-dlp")
        sys.exit(1)
    
    organizer = VideoOrganizer()
    
    if not organizer.data:
        print("Error: Could not load usul_dirayat_hadis.json")
        sys.exit(1)
    
    print("\nChoose video source:")
    print("1. YouTube playlists (recommended for organized content)")
    print("2. YouTube channel")
    print("3. Mixed sources (playlists + channel)")
    
    choice = input("\nEnter choice (1-3): ").strip()
    
    all_videos = []
    
    if choice in ['1', '3']:
        # Get playlist URLs
        playlist_urls = []
        print("\nEnter YouTube playlist URLs (one per line, empty line to finish):")
        
        while True:
            url = input("Playlist URL: ").strip()
            if not url:
                break
            playlist_urls.append(url)
        
        # Extract from playlists
        for i, playlist_url in enumerate(playlist_urls, 1):
            print(f"\nProcessing playlist {i}/{len(playlist_urls)}...")
            videos = organizer.get_playlist_videos(playlist_url)
            all_videos.extend(videos)
            print(f"Extracted {len(videos)} videos from playlist {i}")
    
    if choice in ['2', '3']:
        # Get channel URL
        channel_url = input("\nEnter YouTube channel URL: ").strip()
        max_videos = int(input("Maximum videos to extract from channel (default 300): ") or "300")
        
        print(f"\nExtracting videos from channel...")
        channel_videos = organizer.get_channel_videos(channel_url, max_videos)
        all_videos.extend(channel_videos)
        print(f"Extracted {len(channel_videos)} videos from channel")
    
    if not all_videos:
        print("No videos extracted. Exiting.")
        sys.exit(1)
    
    print(f"\nTotal videos extracted: {len(all_videos)}")
    
    # Remove duplicates
    unique_videos = list(dict.fromkeys(all_videos))
    if len(unique_videos) != len(all_videos):
        print(f"Removed {len(all_videos) - len(unique_videos)} duplicate videos")
        all_videos = unique_videos
    
    # Organize videos by session
    print("\nOrganizing videos by session numbers...")
    session_groups = organizer.organize_videos_by_session(all_videos)
    
    if not session_groups:
        print("No videos could be organized by session numbers.")
        sys.exit(1)
    
    print(f"Successfully organized {sum(len(v) for v in session_groups.values())} videos into {len(session_groups)} sessions")
    
    # Update JSON file
    print("\nUpdating session data...")
    updated_count = organizer.update_sessions_with_videos(session_groups)
    
    if updated_count > 0:
        organizer.save_json()
        
        # Update HTML files
        print("\nUpdating HTML files...")
        organizer.update_html_files()
        
        print(f"\n✓ Successfully updated {updated_count} sessions!")
    else:
        print("\nNo sessions were updated (all may already have videos).")
    
    # Generate final report
    organizer.generate_report(session_groups)
    
    print("\n✓ Complete! Your Usul Dirayat Hadis module has been updated.")

if __name__ == "__main__":
    main()