#!/usr/bin/env python3
"""
Automation Tools Menu for Usul Dirayat Hadis
Provides easy access to all automation scripts
"""

import os
import sys
import subprocess

def show_menu():
    """Display the automation tools menu."""
    print("🤖 Usul Dirayat Hadis Automation Tools")
    print("=" * 50)
    print("Choose an automation tool:")
    print()
    print("1. 🚀 Complete Video Organizer (Recommended)")
    print("   - Fully automated playlist/channel organization")
    print("   - Smart session detection and video selection")
    print("   - Updates JSON and HTML files automatically")
    print()
    print("2. 📋 Playlist Organizer")
    print("   - Focus on playlist-based organization")
    print("   - Groups videos by session numbers")
    print()
    print("3. 🔧 Video ID Extractor")
    print("   - Extract videos for manual review")
    print("   - Channel, playlist, or search extraction")
    print("   - Manual assignment capabilities")
    print()
    print("4. 🧪 Test Automation")
    print("   - Test session detection and title cleaning")
    print("   - Verify automation functionality")
    print()
    print("5. 🎬 Demo Automation")
    print("   - See how the automation works")
    print("   - Examples and workflow demonstration")
    print()
    print("6. 📖 View Documentation")
    print("   - Read the automation guide")
    print("   - Best practices and troubleshooting")
    print()
    print("0. ❌ Exit")
    print()

def run_script(script_name):
    """Run a Python script."""
    try:
        subprocess.run([sys.executable, script_name], check=True)
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Error running {script_name}: {e}")
    except KeyboardInterrupt:
        print(f"\n⏹️  Interrupted {script_name}")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")

def view_documentation():
    """Display the documentation."""
    doc_file = "README_automation.md"
    if os.path.exists(doc_file):
        try:
            with open(doc_file, 'r', encoding='utf-8') as f:
                content = f.read()
            print("\n" + "=" * 60)
            print("📖 AUTOMATION DOCUMENTATION")
            print("=" * 60)
            print(content)
            print("=" * 60)
        except Exception as e:
            print(f"❌ Error reading documentation: {e}")
    else:
        print("❌ Documentation file not found")

def check_prerequisites():
    """Check if required tools are available."""
    print("🔍 Checking prerequisites...")
    
    # Check Python
    python_version = sys.version_info
    if python_version.major >= 3 and python_version.minor >= 6:
        print(f"✓ Python {python_version.major}.{python_version.minor} - OK")
    else:
        print(f"❌ Python {python_version.major}.{python_version.minor} - Need Python 3.6+")
        return False
    
    # Check yt-dlp
    try:
        result = subprocess.run(['yt-dlp', '--version'], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            version = result.stdout.strip()
            print(f"✓ yt-dlp {version} - OK")
        else:
            print("❌ yt-dlp not working properly")
            return False
    except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
        print("❌ yt-dlp not found - Install with: pip install yt-dlp")
        return False
    
    # Check JSON file
    json_files = [
        "usul_dirayat_hadis.json",
        "../usul_dirayat_hadis.json",
        "usul_dirayat_hadis/usul_dirayat_hadis.json"
    ]
    
    json_found = False
    for json_file in json_files:
        if os.path.exists(json_file):
            print(f"✓ Found {json_file}")
            json_found = True
            break
    
    if not json_found:
        print("⚠️  usul_dirayat_hadis.json not found in expected locations")
        print("   This is OK for testing, but needed for actual organization")
    
    print("\n✅ Prerequisites check complete!")
    return True

def main():
    """Main menu loop."""
    # Check prerequisites first
    if not check_prerequisites():
        print("\n❌ Prerequisites not met. Please install required tools.")
        return 1
    
    while True:
        print("\n")
        show_menu()
        
        try:
            choice = input("Enter your choice (0-6): ").strip()
            
            if choice == '0':
                print("👋 Goodbye!")
                break
            
            elif choice == '1':
                print("\n🚀 Starting Complete Video Organizer...")
                run_script("complete_video_organizer.py")
            
            elif choice == '2':
                print("\n📋 Starting Playlist Organizer...")
                run_script("auto_playlist_organizer.py")
            
            elif choice == '3':
                print("\n🔧 Starting Video ID Extractor...")
                run_script("extract_video_ids.py")
            
            elif choice == '4':
                print("\n🧪 Running Automation Tests...")
                run_script("test_organizer.py")
            
            elif choice == '5':
                print("\n🎬 Running Automation Demo...")
                run_script("demo_automation.py")
            
            elif choice == '6':
                view_documentation()
            
            else:
                print("❌ Invalid choice. Please enter 0-6.")
        
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())