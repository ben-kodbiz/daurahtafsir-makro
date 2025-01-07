#!/bin/bash

# Define the playlist URL
PLAYLIST_URL="https://www.youtube.com/playlist?list=PLT0mU9DWAEqSohe0zj8MMIlNera_R32U7"

# Use yt-dlp to extract video IDs in JSON format
yt-dlp --flat-playlist --dump-json "$PLAYLIST_URL" | jq -r '.id'
