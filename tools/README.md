# 📺 Channel Processing Tools

A collection of versatile tools for processing YouTube channels and creating web modules for the Daurah Tafsir Makro application.

## 📁 Directory Structure

```
tools/
├── config.ini              # Centralized configuration file
├── channel_processor.py    # Main Python processing script
├── process_channel.sh      # Shell script wrapper
└── README.md              # This documentation
```

## 🚀 Quick Start

### Prerequisites

1. Python 3.x
2. yt-dlp (`pip install yt-dlp`)

### Basic Usage

```bash
# Process a YouTube channel
./tools/process_channel.sh https://www.youtube.com/@channel \\
    --name \"Module Name\" \\
    --description \"Description of the module\"
```

### Advanced Usage

```bash
# Process with custom output directory and limits
./tools/process_channel.sh https://www.youtube.com/@channel \\
    --name \"Module Name\" \\
    --description \"Description of the module\" \\
    --output ./mymodule \\
    --max-videos 50
```

## 📋 Features

### 1. Video Extraction
- Extracts video IDs and titles from YouTube channels
- Respects rate limits to avoid blocking
- Handles large playlists efficiently

### 2. File Generation
- **Session Files**: Generates individual HTML files for each video
- **Index File**: Creates main index with searchable session grid
- **JSON Data**: Generates structured data for sessions
- **Video Data**: Creates mapping file with video IDs and titles
- **YTID File**: Generates simple list of video IDs

### 3. Smart Processing
- **Title Cleaning**: Automatically cleans video titles for better display
- **Navigation**: Adds \"Previous\" and \"Next\" buttons between sessions
- **Responsive Design**: Mobile-friendly layouts
- **Theme Support**: Light, dark, and sepia themes

## ⚙️ Configuration

The `config.ini` file contains all configurable settings:

### Default Settings
```ini
[DEFAULT]
output_dir = ./output
session_template = session_template.html
index_template = index_template.html
video_data_file = video_data.txt
ytid_file = ytid.txt
json_file = channel_data.json
```

### YouTube Settings
```ini
[YOUTUBE]
yt_dlp_path = yt-dlp
max_videos = 200
request_delay = 3.5
```

### Templates
```ini
[TEMPLATES]
session_title_prefix = Sesi
session_title_separator = \" - \"
session_description_template = Kandungan untuk {session_title} dalam modul {module_name}.
```

### Output Formatting
```ini
[OUTPUT]
title_clean_patterns = [\"\\\\[.*?\\\\]\", \"Sesi \\\\d+ -\", \"sesi \\\\d+ -\"]
title_clean_replacements = [\"\", \"\", \"\"]
max_title_length = 100
```

### Naming Conventions
```ini
[NAMING]
session_file_pattern = session{number}.html
index_file = index.html
```

## 🛠️ Customization

### Adding New Modules

1. **Create a new module**:
```bash
./tools/process_channel.sh https://www.youtube.com/@newchannel \\
    --name \"New Module Name\" \\
    --description \"Description of the new module\" \\
    --output ../new_module_directory
```

2. **Update main application**:
Add link to new module in `index.html`:
```html
<a href=\"new_module_directory/index.html\" class=\"widget enhanced\">
    <i class=\"material-icons widget-icon enhanced\">icon_name</i>
    <span class=\"widget-label enhanced\">New Module Name</span>
</a>
```

### Modifying Templates

1. Edit the HTML templates in `channel_processor.py`
2. Update the configuration in `config.ini`
3. Run the processor to regenerate files

## 📊 Output Structure

The tool generates the following files:

```
output/
├── index.html              # Main module page with session grid
├── session1.html           # First session file
├── session2.html           # Second session file
├── ...                     # Additional session files
├── channel_data.json       # JSON data with session information
├── video_data.txt          # Video IDs and titles mapping
└── ytid.txt               # Simple list of video IDs
```

## 🔧 Troubleshooting

### Common Issues

1. **yt-dlp not found**:
   ```bash
   pip install yt-dlp
   ```

2. **Permission denied**:
   ```bash
   chmod +x ./tools/process_channel.sh
   ```

3. **Python not found**:
   Install Python 3.x from python.org

### Rate Limiting

The tool automatically adds delays between requests to avoid:
- YouTube API rate limits
- IP blocking
- Request timeouts

## 🔄 Maintenance

### Updating the Tool

1. Pull the latest version from the repository
2. Update `config.ini` if needed
3. Test with a small channel before processing large ones

### Adding Features

1. Modify `channel_processor.py` for new functionality
2. Update `config.ini` for new settings
3. Test thoroughly before deployment

## 📞 Support

For issues or feature requests, please contact the development team.

## 📄 License

This tool is part of the Daurah Tafsir Makro project and is licensed under the same terms.