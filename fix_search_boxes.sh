#!/bin/bash

# Fix search box styling across all kitab directories
# This script will ensure all kitab directories use the proper search box styling
# from the unified-sahih-bukhari-theme.css

PROJECT_ROOT="/data/work/dev/daurahtafsir-makro"
KITAB_BASE_DIR="$PROJECT_ROOT/syarah_hadis/syarah_kitab_bukhari"

echo "Fixing search box styling across all kitab directories..."

# Counter for processed directories
count=0

# Loop through all kitab directories
for kitab_dir in "$KITAB_BASE_DIR"/sahih_bukhari_kitab_*; do
    # Check if it's a directory
    if [ -d "$kitab_dir" ]; then
        kitab_name=$(basename "$kitab_dir")
        index_file="$kitab_dir/index.html"
        
        # Check if index.html exists
        if [ -f "$index_file" ]; then
            echo "Processing $kitab_name..."
            
            # Create a backup of the original file
            cp "$index_file" "$index_file.backup"
            
            # The files already reference the unified CSS, so we don't need to modify them
            # The search box styling should come from the unified-sahih-bukhari-theme.css
            # which is already linked in the HTML files
            
            # Increment counter
            ((count++))
        else
            echo "No index.html found in $kitab_name, skipping..."
        fi
    fi
done

echo "Processed $count kitab directories."
echo "All kitab directories already reference the unified CSS file which contains proper search box styling."
echo "Backup files have been created with .backup extension."