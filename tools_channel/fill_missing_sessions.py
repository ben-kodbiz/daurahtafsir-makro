#!/usr/bin/env python3

import json
import os

def analyze_missing_sessions():
    """Analyze which sessions are missing and need placeholders"""
    print("Analyzing missing sessions...\n")
    
    # Load session mapping
    with open('session_mapping.json', 'r', encoding='utf-8') as f:
        session_mapping = json.load(f)
    
    # Convert string keys to integers
    mapped_sessions = set(int(k) for k in session_mapping.keys() if k.isdigit() and 1 <= int(k) <= 120)
    
    # Find missing sessions
    all_sessions = set(range(1, 121))
    missing_sessions = sorted(all_sessions - mapped_sessions)
    
    print(f"Sessions with videos: {len(mapped_sessions)}")
    print(f"Missing sessions: {len(missing_sessions)}")
    print(f"Mapped sessions: {sorted(mapped_sessions)}")
    print(f"\nMissing sessions: {missing_sessions}")
    
    return missing_sessions, mapped_sessions

def create_placeholder_content(session_num):
    """Create placeholder content for missing sessions"""
    return {
        "session_number": session_num,
        "title": f"Sesi {session_num} – Usul Dirayat Hadis",
        "description": f"Sesi {session_num} dalam siri 99 Usul Dirayat Hadis oleh Maulana Muhammad Asri Yusoff. Video untuk sesi ini sedang dicari.",
        "youtube_link": "https://www.youtube.com/watch?v=placeholder",
        "duration": "TBD",
        "topics": [
            f"Usul {session_num} dalam mengenal hadis"
        ]
    }

def update_json_with_placeholders():
    """Update JSON file to ensure all 120 sessions exist"""
    print("\nUpdating JSON file with placeholders for missing sessions...")
    
    # Load current JSON
    with open('../data/usul_dirayat_hadis.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Get current session numbers
    current_sessions = {session['session_number'] for session in data['sessions']}
    
    # Add missing sessions
    missing_sessions, _ = analyze_missing_sessions()
    added_count = 0
    
    for session_num in missing_sessions:
        if session_num not in current_sessions:
            placeholder = create_placeholder_content(session_num)
            data['sessions'].append(placeholder)
            added_count += 1
            print(f"Added placeholder for session {session_num}")
    
    # Sort sessions by session number
    data['sessions'].sort(key=lambda x: x['session_number'])
    
    # Update total count
    data['total_sessions'] = len(data['sessions'])
    
    # Save updated JSON
    with open('../data/usul_dirayat_hadis.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"\nAdded {added_count} placeholder sessions")
    print(f"Total sessions now: {len(data['sessions'])}")
    
    return added_count

def create_missing_html_files():
    """Create HTML files for missing sessions"""
    print("\nCreating HTML files for missing sessions...")
    
    missing_sessions, _ = analyze_missing_sessions()
    created_count = 0
    
    # HTML template for missing sessions
    html_template = '''<!DOCTYPE html>
<html lang="ms">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sesi {session_num} - 99 Usul Dirayat Hadis</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="container">
        <header>
            <h1>99 Usul Dirayat Hadis</h1>
            <h2>Sesi {session_num}</h2>
        </header>
        
        <main>
            <div class="video-container">
                <div class="placeholder-video">
                    <p>Video untuk sesi ini sedang dicari.</p>
                    <p>Sila kembali kemudian atau hubungi pentadbir.</p>
                </div>
            </div>
            
            <div class="session-info">
                <h3>Maklumat Sesi</h3>
                <p><strong>Sesi:</strong> {session_num}</p>
                <p><strong>Tajuk:</strong> Sesi {session_num} – Usul Dirayat Hadis</p>
                <p><strong>Penceramah:</strong> Maulana Muhammad Asri Yusoff</p>
                <p><strong>Status:</strong> Video sedang dicari</p>
            </div>
            
            <div class="navigation">
                <a href="sesi_{prev_session}.html" class="nav-btn prev-btn"{prev_disabled}>← Sesi Sebelumnya</a>
                <a href="index.html" class="nav-btn home-btn">Kembali ke Senarai</a>
                <a href="sesi_{next_session}.html" class="nav-btn next-btn"{next_disabled}>Sesi Seterusnya →</a>
            </div>
        </main>
    </div>
    
    <script src="script.js"></script>
</body>
</html>'''
    
    for session_num in missing_sessions:
        html_file = f"sesi_{session_num}.html"
        
        if not os.path.exists(html_file):
            prev_session = session_num - 1 if session_num > 1 else 1
            next_session = session_num + 1 if session_num < 120 else 120
            prev_disabled = ' style="display:none;"' if session_num == 1 else ''
            next_disabled = ' style="display:none;"' if session_num == 120 else ''
            
            html_content = html_template.format(
                session_num=session_num,
                prev_session=prev_session,
                next_session=next_session,
                prev_disabled=prev_disabled,
                next_disabled=next_disabled
            )
            
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            print(f"Created {html_file}")
            created_count += 1
    
    print(f"\nCreated {created_count} HTML files")
    return created_count

def generate_summary_report():
    """Generate a summary report of the current state"""
    print("\n" + "=" * 60)
    print("FINAL SUMMARY REPORT")
    print("=" * 60)
    
    missing_sessions, mapped_sessions = analyze_missing_sessions()
    
    # Check HTML files
    html_files_exist = 0
    for i in range(1, 121):
        if os.path.exists(f"sesi_{i}.html"):
            html_files_exist += 1
    
    # Load JSON to check total sessions
    with open('../data/usul_dirayat_hadis.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    sessions_with_real_videos = len(mapped_sessions)
    sessions_with_placeholders = len(missing_sessions)
    total_json_sessions = len(data['sessions'])
    
    print(f"Total sessions in JSON: {total_json_sessions}/120")
    print(f"Sessions with real videos: {sessions_with_real_videos}")
    print(f"Sessions with placeholders: {sessions_with_placeholders}")
    print(f"HTML files created: {html_files_exist}/120")
    
    print(f"\nSessions with real videos: {sorted(mapped_sessions)}")
    
    if len(missing_sessions) <= 20:
        print(f"\nSessions still missing videos: {missing_sessions}")
    else:
        print(f"\nFirst 20 sessions missing videos: {missing_sessions[:20]}")
        print(f"... and {len(missing_sessions)-20} more")
    
    completion_percentage = (sessions_with_real_videos / 120) * 100
    print(f"\nCompletion: {completion_percentage:.1f}% ({sessions_with_real_videos}/120 sessions)")
    
    return {
        'total_sessions': total_json_sessions,
        'real_videos': sessions_with_real_videos,
        'placeholders': sessions_with_placeholders,
        'html_files': html_files_exist,
        'completion_percentage': completion_percentage
    }

if __name__ == "__main__":
    print("=" * 60)
    print("FILLING MISSING SESSIONS")
    print("=" * 60)
    
    # Analyze current state
    missing_sessions, mapped_sessions = analyze_missing_sessions()
    
    # Update JSON with placeholders
    json_updates = update_json_with_placeholders()
    
    # Create missing HTML files
    html_created = create_missing_html_files()
    
    # Generate final report
    summary = generate_summary_report()
    
    print("\nProcess completed!")