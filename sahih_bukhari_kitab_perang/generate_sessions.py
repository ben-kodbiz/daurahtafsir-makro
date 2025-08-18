#!/usr/bin/env python3
import json
import os

def generate_session_html(session_data, total_sessions):
    session_id = session_data['id']
    title = session_data['title']
    video_id = session_data['videoId']
    description = session_data['description']
    
    # Navigation logic
    prev_link = f'./session{session_id - 1}.html' if session_id > 1 else '#'
    next_link = f'./session{session_id + 1}.html' if session_id < total_sessions else '#'
    
    prev_disabled = 'disabled' if session_id == 1 else ''
    next_disabled = 'disabled' if session_id == total_sessions else ''
    
    html_content = f'''<!DOCTYPE html>
<html lang="ms">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} - Sahih Bukhari Kitab Perang</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }}

        .container {{
            max-width: 1000px;
            margin: 0 auto;
            background: rgba(255, 255, 255, 0.95);
            border-radius: 20px;
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
            overflow: hidden;
        }}

        .header {{
            background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }}

        .header h1 {{
            font-size: 2rem;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
        }}

        .header p {{
            font-size: 1.1rem;
            opacity: 0.9;
        }}

        .navigation {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 20px 30px;
            background: #f8f9fa;
            border-bottom: 1px solid #e9ecef;
        }}

        .nav-button {{
            padding: 12px 24px;
            background: linear-gradient(135deg, #3498db 0%, #2980b9 100%);
            color: white;
            text-decoration: none;
            border-radius: 25px;
            font-weight: 600;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(52, 152, 219, 0.3);
        }}

        .nav-button:hover {{
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(52, 152, 219, 0.4);
        }}

        .nav-button.disabled {{
            background: #bdc3c7;
            cursor: not-allowed;
            box-shadow: none;
        }}

        .nav-button.disabled:hover {{
            transform: none;
        }}

        .back-link {{
            background: linear-gradient(135deg, #95a5a6 0%, #7f8c8d 100%);
            box-shadow: 0 4px 15px rgba(149, 165, 166, 0.3);
        }}

        .video-container {{
            padding: 30px;
            text-align: center;
        }}

        .video-wrapper {{
            position: relative;
            width: 100%;
            height: 0;
            padding-bottom: 56.25%; /* 16:9 aspect ratio */
            margin-bottom: 20px;
            border-radius: 15px;
            overflow: hidden;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
        }}

        .video-wrapper iframe {{
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            border: none;
        }}

        .video-title {{
            font-size: 1.3rem;
            font-weight: 600;
            color: #2c3e50;
            margin-bottom: 10px;
        }}

        .video-description {{
            color: #7f8c8d;
            font-size: 1rem;
            line-height: 1.6;
        }}

        @media (max-width: 768px) {{
            body {{
                padding: 10px;
            }}

            .header {{
                padding: 20px;
            }}

            .header h1 {{
                font-size: 1.6rem;
            }}

            .navigation {{
                flex-direction: column;
                gap: 15px;
                padding: 20px;
            }}

            .nav-button {{
                padding: 10px 20px;
                font-size: 0.9rem;
            }}

            .video-container {{
                padding: 20px;
            }}

            .video-title {{
                font-size: 1.1rem;
            }}
        }}

        @media (max-width: 480px) {{
            .header h1 {{
                font-size: 1.4rem;
            }}

            .header p {{
                font-size: 1rem;
            }}

            .navigation {{
                padding: 15px;
            }}

            .video-container {{
                padding: 15px;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>{title}</h1>
            <p>Sahih Bukhari - Kitab Perang</p>
        </div>
        
        <div class="navigation">
            <a href="./index.html" class="nav-button back-link">← Senarai Sesi</a>
            <div>
                <a href="{prev_link}" class="nav-button {prev_disabled}">← Sesi Sebelumnya</a>
                <a href="{next_link}" class="nav-button {next_disabled}">Sesi Seterusnya →</a>
            </div>
        </div>
        
        <div class="video-container">
            <div class="video-wrapper">
                <iframe 
                    src="https://www.youtube.com/embed/{video_id}" 
                    title="{title}"
                    allowfullscreen>
                </iframe>
            </div>
            
            <div class="video-title">{title}</div>
            <div class="video-description">
                {description}
            </div>
        </div>
    </div>
</body>
</html>'''
    
    return html_content

def main():
    # Load the JSON data
    with open('sahih_bukhari_kitab_perang.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    sessions = data['sessions']
    total_sessions = len(sessions)
    
    print(f"Generating {total_sessions} session files...")
    
    # Generate HTML files for each session
    for session in sessions:
        session_id = session['id']
        filename = f"session{session_id}.html"
        
        html_content = generate_session_html(session, total_sessions)
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"Generated {filename}")
    
    print(f"Successfully generated all {total_sessions} session files!")

if __name__ == "__main__":
    main()