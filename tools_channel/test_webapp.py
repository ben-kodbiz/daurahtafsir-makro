#!/usr/bin/env python3

import json
import os
import requests
import time
from pathlib import Path

def test_web_application():
    """Test the Usul Dirayat Hadis web application"""
    base_url = "http://localhost:8000"
    
    print("🧪 Testing Usul Dirayat Hadis Web Application")
    print("=" * 50)
    
    # Test 1: Check if JSON data file exists and is valid
    print("\n1. Testing JSON data file...")
    json_path = "../data/usul_dirayat_hadis.json"
    if os.path.exists(json_path):
        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            print(f"   ✅ JSON file loaded successfully")
            print(f"   📊 Total sessions: {data['total_sessions']}")
            print(f"   📝 Title: {data['title']}")
            
            if len(data['sessions']) == 120:
                print(f"   ✅ All 120 sessions present in JSON")
            else:
                print(f"   ⚠️  Expected 120 sessions, found {len(data['sessions'])}")
        except Exception as e:
            print(f"   ❌ Error loading JSON: {e}")
    else:
        print(f"   ❌ JSON file not found at {json_path}")
    
    # Test 2: Check if all HTML files exist
    print("\n2. Testing HTML files...")
    missing_files = []
    for i in range(1, 121):
        html_file = f"sesi_{i}.html"
        if not os.path.exists(html_file):
            missing_files.append(html_file)
    
    if not missing_files:
        print(f"   ✅ All 120 HTML session files exist")
    else:
        print(f"   ❌ Missing {len(missing_files)} HTML files: {missing_files[:5]}...")
    
    # Test 3: Check main files
    print("\n3. Testing main application files...")
    main_files = ['index.html', 'script.js', 'style.css']
    for file in main_files:
        if os.path.exists(file):
            print(f"   ✅ {file} exists")
        else:
            print(f"   ❌ {file} missing")
    
    # Test 4: Test web server accessibility (if running)
    print("\n4. Testing web server accessibility...")
    try:
        response = requests.get(f"{base_url}/usul_dirayat_hadis/", timeout=5)
        if response.status_code == 200:
            print(f"   ✅ Main page accessible (HTTP {response.status_code})")
        else:
            print(f"   ⚠️  Main page returned HTTP {response.status_code}")
        
        # Test JSON endpoint
        json_response = requests.get(f"{base_url}/data/usul_dirayat_hadis.json", timeout=5)
        if json_response.status_code == 200:
            print(f"   ✅ JSON data accessible (HTTP {json_response.status_code})")
        else:
            print(f"   ❌ JSON data not accessible (HTTP {json_response.status_code})")
        
        # Test a few session pages
        test_sessions = [1, 50, 120]
        for session in test_sessions:
            session_response = requests.get(f"{base_url}/usul_dirayat_hadis/sesi_{session}.html", timeout=5)
            if session_response.status_code == 200:
                print(f"   ✅ Session {session} accessible")
            else:
                print(f"   ❌ Session {session} not accessible (HTTP {session_response.status_code})")
                
    except requests.exceptions.ConnectionError:
        print(f"   ⚠️  Web server not running on {base_url}")
        print(f"   💡 Start server with: python3 -m http.server 8000")
    except Exception as e:
        print(f"   ❌ Error testing web server: {e}")
    
    # Test 5: Check video IDs in HTML files
    print("\n5. Testing video IDs in HTML files...")
    valid_videos = 0
    placeholder_videos = 0
    
    for i in range(1, 11):  # Test first 10 sessions
        html_file = f"sesi_{i}.html"
        if os.path.exists(html_file):
            with open(html_file, 'r', encoding='utf-8') as f:
                content = f.read()
                if 'placeholder_video_id' in content:
                    placeholder_videos += 1
                elif 'youtube.com/embed/' in content:
                    valid_videos += 1
    
    print(f"   📊 In first 10 sessions: {valid_videos} with real videos, {placeholder_videos} with placeholders")
    
    print("\n" + "=" * 50)
    print("🎉 Web Application Test Complete!")
    print("\n💡 To access the application:")
    print(f"   🌐 Main page: http://localhost:8000/usul_dirayat_hadis/")
    print(f"   📱 Individual sessions: http://localhost:8000/usul_dirayat_hadis/sesi_[1-120].html")

if __name__ == "__main__":
    test_web_application()