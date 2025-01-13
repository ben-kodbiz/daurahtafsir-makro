#!/bin/bash

# Define the playlist URL
PLAYLIST_URL="https://www.youtube.com/playlist?list=PLT0mU9DWAEqSX7OiG-892dZvjsCuAVghN"

# Use yt-dlp to extract video IDs in JSON format
yt-dlp --flat-playlist --dump-json "$PLAYLIST_URL" | jq -r '.id' >> ytidtafsirquran
