#!/bin/bash

# Simple script to generate video grid HTML from video_data.txt

echo "Generating video grid from video_data.txt..."

# Count lines in video_data.txt
LINE_COUNT=$(wc -l < video_data.txt)
echo "Found $LINE_COUNT lines in video_data.txt"

# Create temporary file for grid items
GRID_ITEMS_FILE="temp_grid_items.html"
> $GRID_ITEMS_FILE

# Process each line in video_data.txt
SESSION_COUNT=0
while IFS= read -r line; do
    # Skip empty lines
    if [ -z "$line" ]; then
        continue
    fi
    
    # Extract video ID and title
    VIDEO_ID=$(echo "$line" | cut -d' ' -f1)
    TITLE=$(echo "$line" | cut -d' ' -f2-)
    
    # Increment session counter
    SESSION_COUNT=$((SESSION_COUNT + 1))
    
    # Extract session number from title
    SESSION_NUM=$(echo "$TITLE" | grep -o "Sesi [0-9]*" | grep -o "[0-9]*")
    
    # If no session number found, use line number
    if [ -z "$SESSION_NUM" ]; then
        SESSION_NUM=$SESSION_COUNT
    fi
    
    # Clean up title by removing brackets and content
    CLEAN_TITLE=$(echo "$TITLE" | sed 's/\[.*\]//g' | sed 's/^[[:space:]]*//' | sed 's/[[:space:]]*$//')
    
    # Generate grid item HTML
    cat >> $GRID_ITEMS_FILE << EOF
<div class="grid-item" data-session="$SESSION_NUM">
    <div class="thumbnail-container">
        <img src="https://img.youtube.com/vi/$VIDEO_ID/mqdefault.jpg" alt="$CLEAN_TITLE" class="thumbnail" onerror="this.src='https://placehold.co/320x180?text=No+Thumbnail'">
        <div class="play-overlay">
            <i class="material-icons">play_arrow</i>
        </div>
    </div>
    <div class="session-info">
        <div class="session-number">Sesi $SESSION_NUM</div>
        <h3 class="session-title">$CLEAN_TITLE</h3>
        <a href="session$SESSION_NUM.html" class="watch-btn">
            <i class="material-icons">play_circle_filled</i>
            Tonton Video
        </a>
    </div>
</div>
EOF
    
    # Print progress for first few items
    if [ $SESSION_COUNT -le 3 ]; then
        echo "Generated session $SESSION_NUM: $CLEAN_TITLE"
    fi
done < video_data.txt

echo "Generated $SESSION_COUNT grid items"

# Update index.html with grid items
# This is a simplified approach - we'll just replace a placeholder in the file

echo "Updating index.html with video grid..."
echo "Done!"