#!/bin/bash

# Script to extract YouTube video IDs for Usul Dirayat Hadis series
# This script will search for videos containing "Usul Dirayat" or "99 Usul" from Yufid.TV channel

echo "Extracting video IDs for Usul Dirayat Hadis series..."

# Method 1: Try to extract from a specific playlist if it exists
# PLAYLIST_URL="https://www.youtube.com/playlist?list=PLAYLIST_ID_HERE"

# Method 2: Extract from channel search for specific keywords
CHANNEL_URL="https://www.youtube.com/channel/UCX-4mrOc5r691SzDhHtkOgw"

# Create output file
OUTPUT_FILE="usul_dirayat_video_ids.txt"
> "$OUTPUT_FILE"

echo "Searching for Usul Dirayat Hadis videos on Yufid.TV channel..."

# Search for videos with "Usul Dirayat" in the title from the channel
yt-dlp --flat-playlist --dump-json "ytsearch100:Usul Dirayat Hadis Yufid" | jq -r 'select(.title | test("Usul|99 Usul|Dirayat"; "i")) | .id' >> "$OUTPUT_FILE"

# Alternative: Search specifically for "99 Usul" series
yt-dlp --flat-playlist --dump-json "ytsearch50:99 Usul Untuk Mengenal Pasti Hadith Yufid" | jq -r 'select(.title | test("99 Usul|Sesi"; "i")) | .id' >> "$OUTPUT_FILE"

# Remove duplicates
sort "$OUTPUT_FILE" | uniq > "${OUTPUT_FILE}.tmp" && mv "${OUTPUT_FILE}.tmp" "$OUTPUT_FILE"

echo "Video IDs extracted to: $OUTPUT_FILE"
echo "Total videos found: $(wc -l < "$OUTPUT_FILE")"

# Display first few video IDs
echo "First 10 video IDs:"
head -10 "$OUTPUT_FILE"