#!/usr/bin/env python3
import json

# Generate complete JSON with 120 sessions
data = {
    "app_name": "Usul Dirayat Hadis",
    "sessions": []
}

# Session titles for first 20 sessions with specific topics
specific_titles = [
    "Pengenalan Usul Dirayat Hadis",
    "Sejarah dan Perkembangan Ilmu Hadis", 
    "Klasifikasi Hadis Berdasarkan Sanad",
    "Klasifikasi Hadis Berdasarkan Matan",
    "Metodologi Kritik Hadis",
    "Ilmu Rijal al-Hadis",
    "Jarh wa Ta'dil",
    "Tabaqat al-Ruwat",
    "Ilal al-Hadis",
    "Hadis Mu'allaq",
    "Hadis Mursal",
    "Hadis Munqati'",
    "Hadis Mu'dal",
    "Hadis Mudallas",
    "Hadis Maqlub",
    "Hadis Mudraj",
    "Hadis Maqtu'",
    "Hadis Mauquf",
    "Hadis Marfu'",
    "Hadis Musnad"
]

# Generate all 120 sessions
for i in range(1, 121):
    if i <= 20:
        title = f"Sesi {i} – {specific_titles[i-1]}"
    else:
        title = f"Sesi {i} – Usul Dirayat Hadis"
    
    session = {
        "session_number": i,
        "title": title,
        "youtube_link": f"placeholder{i}"
    }
    data["sessions"].append(session)

# Write to file
with open('/data/work/dev/daurahtafsir-makro/data/usul_dirayat_hadis.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=4, ensure_ascii=False)

print(f"Generated complete JSON file with {len(data['sessions'])} sessions")