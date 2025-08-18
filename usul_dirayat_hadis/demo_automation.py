#!/usr/bin/env python3
"""
Demo script showing how the automated video organization works
"""

import sys
from complete_video_organizer import VideoOrganizer

def demo_session_detection():
    """Demonstrate session number detection capabilities."""
    print("🔍 Session Number Detection Demo")
    print("=" * 50)
    
    organizer = VideoOrganizer()
    
    # Sample video titles that might be found in playlists
    sample_titles = [
        "Sesi 1 – Pengenalan Usul Dirayat Hadis",
        "Session 15 - Klasifikasi Hadis Sahih",
        "25 - Metodologi Kritik Hadis",
        "[30] Analisis Sanad dan Matan",
        "Part 45 - Hadis Dhaif dan Karakteristiknya",
        "Usul Dirayat Hadis 60 - Hadis Maudhu",
        "Episode 75: Takhrij al-Hadis",
        "90. Aplikasi Modern Ilmu Hadis",
        "Kuliah Umum: Pentingnya Ilmu Hadis",  # Won't match
        "Sesi 150 - Out of Range Session",  # Won't match
    ]
    
    print("Sample video titles and detected sessions:")
    print("-" * 50)
    
    for title in sample_titles:
        session_num = organizer.extract_session_number(title)
        status = "✓" if session_num > 0 else "✗"
        result = f"Session {session_num}" if session_num > 0 else "No match"
        print(f"{status} {result:12} | {title}")
    
    print("\n💡 The system can detect session numbers from various formats!")

def demo_title_cleaning():
    """Demonstrate title cleaning functionality."""
    print("\n🧹 Title Cleaning Demo")
    print("=" * 50)
    
    organizer = VideoOrganizer()
    
    sample_data = [
        ("Sesi 1 – Pengenalan Usul Dirayat Hadis - Maulana Asri", 1),
        ("Session 15 - Usul Dirayat Hadis - Klasifikasi Hadis", 15),
        ("25 - Usul Dirayat Hadis: Metodologi Kritik", 25),
        ("Usul Dirayat Hadis - Sesi 30 - Analisis Mendalam", 30),
        ("45 – Hadis Dhaif dan Karakteristiknya [Usul Dirayat Hadis]", 45),
    ]
    
    print("Original titles → Cleaned titles:")
    print("-" * 50)
    
    for title, session_num in sample_data:
        cleaned = organizer.clean_video_title(title, session_num)
        print(f"Session {session_num:2d}: {title}")
        print(f"         → Sesi {session_num} – {cleaned}")
        print()
    
    print("💡 Titles are automatically cleaned to remove redundancy!")

def demo_video_selection():
    """Demonstrate video selection when multiple videos exist for same session."""
    print("\n🎯 Smart Video Selection Demo")
    print("=" * 50)
    
    organizer = VideoOrganizer()
    
    # Simulate multiple videos for session 15
    videos_for_session_15 = [
        ("abc123", "Sesi 15 - Trailer Upcoming Session"),  # Lower score (trailer)
        ("def456", "Session 15 - Usul Dirayat Hadis - Klasifikasi Hadis Sahih"),  # Higher score
        ("ghi789", "15 - Short Title"),  # Lower score (short)
        ("jkl012", "Sesi 15 - Usul Dirayat Hadis - Detailed Analysis of Hadis Classification"),  # Highest score
    ]
    
    print("Multiple videos found for Session 15:")
    print("-" * 50)
    
    for i, (video_id, title) in enumerate(videos_for_session_15, 1):
        print(f"{i}. {video_id} | {title}")
    
    # Select best video
    best_video_id, best_title = organizer.select_best_video_for_session(videos_for_session_15, 15)
    
    print(f"\n🏆 Selected: {best_video_id} | {best_title}")
    print("\n💡 The system automatically selects the most relevant video!")

def demo_workflow():
    """Demonstrate the complete workflow."""
    print("\n🔄 Complete Automation Workflow")
    print("=" * 50)
    
    workflow_steps = [
        "1. 📥 Extract videos from YouTube playlists/channels",
        "2. 🔍 Detect session numbers from video titles",
        "3. 📊 Group videos by session numbers",
        "4. 🎯 Select best video when multiple options exist",
        "5. 🧹 Clean and format video titles",
        "6. 💾 Update usul_dirayat_hadis.json file",
        "7. 🌐 Update all HTML files with new video IDs",
        "8. 📋 Generate comprehensive report"
    ]
    
    for step in workflow_steps:
        print(step)
    
    print("\n💡 All of this happens automatically with one command!")

def main():
    """Run the complete demo."""
    print("🚀 Automated Video Organization Demo")
    print("=" * 60)
    print("This demo shows how the automation scripts work to organize")
    print("your Usul Dirayat Hadis videos automatically!")
    print("=" * 60)
    
    try:
        demo_session_detection()
        demo_title_cleaning()
        demo_video_selection()
        demo_workflow()
        
        print("\n" + "=" * 60)
        print("🎉 Demo Complete!")
        print("=" * 60)
        print("\nTo use the automation:")
        print("1. Organize your videos into YouTube playlists")
        print("2. Run: python3 complete_video_organizer.py")
        print("3. Enter your playlist URLs")
        print("4. Let the magic happen! ✨")
        print("\nFor detailed instructions, see README_automation.md")
        
    except Exception as e:
        print(f"\n❌ Demo error: {e}")
        print("This is normal if the JSON file doesn't exist yet.")
        print("The automation will work when you have your video data!")

if __name__ == "__main__":
    main()