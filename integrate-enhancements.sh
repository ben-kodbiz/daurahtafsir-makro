#!/bin/bash

# Script to integrate enhancements into the main application

echo "Integrating enhancements into the main application..."

# Backup original files
echo "Creating backups of original files..."
cp index.html index.html.backup
cp styles.css styles.css.backup
cp script.js script.js.backup
cp theme.js theme.js.backup

# Create a new enhanced index.html file
cat > index.html << 'EOF'
<!DOCTYPE html>
<html lang="en" class="light-theme">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Quran App</title>
    <link rel="stylesheet" href="styles.css">
    <link rel="stylesheet" href="enhanced-styles.css">
    <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://fonts.googleapis.com/icon?family=Material+Icons">
</head>
<body>
    <select id="language-selector" onchange="setLanguage(this.value)">
        <option value="en">English</option>
        <option value="ms">Malay</option>
    </select>
    <h1 class="main-heading">Daurah Hadis dan Quran oleh Maulana Asri (darul Kautsar)</h1>
    <div class="widget-container">
        <div class="widget current-page enhanced">
            <i class="material-icons widget-icon enhanced">book</i>
            <span class="widget-label enhanced">Tafsir Mikro</span>
        </div>
        <a href="qawaid_tafsir/index.html" class="widget enhanced">
            <i class="material-icons widget-icon enhanced">school</i>
            <span class="widget-label enhanced">Usul Tafsir</span>
        </a>
        <a href="tafsirbilquran/index.html" class="widget enhanced">
            <i class="material-icons widget-icon enhanced">translate</i>
            <span class="widget-label enhanced">Tafsir Quran dengan Quran</span>
        </a>
        <a href="usul_dirayat_hadis/index.html" class="widget enhanced">
            <i class="material-icons widget-icon enhanced">fact_check</i>
            <span class="widget-label enhanced">Usul Dirayat Hadis</span>
        </a>
        <a href="jami_at_tirmizi/index.html" class="widget enhanced">
            <i class="material-icons widget-icon enhanced">library_books</i>
            <span class="widget-label enhanced">Jami at-Tirmizi (Kitab Thaharah)</span>
        </a>
        <a href="ilal_at_tirmizi/index.html" class="widget enhanced">
            <i class="material-icons widget-icon enhanced">error_outline</i>
            <span class="widget-label enhanced">Ilal at-Tirmizi</span>
        </a>
        <a href="sahih_bukhari_kitab_perang/index.html" class="widget enhanced">
            <i class="material-icons widget-icon enhanced">military_tech</i>
            <span class="widget-label enhanced">Sahih Bukhari-Kitab Perang</span>
        </a>
        <a href="sahih_bukhari_kitab_azan_edisi2/index.html" class="widget enhanced">
            <i class="material-icons widget-icon enhanced">campaign</i>
            <span class="widget-label enhanced">Sahih Bukhari-Kitab Azan(edisi2)</span>
        </a>
    </div>
    <div class="device-warning">
        <i class="material-icons">smartphone</i>
        <span>Mobile optimized version. Enjoy your learning experience!</span>
    </div>

    <div class="search-container enhanced">
        <div class="search-box enhanced">
            <i class="material-icons search-icon enhanced">search</i>
            <input type="text" id="surah-search" class="enhanced" placeholder="Search for surah by name or number..." />
            <button id="clear-search" class="clear-search-btn enhanced">
                <i class="material-icons">close</i>
            </button>
        </div>
    </div>

    <div class="surah-grid enhanced" id="surah-grid">
    </div>

    <script src="script.js?v=1755482400"></script>
    <script src="enhanced-script.js"></script>
    <script src="enhanced-theme.js"></script>
    <div class="theme-toggle-container">
        <button class="theme-toggle" onclick="toggleTheme()">
            <i class="material-icons theme-icon">brightness_4</i>
        </button>
    </div>
</body>
</html>
EOF

echo "Integration complete!"
echo ""
echo "Enhancements have been integrated into the main application."
echo "Backups of original files have been created with .backup extension."
echo ""
echo "To test the enhanced version:"
echo "1. Open index.html in your browser"
echo "2. The application now has improved mobile support and enhanced Material Design components"
echo ""
echo "To revert to the original version:"
echo "1. Restore the backup files:"
echo "   mv index.html.backup index.html"
echo "   mv styles.css.backup styles.css"
echo "   mv script.js.backup script.js"
echo "   mv theme.js.backup theme.js"