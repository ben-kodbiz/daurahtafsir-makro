#!/usr/bin/env python3
"""
Configuration file for channel deployment automation tools
Modify these variables for different channels
"""

# Channel Information
CHANNEL_NAME = "your_channel_name"  # e.g., "usul_dirayat_hadis"
CHANNEL_DISPLAY_NAME = "Your Channel Display Name"  # e.g., "Usul Dirayat Hadis"
CHANNEL_URL = "https://www.youtube.com/channel/YOUR_CHANNEL_ID"  # YouTube channel URL

# Session Configuration
MAX_SESSIONS = 120  # Maximum number of sessions for this channel
SESSION_PREFIX = "sesi"  # Prefix for session files (e.g., "sesi", "session")
SESSION_START_NUMBER = 1  # Starting session number

# File Paths
JSON_FILE = f"{CHANNEL_NAME}.json"  # Main JSON data file
INDEX_FILE = "index.html"  # Main index file
STYLE_FILE = "style.css"  # CSS file
SCRIPT_FILE = "script.js"  # JavaScript file

# Video Detection Patterns
SESSION_PATTERNS = [
    r'(?i)sesi\s*(\d+)',
    r'(?i)session\s*(\d+)',
    r'(?i)part\s*(\d+)',
    r'(?i)episode\s*(\d+)',
    r'(?i)ep\s*(\d+)',
    r'\b(\d+)\s*[-–—]',
    r'\[(\d+)\]',
    r'(?i)' + CHANNEL_NAME.replace('_', '\\s+') + r'\s*(\d+)',
]

# YouTube API Configuration (if needed)
YOUTUBE_API_KEY = ""  # Optional: YouTube API key for enhanced features

# Playlist URLs (for playlist-based organization)
PLAYLIST_URLS = [
    # Add your playlist URLs here
    # "https://www.youtube.com/playlist?list=PLxxxxx",
    # "https://www.youtube.com/playlist?list=PLyyyyy",
]

# Output Configuration
VERBOSE_OUTPUT = True  # Enable detailed output
GENERATE_REPORTS = True  # Generate detailed reports
UPDATE_HTML_FILES = True  # Update HTML files automatically

# Theme Configuration
DEFAULT_THEME = "light"  # Default theme: "light", "dark", "sepia"
ENABLE_THEME_TOGGLE = True  # Enable theme switching

# Search Configuration
ENABLE_SEARCH = True  # Enable search functionality
SEARCH_FIELDS = ["title", "description", "id"]  # Fields to search in

# Backup Configuration
CREATE_BACKUPS = True  # Create backups before modifications
BACKUP_DIR = "backups"  # Backup directory

# Error Handling
CONTINUE_ON_ERROR = True  # Continue processing on non-critical errors
MAX_RETRIES = 3  # Maximum retries for failed operations

# Logging Configuration
LOG_LEVEL = "INFO"  # Log level: DEBUG, INFO, WARNING, ERROR
LOG_FILE = f"{CHANNEL_NAME}_automation.log"  # Log file name

# Template Configuration
HTML_TEMPLATE_DIR = "templates"  # Directory containing HTML templates
USE_CUSTOM_TEMPLATES = False  # Use custom templates if available

# Advanced Configuration
PARALLEL_PROCESSING = False  # Enable parallel processing (experimental)
CACHE_VIDEO_DATA = True  # Cache video data for faster processing
CACHE_EXPIRY_HOURS = 24  # Cache expiry time in hours