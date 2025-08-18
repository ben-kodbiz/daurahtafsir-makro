# Channel Automation Tools

This directory contains all the automation tools and scripts used for deploying and managing different channels in the Daurah Tafsir project. These tools have been consolidated from various channel directories to provide a centralized toolkit for future channel deployments.

## 📁 Directory Structure

```
tools_channel/
├── README.md                     # This documentation file
├── config.py                     # Main configuration file
├── channel_config_template.py    # Template for channel-specific configs
├── deployment_config.py          # Deployment and environment settings
├── Python Scripts/
│   ├── automation_tools.py       # Core automation utilities
│   ├── channel_video_extractor.py # YouTube video extraction
│   ├── complete_video_organizer.py # Video organization and processing
│   ├── auto_playlist_organizer.py # Playlist management
│   ├── demo_automation.py        # Demo and testing utilities
│   ├── generate_session_files.py # Session file generation
│   ├── generate_azan_sessions.py # Azan session generation
│   └── generate_complete_json.py # JSON file generation
└── Shell Scripts/
    ├── extract_video_ids.sh      # Extract video IDs from playlists
    ├── generate_json.sh          # Generate JSON files
    ├── generate_sessions.sh      # Generate session files
    ├── change_pdf.sh             # PDF management
    ├── create_session_files.sh   # Create session files
    ├── yt-id.sh                  # YouTube ID utilities
    ├── rempdf.sh                 # Remove PDF files
    ├── session.sh                # Session management
    └── createsurah.sh            # Surah creation utilities
```

## 🚀 Quick Start

### 1. Setting Up a New Channel

1. **Copy the channel configuration template:**
   ```bash
   cp channel_config_template.py your_channel_config.py
   ```

2. **Edit the configuration file:**
   ```python
   # Edit your_channel_config.py
   CHANNEL_NAME = "Your Channel Name"
   CHANNEL_ID = "your_channel_id"
   PLAYLIST_ID = "your_playlist_id"
   # ... customize other settings
   ```

3. **Run the automation tools:**
   ```bash
   python3 automation_tools.py --config your_channel_config.py
   ```

### 2. Environment Setup

1. **Configure deployment settings:**
   ```python
   # Edit deployment_config.py
   ENVIRONMENT = "development"  # or "staging", "production"
   SERVER_HOST = "localhost"
   SERVER_PORT = 8000
   ```

2. **Install dependencies (if needed):**
   ```bash
   pip install yt-dlp requests beautifulsoup4
   ```

## 🛠️ Configuration Files

### config.py
Main configuration file containing default settings for:
- Channel information
- Session settings
- File paths and naming conventions
- Video detection patterns
- HTML generation settings

### channel_config_template.py
Template for creating channel-specific configurations:
- Channel metadata
- Custom title cleaning rules
- Session detection patterns
- HTML templates
- Playlist organization strategies

### deployment_config.py
Deployment and environment settings:
- Server configuration
- Security settings
- Monitoring and logging
- Backup and recovery
- Performance optimization

## 📋 Available Tools

### Python Scripts

#### automation_tools.py
Core automation utilities for channel management.
```bash
python3 automation_tools.py --channel "Channel Name" --playlist "playlist_id"
```

#### channel_video_extractor.py
Extracts video information from YouTube channels and playlists.
```bash
python3 channel_video_extractor.py --url "https://youtube.com/playlist?list=..."
```

#### complete_video_organizer.py
Organizes videos into sessions and generates HTML files.
```bash
python3 complete_video_organizer.py --config your_channel_config.py
```

#### auto_playlist_organizer.py
Automatically organizes playlists and generates navigation.
```bash
python3 auto_playlist_organizer.py --playlist-id "your_playlist_id"
```

#### generate_session_files.py
Generates individual session HTML files.
```bash
python3 generate_session_files.py --sessions-data sessions.json
```

#### generate_complete_json.py
Generates comprehensive JSON files with all channel data.
```bash
python3 generate_complete_json.py --channel-dir "/path/to/channel"
```

### Shell Scripts

#### extract_video_ids.sh
Extracts video IDs from YouTube playlists.
```bash
./extract_video_ids.sh "playlist_url" > video_ids.txt
```

#### generate_json.sh
Generates JSON files from video data.
```bash
./generate_json.sh "channel_directory"
```

#### generate_sessions.sh
Generates session files from templates.
```bash
./generate_sessions.sh "sessions_data.json"
```

#### create_session_files.sh
Creates session files with proper formatting.
```bash
./create_session_files.sh "channel_name" "session_count"
```

## 🔧 Usage Examples

### Example 1: Setting Up "Usul Dirayat Hadis" Channel

