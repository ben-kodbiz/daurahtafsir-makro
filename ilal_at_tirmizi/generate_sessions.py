#!/usr/bin/env python3
import json
import os

# Read the JSON data
with open('ilal_at_tirmizi.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# HTML template for session pages
html_template = '''<!DOCTYPE html>
<html lang="ms">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} | Ilal at-Tirmizi</title>
    <link rel="stylesheet" href="../styles.css">
    <style>
        .video-container {{
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
        }}
        
        .video-wrapper {{
            position: relative;
            padding-bottom: 56.25%; /* 16:9 aspect ratio */
            height: 0;
            overflow: hidden;
            border-radius: 12px;
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
        }}
        
        .video-wrapper iframe {{
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            border: none;
        }}
        
        .session-info {{
            background: white;
            padding: 30px;
            border-radius: 12px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            margin-top: 20px;
        }}
        
        .session-title {{
            font-size: 2rem;
            font-weight: 700;
            color: #333;
            margin-bottom: 15px;
        }}
        
        .session-description {{
            font-size: 1.1rem;
            color: #666;
            line-height: 1.6;
            margin-bottom: 20px;
        }}
        
        .navigation {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-top: 30px;
        }}
        
        .nav-button {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 12px 24px;
            border: none;
            border-radius: 8px;
            text-decoration: none;
            font-weight: 600;
            transition: transform 0.3s ease;
            display: inline-flex;
            align-items: center;
            gap: 8px;
        }}
        
        .nav-button:hover {{
            transform: translateY(-2px);
        }}
        
        .nav-button.disabled {{
            background: #ccc;
            cursor: not-allowed;
            transform: none;
        }}
        
        @media (max-width: 768px) {{
            .video-container {{
                padding: 15px;
            }}
            
            .session-info {{
                padding: 20px;
            }}
            
            .session-title {{
                font-size: 1.5rem;
            }}
            
            .navigation {{
                flex-direction: column;
                gap: 15px;
            }}
        }}
    </style>
</head>
<body>
    <nav class="navbar">
        <div class="nav-container">
            <div class="nav-logo">
                <a href="../index.html">📚 Daurah Tafsir Makro</a>
            </div>
            <div class="nav-menu">
                <a href="../index.html" class="nav-link">Tafsir Mikro</a>
                <a href="../jami_at_tirmizi/index.html" class="nav-link">Jami at-Tirmizi</a>
                <a href="index.html" class="nav-link active">Ilal at-Tirmizi</a>
            </div>
        </div>
    </nav>

    <div class="video-container">
        <div class="video-wrapper">
            <iframe src="https://www.youtube.com/embed/{video_id}" 
                    allowfullscreen></iframe>
        </div>
        
        <div class="session-info">
            <h1 class="session-title">{title}</h1>
            <p class="session-description">
                {description}
            </p>
            
            <div class="navigation">
                <a href="{prev_link}" class="nav-button{prev_disabled}">
                    {prev_text}
                </a>
                <a href="{next_link}" class="nav-button{next_disabled}">
                    {next_text}
                </a>
            </div>
        </div>
    </div>
</body>
</html>'''

# Generate session files
for session in data['sessions']:
    session_id = session['id']
    title = session['title']
    video_id = session['videoId']
    description = session['description']
    
    # Determine navigation links
    if session_id == 1:
        prev_link = "index.html"
        prev_text = "← Kembali ke Senarai"
        prev_disabled = ""
    else:
        prev_link = f"session{session_id - 1}.html"
        prev_text = f"← Sesi {session_id - 1}"
        prev_disabled = ""
    
    if session_id == len(data['sessions']):
        next_link = "index.html"
        next_text = "Kembali ke Senarai →"
        next_disabled = ""
    else:
        next_link = f"session{session_id + 1}.html"
        next_text = f"Sesi {session_id + 1} →"
        next_disabled = ""
    
    # Generate HTML content
    html_content = html_template.format(
        title=title,
        video_id=video_id,
        description=description,
        prev_link=prev_link,
        prev_text=prev_text,
        prev_disabled=prev_disabled,
        next_link=next_link,
        next_text=next_text,
        next_disabled=next_disabled
    )
    
    # Write to file
    filename = f"session{session_id}.html"
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"Generated {filename}")

print(f"Successfully generated {len(data['sessions'])} session files!")