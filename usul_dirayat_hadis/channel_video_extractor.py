#!/usr/bin/env python3

import json
import os
import re
import time
import subprocess
from pathlib import Path
from difflib import SequenceMatcher

class ChannelVideoExtractor:
    def __init__(self, json_file="usul_dirayat_hadis.json"):
        self.json_file = json_file
        self.data = None
        self.extracted_videos = []
        self.session_assignments = {}
        
    def load_json_data(self):
        """Load the existing JSON data"""
        if os.path.exists(self.json_file):
            with open(self.json_file, 'r', encoding='utf-8') as f:
                self.data = json.load(f)
            print(f"✅ Loaded {len(self.data['sessions'])} sessions from {self.json_file}")
        else:
            print(f"❌ JSON file {self.json_file} not found")
            return False
        return True
    
    def extract_session_number(self, title):
        """Extract session number from video title using multiple patterns"""
        title_lower = title.lower()
        
        # Pattern 1: Direct session number (Sesi 1, Session 1, etc.)
        patterns = [
            r'sesi\s*(\d+)',
            r'session\s*(\d+)',
            r'part\s*(\d+)',
            r'episode\s*(\d+)',
            r'ep\s*(\d+)',
            r'\b(\d+)\s*-\s*usul',
            r'usul.*?(\d+)',
            r'hadis.*?(\d+)',
            r'dirayat.*?(\d+)',
            r'\b(\d{1,3})\b.*usul',
            r'\b(\d{1,3})\b.*hadis',
            r'\b(\d{1,3})\b.*dirayat'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, title_lower)
            if match:
                session_num = int(match.group(1))
                if 1 <= session_num <= 120:
                    return session_num
        
        # Pattern 2: Date-based extraction (if videos are chronologically ordered)
        date_patterns = [
            r'(\d{2})(\d{2})(\d{4})',  # DDMMYYYY
            r'(\d{4})(\d{2})(\d{2})',  # YYYYMMDD
            r'(\d{2})/(\d{2})/(\d{4})', # DD/MM/YYYY
        ]
        
        for pattern in date_patterns:
            match = re.search(pattern, title)
            if match:
                # This could be used for chronological ordering
                pass
        
        return None
    
    def extract_videos_from_channel(self, channel_url, max_videos=200):
        """Extract video IDs and titles from YouTube channel with rate limiting"""
        print(f"🔍 Extracting videos from channel: {channel_url}")
        print(f"⏱️  Using 3-4 second delays between requests to avoid rate limiting")
        
        try:
            # Use yt-dlp to extract video information
            cmd = [
                'yt-dlp',
                '--flat-playlist',
                '--print', '%(id)s|%(title)s|%(upload_date)s',
                '--playlist-end', str(max_videos),
                channel_url
            ]
            
            print("🚀 Starting video extraction...")
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
            
            if result.returncode != 0:
                print(f"❌ Error extracting videos: {result.stderr}")
                return False
            
            lines = result.stdout.strip().split('\n')
            print(f"📊 Found {len(lines)} videos in channel")
            
            for i, line in enumerate(lines):
                if '|' in line:
                    parts = line.split('|')
                    if len(parts) >= 2:
                        video_id = parts[0]
                        title = parts[1]
                        upload_date = parts[2] if len(parts) > 2 else ''
                        
                        self.extracted_videos.append({
                            'video_id': video_id,
                            'title': title,
                            'upload_date': upload_date,
                            'youtube_url': f'https://www.youtube.com/watch?v={video_id}'
                        })
                        
                        # Rate limiting: 3-4 second pause every 10 videos
                        if (i + 1) % 10 == 0:
                            delay = 3.5  # 3.5 seconds average
                            print(f"⏳ Processed {i + 1} videos, pausing for {delay} seconds...")
                            time.sleep(delay)
            
            print(f"✅ Successfully extracted {len(self.extracted_videos)} videos")
            return True
            
        except subprocess.TimeoutExpired:
            print("❌ Extraction timed out after 5 minutes")
            return False
        except Exception as e:
            print(f"❌ Error during extraction: {e}")
            return False
    
    def similarity(self, a, b):
        """Calculate similarity between two strings"""
        return SequenceMatcher(None, a.lower(), b.lower()).ratio()
    
    def smart_session_matching(self):
        """Intelligently match extracted videos to session numbers"""
        print("🧠 Starting smart session matching...")
        
        # First pass: Direct session number extraction
        direct_matches = {}
        unmatched_videos = []
        
        for video in self.extracted_videos:
            session_num = self.extract_session_number(video['title'])
            if session_num:
                if session_num not in direct_matches:
                    direct_matches[session_num] = []
                direct_matches[session_num].append(video)
                print(f"📍 Direct match: Session {session_num} - {video['title'][:60]}...")
            else:
                unmatched_videos.append(video)
        
        print(f"✅ Direct matches found: {len(direct_matches)} sessions")
        print(f"🔍 Unmatched videos: {len(unmatched_videos)}")
        
        # Second pass: Fuzzy matching for unmatched videos
        if unmatched_videos:
            print("🔍 Attempting fuzzy matching for remaining videos...")
            
            for video in unmatched_videos:
                best_match = None
                best_score = 0
                
                for session in self.data['sessions']:
                    session_num = session['session_number']
                    if session_num in direct_matches:
                        continue  # Skip already matched sessions
                    
                    # Compare with session title
                    score = self.similarity(video['title'], session['title'])
                    
                    # Boost score for keyword matches
                    keywords = ['usul', 'dirayat', 'hadis', 'hadith']
                    for keyword in keywords:
                        if keyword in video['title'].lower() and keyword in session['title'].lower():
                            score += 0.1
                    
                    if score > best_score and score > 0.3:  # Minimum similarity threshold
                        best_score = score
                        best_match = session_num
                
                if best_match:
                    if best_match not in direct_matches:
                        direct_matches[best_match] = []
                    direct_matches[best_match].append(video)
                    print(f"🎯 Fuzzy match: Session {best_match} - {video['title'][:60]}... (score: {best_score:.2f})")
        
        # Third pass: Chronological assignment for remaining videos
        remaining_sessions = [s['session_number'] for s in self.data['sessions'] if s['session_number'] not in direct_matches]
        remaining_videos = [v for v in self.extracted_videos if not any(v in videos for videos in direct_matches.values())]
        
        if remaining_videos and remaining_sessions:
            print(f"📅 Chronologically assigning {len(remaining_videos)} remaining videos to {len(remaining_sessions)} sessions")
            
            # Sort videos by upload date if available
            remaining_videos.sort(key=lambda x: x.get('upload_date', ''), reverse=False)
            remaining_sessions.sort()
            
            for i, video in enumerate(remaining_videos[:len(remaining_sessions)]):
                session_num = remaining_sessions[i]
                if session_num not in direct_matches:
                    direct_matches[session_num] = []
                direct_matches[session_num].append(video)
                print(f"📅 Chronological assignment: Session {session_num} - {video['title'][:60]}...")
        
        self.session_assignments = direct_matches
        print(f"\n✅ Session matching complete: {len(direct_matches)} sessions assigned")
        return direct_matches
    
    def select_best_video_per_session(self):
        """Select the best video for each session when multiple videos are available"""
        print("🎯 Selecting best video for each session...")
        
        final_assignments = {}
        
        for session_num, videos in self.session_assignments.items():
            if len(videos) == 1:
                final_assignments[session_num] = videos[0]
            else:
                # Multiple videos for same session - select best one
                best_video = None
                best_score = 0
                
                for video in videos:
                    score = 0
                    title_lower = video['title'].lower()
                    
                    # Prefer videos with session number in title
                    if str(session_num) in title_lower:
                        score += 2
                    
                    # Prefer videos with key terms
                    key_terms = ['usul', 'dirayat', 'hadis']
                    for term in key_terms:
                        if term in title_lower:
                            score += 1
                    
                    # Prefer longer titles (more descriptive)
                    score += len(video['title']) / 1000
                    
                    if score > best_score:
                        best_score = score
                        best_video = video
                
                final_assignments[session_num] = best_video or videos[0]
                print(f"🎯 Session {session_num}: Selected '{best_video['title'][:50]}...' from {len(videos)} options")
        
        return final_assignments
    
    def update_json_with_assignments(self, assignments):
        """Update the JSON file with video assignments"""
        print("💾 Updating JSON file with video assignments...")
        
        updated_count = 0
        
        for session in self.data['sessions']:
            session_num = session['session_number']
            if session_num in assignments:
                video = assignments[session_num]
                session['video_id'] = video['video_id']
                session['youtube_url'] = video['youtube_url']
                updated_count += 1
                print(f"✅ Updated Session {session_num}: {video['video_id']}")
        
        # Save updated JSON
        with open(self.json_file, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, indent=2, ensure_ascii=False)
        
        print(f"\n💾 Updated {updated_count} sessions in {self.json_file}")
        return updated_count
    
    def update_html_files(self, assignments):
        """Update HTML files with new video IDs"""
        print("🌐 Updating HTML files with new video IDs...")
        
        updated_files = 0
        
        for session_num, video in assignments.items():
            html_file = f"sesi_{session_num}.html"
            if os.path.exists(html_file):
                with open(html_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Replace video ID in iframe src
                old_pattern = r'youtube\.com/embed/[a-zA-Z0-9_-]+'
                new_embed = f'youtube.com/embed/{video["video_id"]}'
                
                if re.search(old_pattern, content):
                    updated_content = re.sub(old_pattern, new_embed, content)
                    
                    with open(html_file, 'w', encoding='utf-8') as f:
                        f.write(updated_content)
                    
                    updated_files += 1
                    print(f"✅ Updated {html_file} with video ID: {video['video_id']}")
        
        print(f"\n🌐 Updated {updated_files} HTML files")
        return updated_files
    
    def generate_report(self, assignments):
        """Generate a detailed report of the extraction and assignment process"""
        print("\n" + "=" * 60)
        print("📊 CHANNEL VIDEO EXTRACTION REPORT")
        print("=" * 60)
        
        print(f"\n📺 Total videos extracted: {len(self.extracted_videos)}")
        print(f"🎯 Sessions assigned: {len(assignments)}")
        print(f"📝 Remaining unassigned sessions: {120 - len(assignments)}")
        
        if assignments:
            print("\n✅ Successfully assigned sessions:")
            for session_num in sorted(assignments.keys()):
                video = assignments[session_num]
                print(f"   Session {session_num:3d}: {video['title'][:70]}...")
        
        unassigned = [i for i in range(1, 121) if i not in assignments]
        if unassigned:
            print(f"\n⚠️  Unassigned sessions ({len(unassigned)}): {unassigned[:20]}{'...' if len(unassigned) > 20 else ''}")
        
        print("\n" + "=" * 60)
    
    def run_full_extraction(self, channel_url):
        """Run the complete extraction and assignment process"""
        print("🚀 Starting Channel Video Extraction Process")
        print("=" * 50)
        
        # Step 1: Load existing data
        if not self.load_json_data():
            return False
        
        # Step 2: Extract videos from channel
        if not self.extract_videos_from_channel(channel_url):
            return False
        
        # Step 3: Smart session matching
        self.smart_session_matching()
        
        # Step 4: Select best video per session
        final_assignments = self.select_best_video_per_session()
        
        # Step 5: Update JSON file
        self.update_json_with_assignments(final_assignments)
        
        # Step 6: Update HTML files
        self.update_html_files(final_assignments)
        
        # Step 7: Generate report
        self.generate_report(final_assignments)
        
        print("\n🎉 Channel video extraction completed successfully!")
        return True

def main():
    """Main function to run the channel video extractor"""
    extractor = ChannelVideoExtractor()
    
    # Get channel URL from user
    print("🎬 Channel Video Extractor for Usul Dirayat Hadis")
    print("=" * 50)
    
    channel_url = input("Enter YouTube channel URL: ").strip()
    
    if not channel_url:
        print("❌ No channel URL provided")
        return
    
    # Run the extraction process
    success = extractor.run_full_extraction(channel_url)
    
    if success:
        print("\n✅ Process completed successfully!")
        print("🌐 You can now test the web application with updated videos")
    else:
        print("\n❌ Process failed. Please check the errors above.")

if __name__ == "__main__":
    main()