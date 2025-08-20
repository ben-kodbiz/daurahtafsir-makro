#!/bin/bash

# Script to update all Sahih Muslim Kitab Haji session files with actual YouTube video IDs

echo "Updating Sahih Muslim Kitab Haji session files with actual YouTube video IDs..."

# Read video IDs from ytid.txt into an array
mapfile -t video_ids < ytid.txt

# Get the total number of sessions
TOTAL_SESSIONS=${#video_ids[@]}

echo "Found $TOTAL_SESSIONS video IDs"

# Update each session file
for i in $(seq 1 $TOTAL_SESSIONS); do
    # Calculate array index (0-based)
    index=$((i - 1))
    
    # Get the video ID for this session
    video_id=${video_ids[$index]}
    
    echo "Updating session_$i.html with video ID: $video_id"
    
    # Update the session file with the actual video ID by replacing the YouTube embed URL
    sed -i "s|youtube.com/embed/[a-zA-Z0-9_-]*|youtube.com/embed/$video_id|g" "session_$i.html"
done

echo "All Sahih Muslim Kitab Haji session files have been updated with actual YouTube video IDs!"