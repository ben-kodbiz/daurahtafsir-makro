#!/usr/bin/env python3

import json
import os

def create_html_file(session_num, session_data):
    """Create HTML file for a session"""
    
    # Determine if this session has a real video or placeholder
    has_real_video = 'placeholder' not in session_data['youtube_link']
    
    if has_real_video:
        # Extract video ID from YouTube URL
        video_id = None
        if 'watch?v=' in session_data['youtube_link']:
            video_id = session_data['youtube_link'].split('watch?v=')[1].split('&')[0]
        
        video_section = f'''
            <div class="video-container">
                <iframe 
                    src="https://www.youtube.com/embed/{video_id}" 
                    frameborder="0" 
                    allowfullscreen>
                </iframe>
            </div>'''
    else:
        video_section = '''
            <div class="video-container">
                <div class="placeholder-video">
                    <p>Video untuk sesi ini sedang dicari.</p>
                    <p>Sila kembali kemudian atau hubungi pentadbir.</p>
                </div>
            </div>'''
    
    # Navigation buttons
    prev_session = session_num - 1 if session_num > 1 else 1
    next_session = session_num + 1 if session_num < 120 else 120
    prev_disabled = ' style="opacity:0.5; pointer-events:none;"' if session_num == 1 else ''
    next_disabled = ' style="opacity:0.5; pointer-events:none;"' if session_num == 120 else ''
    
    # Topics section
    topics_html = ''
    if 'topics' in session_data and session_data['topics']:
        topics_list = '\n'.join([f'                    <li>{topic}</li>' for topic in session_data['topics']])
        topics_html = f'''
                <div class="topics">
                    <h4>Topik-topik:</h4>
                    <ul>
{topics_list}
                    </ul>
                </div>'''
    
    # Status indicator
    status = "Tersedia" if has_real_video else "Video sedang dicari"
    status_class = "available" if has_real_video else "pending"
    
    html_content = f'''<!DOCTYPE html>
<html lang="ms">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{session_data['title']} - 99 Usul Dirayat Hadis</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="container">
        <header>
            <h1>99 Usul Dirayat Hadis</h1>
            <h2>{session_data['title']}</h2>
        </header>
        
        <main>{video_section}
            
            <div class="session-info">
                <h3>Maklumat Sesi</h3>
                <p><strong>Sesi:</strong> {session_num}</p>
                <p><strong>Tajuk:</strong> {session_data['title']}</p>
                <p><strong>Penceramah:</strong> Maulana Muhammad Asri Yusoff</p>
                <p><strong>Tempoh:</strong> {session_data.get('duration', 'TBD')}</p>
                <p><strong>Status:</strong> <span class="status {status_class}">{status}</span></p>
                
                <div class="description">
                    <h4>Penerangan:</h4>
                    <p>{session_data.get('description', 'Penerangan untuk sesi ini akan dikemaskini.')}</p>
                </div>{topics_html}
            </div>
            
            <div class="navigation">
                <a href="sesi_{prev_session}.html" class="nav-btn prev-btn"{prev_disabled}>← Sesi {prev_session}</a>
                <a href="index.html" class="nav-btn home-btn">Kembali ke Senarai</a>
                <a href="sesi_{next_session}.html" class="nav-btn next-btn"{next_disabled}>Sesi {next_session} →</a>
            </div>
        </main>
    </div>
    
    <script src="script.js"></script>
</body>
</html>'''
    
    return html_content

def create_all_missing_html_files():
    """Create HTML files for all sessions"""
    print("Creating HTML files for all 120 sessions...\n")
    
    # Load JSON data
    with open('../data/usul_dirayat_hadis.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Create a mapping of session numbers to session data
    session_map = {session['session_number']: session for session in data['sessions']}
    
    created_count = 0
    updated_count = 0
    
    for session_num in range(1, 121):
        html_file = f"sesi_{session_num}.html"
        
        if session_num in session_map:
            session_data = session_map[session_num]
            html_content = create_html_file(session_num, session_data)
            
            # Check if file exists and if content needs updating
            file_exists = os.path.exists(html_file)
            
            if not file_exists:
                with open(html_file, 'w', encoding='utf-8') as f:
                    f.write(html_content)
                print(f"Created {html_file}")
                created_count += 1
            else:
                # Check if we need to update existing file (for real videos)
                with open(html_file, 'r', encoding='utf-8') as f:
                    existing_content = f.read()
                
                # Update if it's a placeholder and we now have a real video
                if 'placeholder-video' in existing_content and 'placeholder' not in session_data['youtube_link']:
                    with open(html_file, 'w', encoding='utf-8') as f:
                        f.write(html_content)
                    print(f"Updated {html_file} with real video")
                    updated_count += 1
        else:
            print(f"Warning: No data found for session {session_num}")
    
    print(f"\nCreated {created_count} new HTML files")
    print(f"Updated {updated_count} existing HTML files")
    
    # Verify all files exist
    missing_files = []
    for i in range(1, 121):
        if not os.path.exists(f"sesi_{i}.html"):
            missing_files.append(i)
    
    if missing_files:
        print(f"\nStill missing HTML files for sessions: {missing_files}")
    else:
        print(f"\n✅ All 120 HTML files now exist!")
    
    return created_count, updated_count, len(missing_files)

def verify_html_files():
    """Verify all HTML files are properly created"""
    print("\nVerifying HTML files...")
    
    total_files = 0
    files_with_videos = 0
    files_with_placeholders = 0
    
    for i in range(1, 121):
        html_file = f"sesi_{i}.html"
        if os.path.exists(html_file):
            total_files += 1
            
            with open(html_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if 'placeholder-video' in content:
                files_with_placeholders += 1
            elif 'youtube.com/embed/' in content:
                files_with_videos += 1
    
    print(f"Total HTML files: {total_files}/120")
    print(f"Files with real videos: {files_with_videos}")
    print(f"Files with placeholders: {files_with_placeholders}")
    
    return total_files, files_with_videos, files_with_placeholders

if __name__ == "__main__":
    print("=" * 60)
    print("CREATING ALL HTML FILES")
    print("=" * 60)
    
    # Create all missing HTML files
    created, updated, missing = create_all_missing_html_files()
    
    # Verify the results
    total, with_videos, with_placeholders = verify_html_files()
    
    print("\n" + "=" * 60)
    print("FINAL VERIFICATION")
    print("=" * 60)
    print(f"HTML files created: {created}")
    print(f"HTML files updated: {updated}")
    print(f"Total HTML files: {total}/120")
    print(f"Files with real videos: {with_videos}")
    print(f"Files with placeholders: {with_placeholders}")
    
    if total == 120:
        print("\n🎉 SUCCESS: All 120 HTML files are now available!")
    else:
        print(f"\n⚠️  WARNING: {120 - total} HTML files are still missing")