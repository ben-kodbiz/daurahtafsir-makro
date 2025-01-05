#!/bin/bash

# HTML template
template=$(cat <<EOF
<!DOCTYPE html>
<html lang="en" class="light-theme">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Surah {{surahName}} - Quran App</title>
    <link rel="stylesheet" href="styles.css">
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
             <h1 class="surah-title">Surah {{surahName}}</h1>
            <button class="theme-toggle" onclick="toggleTheme()">
                <i class="material-icons theme-icon">brightness_4</i>
            </button>
        </div>
        <div class="content-area">
             <h3 class="section-heading">Other Materials</h3>
                 <div class="other-materials">
                     <iframe src="pdfs/1.-surah-al-fatihah.pdf" width="100%" height="400" style="border:none;"></iframe>
                     <a href="pdfs/1.-surah-al-fatihah.pdf" target="_blank" class="download-button">Download PDF Explanation</a>
                </div>
                 <h3 class="section-heading">YouTube Videos</h3>
                 <div class="youtube-videos">
                    
                      <iframe width="560" height="315" src="https://www.youtube.com/embed/dQw4w9WgXcQ" frameborder="0" allowfullscreen></iframe>
                     
                 
                 </div>
            </div>
        </div>
    </div>
    <script>
    function toggleTheme() {
        document.documentElement.classList.toggle('dark-theme');
        document.documentElement.classList.toggle('light-theme');
    }
    </script>
</body>
</html>
EOF
)

# Loop from 1 to 114
for i in $(seq 1 114); do
  # Create the filename
  filename="surah_${i}.html"

  # Create the file and add content
  echo "$template" | sed \
      -e "s/{{surahName}}/Surah ${i}/g" \
      -e "s/{{imageSrc}}/images\/surah_${i}.webp/g" \
      > "$filename"

  echo "Created file: $filename"
done

echo "All surah files created."