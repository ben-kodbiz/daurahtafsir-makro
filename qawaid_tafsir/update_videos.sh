#!/bin/bash

# Script to update all Usul Tafsir (Qawaid Tafsir) session files with actual YouTube video IDs

echo "Updating Usul Tafsir session files with actual YouTube video IDs..."

# Read video IDs from ytidtafsirquran into an array
mapfile -t video_ids < ytidtafsirquran

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
    
    # Update the session file with the actual video ID
    sed -i "s/VIDEO_ID_FOR_SESSION_$i/$video_id/g" "session_$i.html"
    sed -i "s/VIDEO_ID_FOR_SESSION_[0-9]*/$video_id/g" "session_$i.html"
done

echo "All Usul Tafsir session files have been updated with actual YouTube video IDs!"