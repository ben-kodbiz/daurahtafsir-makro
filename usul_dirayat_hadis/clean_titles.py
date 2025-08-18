#!/usr/bin/env python3
"""
Script to clean up and improve the session titles by removing redundancy
and making them more concise and readable.
"""

import json
import re
from pathlib import Path

def clean_title(session_number, current_title):
    """
    Clean and improve a session title
    """
    # Extract the part after "Sesi X – "
    title_match = re.match(r'Sesi \d+ – (.+)', current_title)
    if not title_match:
        return current_title
    
    content = title_match.group(1).strip()
    
    # Remove redundant session numbers at the beginning
    content = re.sub(r'^Sesi \d+\s*[-–]?\s*', '', content)
    
    # Remove common prefixes and suffixes
    content = re.sub(r'\[LIVE\]\s*', '', content, flags=re.IGNORECASE)
    content = re.sub(r'Maulana\s+(Muhammad\s+)?Asri\s+Yusoff\s*:?\s*', '', content, flags=re.IGNORECASE)
    content = re.sub(r'99\s*(Mengenal\s+)?Hadis?\s*(Palsu\s*(dan?\s*|&\s*)?Dhaif)?\s*:?\s*', '', content, flags=re.IGNORECASE)
    content = re.sub(r'99\s*Dalam\s+Mengenal\s+Hadith\s+Palsu\s*&\s*Dhaif\s*', '', content, flags=re.IGNORECASE)
    
    # Remove bracketed references at the end
    content = re.sub(r'\s*-?\s*\[USUL\s+DIRAYAT\s*HADIS?[-–]?Usul\s+\d+\]\s*$', '', content, flags=re.IGNORECASE)
    content = re.sub(r'\s*-?\s*\[Usul\s+\d+\]\s*$', '', content, flags=re.IGNORECASE)
    content = re.sub(r'\s*-?\s*\[PALSU\]\s*', '', content, flags=re.IGNORECASE)
    
    # Clean up specific patterns
    content = re.sub(r'Hadith?\s+', 'Hadis ', content, flags=re.IGNORECASE)
    content = re.sub(r'\s*-\s*\[.*?\]\s*$', '', content)  # Remove trailing brackets
    
    # Remove extra dashes and clean up
    content = re.sub(r'^[-–]\s*', '', content)
    content = re.sub(r'\s*[-–]\s*$', '', content)
    content = re.sub(r'\s+', ' ', content)
    content = content.strip()
    
    # Handle specific cases
    if 'Takrif Ma\'nawi' in content:
        content = 'Hadis Mengandungi Penyelewengan Makna (Takrif Ma\'nawi)'
    elif 'Canggah Akal Yang Sihat' in content:
        content = 'Hadis yang Bertentangan dengan Akal Sehat'
    elif 'Kelebihan Setiap Surah' in content:
        content = 'Hadis Kelebihan Setiap Surah dalam Al-Quran'
    elif 'Puji Kehidupan Membujang' in content:
        content = 'Hadis Palsu tentang Kelebihan Hidup Membujang'
    elif 'Kelebihan Orang Yang Bernama Muhammad' in content:
        content = 'Hadis tentang Kelebihan Nama Muhammad'
    elif 'Kelebihan orang yang berwajah cantik' in content:
        content = 'Hadis Palsu tentang Kelebihan Wajah Cantik'
    elif 'Mencela Sesuatu Pekerjaan' in content:
        content = 'Hadis Maudhu\' tentang Mencela Pekerjaan'
    elif 'Riwayat Khadir' in content and 'Sahabat Nabi' in content:
        content = 'Riwayat Palsu Khadir Berjumpa Sahabat Nabi'
    elif 'Riwayat Khadir' in content and 'Umur Panjang' in content:
        content = 'Riwayat Palsu tentang Umur Panjang Khadir'
    elif 'Kitab Tafsir Maudhu\'i' in content:
        content = 'Kitab Tafsir Maudhu\'i dan Polemik Keberadaan Allah'
    
    # Ensure proper capitalization
    if content and len(content) > 0:
        content = content[0].upper() + content[1:] if len(content) > 1 else content.upper()
    
    # Return cleaned title
    return f"Sesi {session_number} – {content}" if content else f"Sesi {session_number} – Usul Dirayat Hadis"

def clean_all_titles():
    """
    Clean all titles in the JSON file
    """
    json_file = Path('/data/work/dev/daurahtafsir-makro/data/usul_dirayat_hadis.json')
    
    # Load the JSON data
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    cleaned_count = 0
    
    print("Cleaning session titles...")
    
    for i, session in enumerate(data['sessions']):
        session_num = session['session_number']
        current_title = session['title']
        
        # Clean the title
        new_title = clean_title(session_num, current_title)
        
        # Update if changed
        if new_title != current_title:
            data['sessions'][i]['title'] = new_title
            cleaned_count += 1
            print(f"Session {session_num}: {new_title}")
    
    # Save the updated JSON
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"\nCleaned {cleaned_count} session titles.")
    return cleaned_count

def update_html_files():
    """
    Update HTML files with cleaned titles
    """
    json_file = Path('/data/work/dev/daurahtafsir-makro/data/usul_dirayat_hadis.json')
    html_dir = Path('/data/work/dev/daurahtafsir-makro/usul_dirayat_hadis')
    
    # Load the updated JSON data
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    updated_html_count = 0
    
    for session in data['sessions']:
        session_num = session['session_number']
        title = session['title']
        
        html_file = html_dir / f'sesi_{session_num}.html'
        
        if html_file.exists():
            # Read the HTML file
            with open(html_file, 'r', encoding='utf-8') as f:
                html_content = f.read()
            
            # Update the title in HTML
            # Update page title
            html_content = re.sub(
                r'<title>.*?</title>',
                f'<title>{title}</title>',
                html_content
            )
            
            # Update h1 title
            html_content = re.sub(
                r'<h1>.*?</h1>',
                f'<h1>{title}</h1>',
                html_content
            )
            
            # Write back the updated HTML
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            updated_html_count += 1
    
    print(f"Updated {updated_html_count} HTML files with cleaned titles.")
    return updated_html_count

if __name__ == '__main__':
    print("Starting title cleaning process...")
    
    # Clean JSON titles
    json_updates = clean_all_titles()
    
    # Update HTML files
    html_updates = update_html_files()
    
    print(f"\nSummary:")
    print(f"- Cleaned {json_updates} session titles in JSON")
    print(f"- Updated {html_updates} HTML files")
    print(f"\nTitle cleaning process completed!")