```python
# Create usul_dirayat_config.py
CHANNEL_NAME = "Usul Dirayat Hadis"
CHANNEL_ID = "UC..."
PLAYLIST_ID = "PL..."
SESSION_PREFIX = "Sesi"
TITLE_CLEANING_RULES = [
    (r'Sesi \d+[:\s]*', ''),
    (r'\s*-\s*Ustadz.*', ''),
]
```

```bash
# Run automation
python3 automation_tools.py --config usul_dirayat_config.py
```

### Example 2: Setting Up "Jami at-Tirmizi" Channel

```python
# Create jami_tirmizi_config.py
CHANNEL_NAME = "Jami at-Tirmizi (Kitab Thaharah)"
CHANNEL_ID = "UC..."
PLAYLIST_ID = "PL..."
SESSION_PREFIX = "Hadis"
CUSTOM_SESSION_DETECTION = r'(?:Hadis|Bab)\s*(\d+)'
```

```bash
# Extract videos and organize
python3 channel_video_extractor.py --config jami_tirmizi_config.py
python3 complete_video_organizer.py --config jami_tirmizi_config.py
```

### Example 3: Batch Processing Multiple Channels

```bash
#!/bin/bash
# batch_deploy.sh

channels=("usul_dirayat" "jami_tirmizi" "qawaid_tafsir")

for channel in "${channels[@]}"; do
    echo "Processing $channel..."
    python3 automation_tools.py --config "${channel}_config.py"
    echo "$channel completed!"
done
```

## 🎯 Best Practices

### 1. Configuration Management
- Always create a separate config file for each channel
- Use descriptive names for configuration files
- Keep sensitive information (API keys) in environment variables
- Validate configuration before running automation

### 2. File Organization
- Follow consistent naming conventions
- Use the same directory structure across channels
- Keep backups of important files
- Use version control for configuration files

### 3. Error Handling
- Always check script output for errors
- Use logging to track automation progress
- Implement retry mechanisms for network operations
- Validate generated files before deployment

### 4. Performance Optimization
- Use batch processing for large datasets
- Implement caching for repeated operations
- Monitor resource usage during automation
- Use parallel processing when appropriate

## 🔍 Troubleshooting

### Common Issues

#### 1. YouTube Extraction Fails
```bash
# Update yt-dlp
pip install --upgrade yt-dlp

# Check if URL is accessible
curl -I "https://youtube.com/playlist?list=..."
```

#### 2. Session Detection Not Working
```python
# Debug session detection patterns
import re
pattern = r'Sesi\s*(\d+)'
test_title = "Sesi 1: Introduction"
match = re.search(pattern, test_title)
print(f"Match: {match.group(1) if match else 'No match'}")
```

#### 3. HTML Generation Issues
```bash
# Check template files
ls -la templates/

# Validate HTML output
python3 -m http.server 8000
# Open http://localhost:8000 in browser
```

#### 4. Permission Issues
```bash
# Fix script permissions
chmod +x *.sh

# Check directory permissions
ls -la ../
```

### Debug Mode

Enable debug mode in your configuration:
```python
DEBUG_MODE = True
VERBOSE_LOGGING = True
```

Or run with debug flags:
```bash
python3 automation_tools.py --debug --verbose
```

## 📊 Monitoring and Logging

### Log Files
- `automation.log` - Main automation log
- `errors.log` - Error-specific log
- `performance.log` - Performance metrics

### Monitoring Commands
```bash
# Watch logs in real-time
tail -f logs/automation.log

# Check for errors
grep -i error logs/*.log

# Monitor disk usage
du -sh */
```

## 🔄 Maintenance

### Regular Tasks
1. **Update dependencies:**
   ```bash
   pip install --upgrade yt-dlp requests beautifulsoup4
   ```

2. **Clean up temporary files:**
   ```bash
   find . -name "*.tmp" -delete
   find . -name "__pycache__" -type d -exec rm -rf {} +
   ```

3. **Backup configurations:**
   ```bash
   tar -czf configs_backup_$(date +%Y%m%d).tar.gz *_config.py
   ```

4. **Update documentation:**
   - Keep this README updated with new tools
   - Document any custom modifications
   - Update examples with real use cases

## 📞 Support

For issues or questions:
1. Check the troubleshooting section above
2. Review log files for error details
3. Validate your configuration files
4. Test with a small dataset first

## 📝 Contributing

When adding new tools:
1. Follow the existing naming conventions
2. Add configuration options to the template
3. Update this README with usage examples
4. Include error handling and logging
5. Test with multiple channel types

---

**Note:** This toolkit is designed to be flexible and extensible. Each channel may have unique requirements, so feel free to customize the configuration files and scripts as needed.