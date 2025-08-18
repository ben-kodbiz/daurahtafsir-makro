#!/usr/bin/env python3

import json
import os
import re
import time
import subprocess
from pathlib import Path
from difflib import SequenceMatcher

class TirmiziChannelExtractor:
    def __init__(self, json_file="jami_at_tirmizi.json"):
        self.json_file = json_file
        self.data = None
        self.extracted_videos = []
        self.session_assignments = {}
        
    def load_json_data(self):
        """Load the existing JSON data or create initial structure"""
        if os.path.exists(self.json_file):
            with open(self.json_file, 'r', encoding='utf-8') as f:
                self.data = json.load(f)
            print(f"✅ Loaded {len(self.data['sessions'])} sessions from {self.json_file}")
        else:
            # Create initial structure for Jami at-Tirmizi
            self.data = {
                "title": "Jami at-Tirmizi - Kitab Thaharah",
                "description": "Syarahan Kitab Hadith Jami' at-Tirmizi - Kitab Thaharah oleh Maulana Muhd Asri Yusoff",
                "sessions": []
            }
            print(f"📝 Created initial structure for {self.json_file}")
        return True
    
    def extract_session_number(self, title):
        """Extract session number from video title using multiple patterns for Tirmizi content"""
        title_lower = title.lower()
        
        # Pattern for Tirmizi content
        patterns = [
            r'sesi\s*(\d+)',
            r'session\s*(\d+)',
            r'part\s*(\d+)',
            r'episode\s*(\d+)',
            r'ep\s*(\d+)',
            r'\b(\d+)\s*-\s*tirmizi',
            r'tirmizi.*?(\d+)',
            r'thaharah.*?(\d+)',
            r'kitab.*?(\d+)',
            r'\b(\d{1,3})\b.*tirmizi',
            r'\b(\d{1,3})\b.*thaharah',
            r'\b(\d{1,3})\b.*kitab',
            r'hadith.*?(\d+)',
            r'hadis.*?(\d+)',
            r'\b(\d{1,3})\b.*hadith',
            r'\b(\d{1,3})\b.*hadis'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, title_lower)
            if match:
                session_num = int(match.group(1))
                if 1 <= session_num <= 200:  # Reasonable range
                    return session_num
        
        # Try to extract any number from the title as fallback
        numbers = re.findall(r'\b(\d{1,3})\b', title)
        for num_str in numbers:
            num = int(num_str)
            if 1 <= num <= 200:
                return num
                
        return None
    
    def extract_videos_from_channel(self, channel_url, max_videos=200):
        """Extract video information from YouTube channel using yt-dlp"""
        print(f"🔍 Extracting videos from channel: {channel_url}")
        print(f"📊 Maximum videos to extract: {max_videos}")
        
        try:
            # Use yt-dlp to extract video information
            cmd = [
                'yt-dlp',
                '--flat-playlist',
                '--print', '%(id)s|%(title)s|%(url)s',
                '--playlist-end', str(max_videos),
                channel_url
            ]
            
            print(f"🚀 Running command: {' '.join(cmd)}")
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
            
            if result.returncode != 0:
                print(f"❌ Error running yt-dlp: {result.stderr}")
                return False
            
            # Parse the output
            lines = result.stdout.strip().split('\n')
            print(f"📥 Found {len(lines)} videos")
            
            for line in lines:
                if '|' in line:
                    parts = line.split('|', 2)
                    if len(parts) >= 2:
                        video_id = parts[0].strip()
                        title = parts[1].strip()
                        url = f"https://www.youtube.com/watch?v={video_id}"
                        
                        # Extract session number
                        session_num = self.extract_session_number(title)
                        
                        video_info = {
                            'video_id': video_id,
                            'title': title,
                            'url': url,
                            'extracted_session': session_num
                        }
                        
                        self.extracted_videos.append(video_info)
                        
                        if session_num:
                            print(f"📹 Session {session_num}: {title[:60]}...")
                        else:
                            print(f"❓ No session detected: {title[:60]}...")
            
            print(f"✅ Successfully extracted {len(self.extracted_videos)} videos")
            return True
            
        except subprocess.TimeoutExpired:
            print("⏰ Command timed out after 5 minutes")
            return False
        except Exception as e:
            print(f"❌ Error extracting videos: {str(e)}")
            return False
    
    def similarity(self, a, b):
        """Calculate similarity between two strings"""
        return SequenceMatcher(None, a.lower(), b.lower()).ratio()
    
    def create_sessions_from_videos(self):
        """Create session structure from extracted videos"""
        print("\n🔄 Creating sessions from extracted videos...")
        
        # Group videos by session number
        session_groups = {}
        unassigned_videos = []
        
        for video in self.extracted_videos:
            session_num = video['extracted_session']
            if session_num:
                if session_num not in session_groups:
                    session_groups[session_num] = []
                session_groups[session_num].append(video)
            else:
                unassigned_videos.append(video)
        
        # Create sessions
        sessions = []
        for session_num in sorted(session_groups.keys()):
            videos = session_groups[session_num]
            
            # If multiple videos for same session, pick the best one
            if len(videos) > 1:
                # Prefer videos with more specific titles
                best_video = max(videos, key=lambda v: len(v['title']))
                print(f"📹 Session {session_num}: Selected '{best_video['title'][:50]}...' from {len(videos)} options")
            else:
                best_video = videos[0]
                print(f"📹 Session {session_num}: {best_video['title'][:50]}...")
            
            # Clean up the title for session
            clean_title = self.clean_title(best_video['title'])
            
            session = {
                "session_number": session_num,
                "title": clean_title,
                "video_id": best_video['video_id'],
                "youtube_url": best_video['url']
            }
            sessions.append(session)
        
        # Handle unassigned videos by creating sequential sessions
        if unassigned_videos:
            print(f"\n📝 Assigning {len(unassigned_videos)} unassigned videos to sequential sessions...")
            next_session = max(session_groups.keys()) + 1 if session_groups else 1
            
            for video in unassigned_videos:
                clean_title = self.clean_title(video['title'])
                session = {
                    "session_number": next_session,
                    "title": clean_title,
                    "video_id": video['video_id'],
                    "youtube_url": video['url']
                }
                sessions.append(session)
                print(f"📹 Session {next_session}: {clean_title[:50]}...")
                next_session += 1
        
        # Sort sessions by session number
        sessions.sort(key=lambda x: x['session_number'])
        self.data['sessions'] = sessions
        
        print(f"\n✅ Created {len(sessions)} sessions")
        return sessions
    
    def clean_title(self, title):
        """Clean up video title for session display"""
        # Remove common prefixes/suffixes
        title = re.sub(r'^(Jami\s*at-Tirmizi|Tirmizi|Kitab\s*Thaharah)\s*[-:]?\s*', '', title, flags=re.IGNORECASE)
        title = re.sub(r'\s*[-:]?\s*(Maulana\s*Asri|Maulana\s*Muhd\s*Asri\s*Yusoff).*$', '', title, flags=re.IGNORECASE)
        
        # Remove session numbers from title if they're at the beginning
        title = re.sub(r'^(Sesi|Session|Part|Episode|Ep)\s*\d+\s*[-:]?\s*', '', title, flags=re.IGNORECASE)
        
        # Clean up extra whitespace and dashes
        title = re.sub(r'\s*[-:]\s*', ' - ', title)
        title = re.sub(r'\s+', ' ', title).strip()
        
        return title if title else "Jami at-Tirmizi - Kitab Thaharah"
    
    def save_json_data(self):
        """Save the updated JSON data"""
        with open(self.json_file, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)
        print(f"💾 Saved data to {self.json_file}")
    
    def generate_report(self):
        """Generate a summary report"""
        print("\n" + "="*60)
        print("📊 EXTRACTION REPORT")
        print("="*60)
        print(f"📁 JSON File: {self.json_file}")
        print(f"📹 Total Videos Extracted: {len(self.extracted_videos)}")
        print(f"📚 Total Sessions Created: {len(self.data['sessions'])}")
        
        if self.data['sessions']:
            session_numbers = [s['session_number'] for s in self.data['sessions']]
            print(f"📈 Session Range: {min(session_numbers)} - {max(session_numbers)}")
        
        print("\n✅ Extraction completed successfully!")
        print("="*60)
    
    def run_full_extraction(self, channel_url):
        """Run the complete extraction process"""
        print("🚀 Starting Jami at-Tirmizi video extraction...")
        
        # Load existing data
        if not self.load_json_data():
            return False
        
        # Extract videos from channel
        if not self.extract_videos_from_channel(channel_url):
            return False
        
        # Create sessions from videos
        self.create_sessions_from_videos()
        
        # Save the data
        self.save_json_data()
        
        # Generate report
        self.generate_report()
        
        return True

def main():
    # Channel URL for Jami at-Tirmizi
    channel_url = "https://www.youtube.com/channel/UCYwDmnff7eBnXAYOrqnWdYg/videos"
    
    extractor = TirmiziChannelExtractor()
    success = extractor.run_full_extraction(channel_url)
    
    if success:
        print("\n🎉 Video extraction completed successfully!")
    else:
        print("\n❌ Video extraction failed!")

if __name__ == "__main__":
    main()