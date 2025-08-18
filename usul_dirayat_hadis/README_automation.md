# Automated Video Organization for Usul Dirayat Hadis

This directory contains automated scripts to organize videos into playlists by session numbers and extract video IDs correctly for placement in sessions.

## Scripts Overview

### 1. `complete_video_organizer.py` (Recommended)
The main comprehensive script that automates the entire process:
- Extracts videos from YouTube playlists and/or channels
- Automatically groups videos by session numbers using intelligent pattern matching
- Selects the best video when multiple videos are found for the same session
- Updates the JSON file and HTML files
- Provides detailed reports

### 2. `auto_playlist_organizer.py`
Focused on playlist organization:
- Extracts videos from multiple YouTube playlists
- Groups videos by detected session numbers
- Updates the main JSON file

### 3. `extract_video_ids.py`
Utility for manual video management:
- Extracts videos from channels, playlists, or search results
- Saves videos to JSON for manual review and assignment
- Applies manual assignments to the main JSON file

## Quick Start Guide

### Prerequisites
```bash
# Install yt-dlp if not already installed
pip install yt-dlp
```

### Method 1: Fully Automated (Recommended)

1. **Prepare your playlists**: Group your videos into YouTube playlists by session numbers
   - Create playlists like "Usul Dirayat Hadis Sessions 1-20", "Sessions 21-40", etc.
   - Ensure video titles contain session numbers (e.g., "Sesi 1", "Session 15")

2. **Run the complete organizer**:
   ```bash
   cd usul_dirayat_hadis
   python3 complete_video_organizer.py
   ```

3. **Choose option 1** (YouTube playlists) and enter your playlist URLs

4. **Review the results** - the script will:
   - Extract all videos from your playlists
   - Automatically detect session numbers
   - Update `usul_dirayat_hadis.json`
   - Update all HTML files
   - Show a detailed report

### Method 2: Channel-Based Extraction

1. **Run the complete organizer**:
   ```bash
   python3 complete_video_organizer.py
   ```

2. **Choose option 2** (YouTube channel) and enter the channel URL

3. **Set maximum videos** to extract (recommended: 300)

### Method 3: Mixed Sources

1. **Run the complete organizer**:
   ```bash
   python3 complete_video_organizer.py
   ```

2. **Choose option 3** (Mixed sources)

3. **Enter playlist URLs** first, then the channel URL

## Manual Fine-Tuning

If some videos aren't automatically matched:

1. **Extract videos for manual review**:
   ```bash
   python3 extract_video_ids.py
   ```

2. **Choose your extraction method** (channel, playlist, or search)

3. **Review the generated JSON file** (e.g., `extracted_videos_150.json`)

4. **Manually assign sessions** by editing the `assigned_session` field:
   ```json
   {
     "video_id": "abc123def45",
     "title": "Some Video Title",
     "detected_session": null,
     "youtube_url": "https://www.youtube.com/watch?v=abc123def45",
     "assigned_session": 25  // Add this manually
   }
   ```

5. **Apply manual assignments**:
   ```bash
   python3 extract_video_ids.py
   # Choose option 4 and provide the path to your edited JSON file
   ```

## Session Number Detection

The scripts can detect session numbers from various title formats:
- `Sesi 1`, `Sesi 15`
- `Session 1`, `Session 15`
- `1 - Topic Name`
- `[1] Topic Name`
- `Part 1`, `Episode 1`
- `Usul Dirayat Hadis 1`
- And many more patterns

## Best Practices

### For Playlist Organization:
1. **Group videos logically** - create playlists that group sessions sequentially
2. **Use clear titles** - ensure video titles contain session numbers
3. **Verify playlist order** - videos should be in the correct sequence

### For Channel Extraction:
1. **Set appropriate limits** - don't extract too many irrelevant videos
2. **Use keyword filtering** - filter results by relevant keywords
3. **Review before applying** - always check the extracted videos

### For Manual Assignment:
1. **Start with automatic detection** - let the script do most of the work
2. **Focus on edge cases** - manually assign only problematic videos
3. **Double-check assignments** - verify session numbers are correct

## Troubleshooting

### Common Issues:

1. **"yt-dlp not found"**:
   ```bash
   pip install yt-dlp
   ```

2. **"HTTP Error 403"**:
   - This is normal for some videos (age-restricted, private, etc.)
   - The script will continue with other videos

3. **"No videos extracted"**:
   - Check if the playlist/channel URL is correct
   - Ensure the playlist is public
   - Try with a different playlist/channel

4. **"Videos not matching sessions"**:
   - Check if video titles contain session numbers
   - Use manual assignment for problematic videos
   - Consider updating the session detection patterns

### Performance Tips:

1. **Use playlists when possible** - they're faster and more accurate
2. **Limit channel extraction** - set reasonable maximum video limits
3. **Run in batches** - process large collections in smaller chunks

## Output Files

- `usul_dirayat_hadis.json` - Updated with new video links and titles
- `session_*.html` - All HTML files updated with new video IDs
- `extracted_videos_*.json` - Temporary files for manual review
- Console output with detailed progress and reports

## Example Workflow

```bash
# 1. Organize your videos into playlists on YouTube
# 2. Run the complete organizer
python3 complete_video_organizer.py

# 3. Choose option 1 (playlists)
# 4. Enter your playlist URLs:
# https://www.youtube.com/playlist?list=PLxxxxx (Sessions 1-30)
# https://www.youtube.com/playlist?list=PLyyyyy (Sessions 31-60)
# https://www.youtube.com/playlist?list=PLzzzzz (Sessions 61-90)
# (empty line to finish)

# 5. Review the report and check updated files
# 6. If needed, use extract_video_ids.py for manual fine-tuning
```

This automated approach should significantly reduce the manual work required to organize your video collection!