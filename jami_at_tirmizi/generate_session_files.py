#!/usr/bin/env python3

import json
import os
from pathlib import Path

def load_sessions_data():
    """Load sessions data from JSON file"""
    json_file = "jami_at_tirmizi.json"
    if not os.path.exists(json_file):
        print(f"❌ JSON file {json_file} not found")
        return None
    
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print(f"✅ Loaded {len(data['sessions'])} sessions from {json_file}")
    return data['sessions']

def create_session_html(session):
    """Create HTML content for a session"""
    session_number = session['session_number']
    title = session['title']
    video_id = session['video_id']
    
    html_content = f'''<!DOCTYPE html>
<html lang="en" class="light-theme">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sesi {session_number} – {title}</title>
    <link rel="stylesheet" href="style.css">
    <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://fonts.googleapis.com/icon?family=Material+Icons">
</head>
<body>
    <div class="surah-container">
        <div class="app-bar">
            <a href="index.html" class="back-button">
               <i class="material-icons">arrow_back</i>
                Back
            </a>
             <h1 class="surah-title">Sesi {session_number} – {title}</h1>
            <button class="theme-toggle" onclick="toggleTheme()">
                <i class="material-icons theme-icon">brightness_4</i>
            </button>
        </div>
        <div class="content-area">
                 <h3 class="section-heading">YouTube Videos</h3>
                 <div class="youtube-videos">
                      <iframe width="560" height="315" src="https://www.youtube.com/embed/{video_id}" frameborder="0" allowfullscreen></iframe>
                 </div>
            </div>
        </div>
    </div>
    <script>
        function toggleTheme() {{
            const html = document.documentElement;
            const currentTheme = html.className;
            if (currentTheme === 'light-theme') {{
                html.className = 'dark-theme';
            }} else if (currentTheme === 'dark-theme') {{
                html.className = 'sepia-theme';
            }} else {{
                html.className = 'light-theme';
            }}
        }}
    </script>
</body>
</html>'''
    
    return html_content

def generate_all_session_files(sessions):
    """Generate HTML files for all sessions"""
    print(f"\n🔄 Generating HTML files for {len(sessions)} sessions...")
    
    created_files = []
    
    for session in sessions:
        session_number = session['session_number']
        filename = f"sesi_{session_number}.html"
        
        # Create HTML content
        html_content = create_session_html(session)
        
        # Write to file
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        created_files.append(filename)
        print(f"📄 Created {filename}")
    
    print(f"\n✅ Successfully created {len(created_files)} HTML files")
    return created_files

def main():
    print("🚀 Starting Jami at-Tirmizi session file generation...")
    
    # Load sessions data
    sessions = load_sessions_data()
    if not sessions:
        return False
    
    # Generate session files
    created_files = generate_all_session_files(sessions)
    
    print("\n" + "="*60)
    print("📊 GENERATION REPORT")
    print("="*60)
    print(f"📚 Total Sessions: {len(sessions)}")
    print(f"📄 HTML Files Created: {len(created_files)}")
    print("\n✅ Session file generation completed successfully!")
    print("="*60)
    
    return True

if __name__ == "__main__":
    success = main()
    if not success:
        print("\n❌ Session file generation failed!")
        exit(1)