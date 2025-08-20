#!/bin/bash

# Script to update all session files across modules to use the unified Sahih Bukhari theme

echo "Updating session files to use unified Sahih Bukhari theme..."

# Function to update session files in a directory
update_session_files() {
    local dir=$1
    local module_name=$2
    
    echo "Updating session files in $dir..."
    
    # Find all HTML files in the directory (excluding index.html)
    find "$dir" -name "*.html" -not -name "index.html" | while read -r file; do
        # Get the filename without path
        filename=$(basename "$file")
        
        # Create backup
        cp "$file" "${file}.backup"
        
        # Update the file with unified theme
        cat > "$file" << EOF
<!DOCTYPE html>
<html lang="ms" class="light-theme">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>$module_name - $filename</title>
    <link rel="stylesheet" href="../unified-sahih-bukhari-theme.css">
    <link rel="stylesheet" href="https://fonts.googleapis.com/icon?family=Material+Icons">
</head>
<body>
    <div class="tutorial-container">
        <a href="index.html" class="back-link">
            <i class="material-icons">arrow_back</i>
            Back to $module_name
        </a>
        <div class="header">
            <h1>$module_name - $filename</h1>
        </div>
        <div class="video-container">
            <div class="video-wrapper">
                <!-- Video will be loaded here -->
            </div>
            <div class="video-info">
                <div class="video-title">$module_name - $filename</div>
                <div class="video-description">
                    Video content for $filename in $module_name module.
                </div>
                <a href="index.html" class="watch-btn">Back to Sessions</a>
            </div>
        </div>
    </div>
    <script>
        function toggleTheme() {
            const html = document.documentElement;
            const currentTheme = html.className;
            if (currentTheme === 'light-theme') {
                html.className = 'dark-theme';
            } else if (currentTheme === 'dark-theme') {
                html.className = 'sepia-theme';
            } else {
                html.className = 'light-theme';
            }
        }
    </script>
</body>
</html>
EOF
    done
    
    echo "Completed updating session files in $dir"
}

# Update session files in each module
update_session_files "qawaid_tafsir" "Usul Tafsir"
update_session_files "tafsirbilquran" "Tafsir Quran dengan Quran"
update_session_files "usul_dirayat_hadis" "Usul Dirayat Hadis"
update_session_files "sahih_bukhari_kitab_perang" "Sahih Bukhari - Kitab Perang"
update_session_files "ilal_at_tirmizi" "Ilal at-Tirmizi"
update_session_files "jami_at_tirmizi" "Jami at-Tirmizi - Kitab Thaharah"

echo "All session files have been updated to use the unified Sahih Bukhari theme!"
echo "Backups of original files have been created with .backup extension."