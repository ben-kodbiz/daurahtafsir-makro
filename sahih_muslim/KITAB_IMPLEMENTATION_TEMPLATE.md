# Kitab Implementation Template

This template provides guidelines for implementing new Kitab in the Sahih Muslim module.

## Directory Structure
```
sahih_muslim_kitab_[KITAB_NAME]/
├── index.html                 # Main grid view page
├── session1.html              # Individual session pages
├── session2.html
├── ...
├── channel_data.json          # Session data in JSON format
├── video_data.txt             # Video ID and title mapping
└── ytid.txt                   # Simple list of YouTube IDs
```

## Implementation Steps

### 1. Create Directory
```bash
mkdir -p sahih_muslim_kitab_[KITAB_NAME]
```

### 2. Process YouTube Channel
Use the channel processing tools to generate the initial structure:
```bash
cd /data/work/dev/daurahtafsir-makro/tools
./process_channel.sh <YOUTUBE_CHANNEL_URL> \
  --name "Kitab [KITAB_NAME]" \
  --description "Kitab [KITAB_NAME] from Sahih Muslim series" \
  --output "../sahih_muslim/sahih_muslim_kitab_[KITAB_NAME]"
```

### 3. Enhance Grid View
After processing, enhance the grid view with Material Design styling by:
- Replacing the basic grid with the enhanced Material Design grid (copy from Kitab Muqaddimah)
- Adding YouTube thumbnails for each session
- Including session chips with numbering
- Adding play overlays and hover effects

### 4. Verify Implementation
- Test all session pages to ensure videos load correctly
- Verify search functionality works
- Check theme switching (light/dark mode)
- Test responsive design on different screen sizes
- Ensure navigation back to main Sahih Muslim page works

### 5. Update Tracking
Update the KITAB_TRACKING.md file with the implementation status:
```bash
cd /data/work/dev/daurahtafsir-makro/sahih_muslim
./update_tracking.sh [KITAB_NUMBER] completed [SESSION_COUNT] "All sessions processed"
```

## Required Components

### index.html
- Enhanced Material Design grid view with thumbnails
- Search functionality
- Theme support
- Back navigation to main Sahih Muslim page
- Session data with video IDs for thumbnail generation

### Session Pages
- Embedded YouTube videos
- Navigation to previous/next sessions
- Consistent styling with the rest of the application
- Responsive design

### Data Files
- `channel_data.json` - JSON data with session information
- `video_data.txt` - Video ID and title mapping
- `ytid.txt` - Simple list of YouTube video IDs

## Best Practices

1. **Consistency**: Follow the same styling and structure as existing Kitab
2. **Performance**: Optimize images and minimize CSS/JS
3. **Accessibility**: Ensure proper alt text and semantic HTML
4. **Responsive Design**: Test on various screen sizes
5. **Error Handling**: Provide fallbacks for missing thumbnails
6. **Documentation**: Update README.md with implementation details

## Example Command Sequence

```bash
# Create directory
mkdir -p sahih_muslim_kitab_iman

# Process channel (example)
cd /data/work/dev/daurahtafsir-makro/tools
./process_channel.sh https://www.youtube.com/@example-channel \
  --name "Kitab Iman" \
  --description "Kitab Iman from Sahih Muslim series" \
  --output "../sahih_muslim/sahih_muslim_kitab_iman"

# Enhance grid view (manually update index.html with Material Design styling)

# Update tracking
cd /data/work/dev/daurahtafsir-makro/sahih_muslim
./update_tracking.sh 2 completed 25 "All sessions processed"
```

## Quality Assurance Checklist

- [ ] All session pages load correctly
- [ ] YouTube videos embed properly
- [ ] Search functionality works
- [ ] Theme switching functions
- [ ] Responsive design tested
- [ ] Back navigation works
- [ ] Session navigation (prev/next) works
- [ ] Thumbnails display correctly
- [ ] Error handling for missing thumbnails
- [ ] Consistent styling with other modules
- [ ] Tracking document updated
- [ ] README.md updated