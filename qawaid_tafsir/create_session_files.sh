#!/bin/zsh

# Ensure required files exist
if [[ ! -f "../data/tutorial_sessions.json" ]]; then
  echo "Error: JSON data file '../data/tutorial_sessions.json' not found!"
  exit 1
fi

if [[ ! -f "ytid.txt" ]]; then
  echo "Error: YouTube IDs file 'ytid.txt' not found!"
  exit 1
fi

# HTML template
template=$(cat <<'EOF'
<!DOCTYPE html>
<html lang="en" class="light-theme">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Surah {{sessionTitle}} - Quran App</title>
    <link rel="stylesheet" href="../styles.css">
    <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://fonts.googleapis.com/icon?family=Material+Icons">
</head>
<body>
    <div class="surah-container">
        <div class="app-bar">
            <a href="../index.html" class="back-button">
               <i class="material-icons">arrow_back</i>
                Back
            </a>
             <h1 class="surah-title">Surah {{sessionTitle}}</h1>
            <button class="theme-toggle" onclick="toggleTheme()">
                <i class="material-icons theme-icon">brightness_4</i>
            </button>
        </div>
        <div class="content-area">
             <h3 class="section-heading">Other Materials</h3>
                 <div class="other-materials">
                     <iframe src="{{pdfLink}}" width="100%" height="400" style="border:none;"></iframe>
                     <a href="{{pdfLink}}" target="_blank" class="download-button">Download PDF Explanation</a>
                </div>
                 <h3 class="section-heading">YouTube Videos</h3>
                 <div class="youtube-videos">
                      <iframe width="560" height="315" src="{{youtubeLink}}" frameborder="0" allowfullscreen></iframe>
                 </div>
            </div>
        </div>
    </div>
    <script src="../theme.js"></script>
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

# Load JSON data
json_data=$(cat "../data/tutorial_sessions.json")
if [[ -z "$json_data" ]]; then
  echo "Error: JSON data is empty!"
  exit 1
fi

# Read YouTube IDs into an array
youtube_ids=()
while IFS= read -r line; do
  youtube_ids+=("$line")
done < "ytid.txt"

# Ensure there are sessions to process
session_count=$(echo "$json_data" | jq '.sessions | length')
if (( session_count == 0 )); then
  echo "Error: No sessions found in the JSON data."
  exit 1
fi

# Loop through each session
i=1 # Zsh arrays are 1-based
while IFS= read -r session; do
  session_number=$(echo "$session" | jq -r '.session_number')
  session_title=$(echo "$session" | jq -r '.title')
  pdf_link=$(echo "$session" | jq -r '.pdf_link')

  # Validate YouTube ID availability
  if (( i > ${#youtube_ids[@]} )); then
    echo "Error: Not enough YouTube IDs in 'ytid.txt' for session $session_number."
    exit 1
  fi

  youtube_id=${youtube_ids[i]}
  youtube_link="https://www.youtube.com/embed/${youtube_id}"

  # Create the filename
  filename="session_${session_number}.html"

  # Replace placeholders and create the file
  echo "$template" | sed \
    -e "s/{{sessionTitle}}/${session_title}/g" \
    -e "s|{{pdfLink}}|${pdf_link}|g" \
    -e "s|{{youtubeLink}}|${youtube_link}|g" > "$filename"

  echo "Created file: $filename"
  ((i++))
done < <(echo "$json_data" | jq -c '.sessions[]')

echo "All session files created successfully."
