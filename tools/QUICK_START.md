# 🎬 Channel Processing Tools - Quick Start Guide

This document demonstrates how to use the channel processing tools to add new modules to the Daurah Tafsir Makro application.

## 🚀 Quick Example

### 1. Process a New Channel

```bash
# Navigate to the tools directory
cd /data/work/dev/daurahtafsir-makro/tools

# Process a YouTube channel to create a new module
./process_channel.sh https://www.youtube.com/@example-channel \\
    --name \"Sahih Bukhari - Kitab Solat\" \\
    --description \"Kajian terperinci tentang Kitab Solat dari koleksi hadis Sahih Bukhari\" \\
    --output ../sahih_bukhari_kitab_solat \\
    --max-videos 50
```

### 2. Add Module to Main Application

After processing, add the new module to the main `index.html`:

```html
<a href=\"sahih_bukhari_kitab_solat/index.html\" class=\"widget enhanced\">
    <i class=\"material-icons widget-icon enhanced\">mosque</i>
    <span class=\"widget-label enhanced\">Sahih Bukhari-Kitab Solat</span>
</a>
```

## 📋 Detailed Usage

### Basic Command Structure

```bash
./process_channel.sh <CHANNEL_URL> --name <MODULE_NAME> --description <DESCRIPTION>
```

### All Options

| Option | Description | Example |
|--------|-------------|---------|
| `--output <dir>` | Output directory for generated files | `--output ../my_module` |
| `--max-videos <n>` | Maximum number of videos to process | `--max-videos 100` |
| `--config <file>` | Custom configuration file | `--config my_config.ini` |

### Example with All Options

```bash
./process_channel.sh https://www.youtube.com/@islamic-lectures \\
    --name \"Fiqh of Worship\" \\
    --description \"Comprehensive study of worship jurisprudence\" \\
    --output ../fiqh_worship \\
    --max-videos 75 \\
    --config ./example_config.ini
```

## 📁 Generated Output

The tool creates a complete module with:

```
output_directory/
├── index.html              # Main page with searchable session grid
├── session1.html           # First video session
├── session2.html           # Second video session
├── ...                     # Additional sessions
├── channel_data.json       # Structured session data
├── video_data.txt          # Video ID to title mapping
└── ytid.txt               # Simple list of video IDs
```

## ⚙️ Customization

### Configuration File

Modify `config.ini` to change:

- Rate limiting settings
- Title cleaning patterns
- File naming conventions
- Template settings

### Example Custom Config

```ini
[YOUTUBE]
request_delay = 5.0    # Increase delay for sensitive channels
max_videos = 100       # Limit videos for smaller modules

[OUTPUT]
max_title_length = 60  # Shorter titles for mobile
```

## 🛠️ Utility Scripts

### Interactive Menu

```bash
./utils.sh
```

Provides a menu for:
- Processing new channels
- Checking video counts
- Listing existing modules
- And more...

### Direct Tool Usage

```bash
# Run processor directly
python3 channel_processor.py <CHANNEL_URL> --name \"Module\" --description \"Desc\"
```

## ✅ Verification

After processing, verify the output:

```bash
# Check generated files
ls -la ../output_directory/

# Test a session file
head -20 ../output_directory/session1.html

# Verify JSON structure
jq . ../output_directory/channel_data.json
```

## 📞 Need Help?

For issues or questions:

1. Check the detailed README: `cat README.md`
2. Run the interactive utility: `./utils.sh`
3. View tool help: `./process_channel.sh --help`

The tools are designed to be robust and adaptable for any Islamic lecture channel on YouTube.