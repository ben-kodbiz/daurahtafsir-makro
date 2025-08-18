#!/usr/bin/env python3
"""
Channel-specific configuration template
Copy this file and customize for each new channel
"""

# Import base configuration
from config import *

# =============================================================================
# CHANNEL-SPECIFIC CONFIGURATION
# Customize these values for your specific channel
# =============================================================================

# Example configurations for different channels:

# For Usul Dirayat Hadis:
if CHANNEL_NAME == "usul_dirayat_hadis":
    CHANNEL_DISPLAY_NAME = "Usul Dirayat Hadis"
    MAX_SESSIONS = 120
    SESSION_PREFIX = "sesi"
    CHANNEL_URL = "https://www.youtube.com/channel/UC_YOUR_CHANNEL_ID"
    SESSION_PATTERNS = [
        r'(?i)sesi\s*(\d+)',
        r'(?i)usul\s+dirayat\s+hadis\s*(\d+)',
        r'\b(\d+)\s*[-–—]',
        r'\[(\d+)\]',
    ]

# For Jami at-Tirmizi:
elif CHANNEL_NAME == "jami_at_tirmizi":
    CHANNEL_DISPLAY_NAME = "Jami at-Tirmizi"
    MAX_SESSIONS = 143
    SESSION_PREFIX = "sesi"
    CHANNEL_URL = "https://www.youtube.com/channel/UC_YOUR_CHANNEL_ID"
    SESSION_PATTERNS = [
        r'(?i)sesi\s*(\d+)',
        r'(?i)jami\s+at[\s-]?tirmizi\s*(\d+)',
        r'(?i)tirmizi\s*(\d+)',
        r'\b(\d+)\s*[-–—]',
        r'\[(\d+)\]',
    ]

# For Ilal at-Tirmizi:
elif CHANNEL_NAME == "ilal_at_tirmizi":
    CHANNEL_DISPLAY_NAME = "Ilal at-Tirmizi"
    MAX_SESSIONS = 45
    SESSION_PREFIX = "session"
    CHANNEL_URL = "https://www.youtube.com/channel/UC_YOUR_CHANNEL_ID"
    SESSION_PATTERNS = [
        r'(?i)session\s*(\d+)',
        r'(?i)ilal\s+at[\s-]?tirmizi\s*(\d+)',
        r'\b(\d+)\s*[-–—]',
        r'\[(\d+)\]',
    ]

# For Qawaid Tafsir:
elif CHANNEL_NAME == "qawaid_tafsir":
    CHANNEL_DISPLAY_NAME = "Qawaid Tafsir"
    MAX_SESSIONS = 115
    SESSION_PREFIX = "session"
    CHANNEL_URL = "https://www.youtube.com/channel/UC_YOUR_CHANNEL_ID"
    SESSION_PATTERNS = [
        r'(?i)session\s*(\d+)',
        r'(?i)qawaid\s+tafsir\s*(\d+)',
        r'\b(\d+)\s*[-–—]',
        r'\[(\d+)\]',
    ]

# For Sahih Bukhari - Kitab Perang:
elif CHANNEL_NAME == "sahih_bukhari_kitab_perang":
    CHANNEL_DISPLAY_NAME = "Sahih Bukhari - Kitab Perang"
    MAX_SESSIONS = 50
    SESSION_PREFIX = "session"
    CHANNEL_URL = "https://www.youtube.com/channel/UC_YOUR_CHANNEL_ID"
    SESSION_PATTERNS = [
        r'(?i)session\s*(\d+)',
        r'(?i)sahih\s+bukhari\s*(\d+)',
        r'(?i)kitab\s+perang\s*(\d+)',
        r'\b(\d+)\s*[-–—]',
        r'\[(\d+)\]',
    ]

# For Sahih Bukhari - Kitab Azan (Edisi 2):
elif CHANNEL_NAME == "sahih_bukhari_kitab_azan_edisi2":
    CHANNEL_DISPLAY_NAME = "Sahih Bukhari - Kitab Azan (Edisi 2)"
    MAX_SESSIONS = 30
    SESSION_PREFIX = "session"
    CHANNEL_URL = "https://www.youtube.com/channel/UC_YOUR_CHANNEL_ID"
    SESSION_PATTERNS = [
        r'(?i)session\s*(\d+)',
        r'(?i)sahih\s+bukhari\s*(\d+)',
        r'(?i)kitab\s+azan\s*(\d+)',
        r'(?i)edisi\s+2\s*(\d+)',
        r'\b(\d+)\s*[-–—]',
        r'\[(\d+)\]',
    ]

# =============================================================================
# ADVANCED CHANNEL-SPECIFIC SETTINGS
# =============================================================================

# Custom video title cleaning rules for specific channels
CUSTOM_TITLE_CLEANING_RULES = {
    "usul_dirayat_hadis": [
        (r'\s*[-–—]\s*Usul Dirayat Hadis.*$', ''),
        (r'^Usul Dirayat Hadis\s*[-–—]\s*', ''),
        (r'\s*\|.*$', ''),  # Remove everything after |
    ],
    "jami_at_tirmizi": [
        (r'\s*[-–—]\s*Jami at[\s-]?Tirmizi.*$', ''),
        (r'^Jami at[\s-]?Tirmizi\s*[-–—]\s*', ''),
        (r'\s*\|.*$', ''),
    ],
    # Add more channel-specific rules as needed
}

# Custom session detection for specific channels
CUSTOM_SESSION_DETECTION = {
    "usul_dirayat_hadis": {
        "min_session": 1,
        "max_session": 120,
        "strict_range": True,
    },
    "jami_at_tirmizi": {
        "min_session": 1,
        "max_session": 143,
        "strict_range": True,
    },
    # Add more channel-specific detection rules
}

# Custom HTML template mappings
CUSTOM_HTML_TEMPLATES = {
    "usul_dirayat_hadis": "usul_template.html",
    "jami_at_tirmizi": "tirmizi_template.html",
    # Add more template mappings
}

# Channel-specific playlist organization strategies
PLAYLIST_STRATEGIES = {
    "usul_dirayat_hadis": "session_based",  # Group by session numbers
    "jami_at_tirmizi": "sequential",       # Sequential organization
    "qawaid_tafsir": "topic_based",        # Group by topics
    # Add more strategies
}

# =============================================================================
# VALIDATION FUNCTIONS
# =============================================================================

def validate_channel_config():
    """
    Validate the channel configuration
    """
    errors = []
    
    if not CHANNEL_NAME:
        errors.append("CHANNEL_NAME is required")
    
    if not CHANNEL_DISPLAY_NAME:
        errors.append("CHANNEL_DISPLAY_NAME is required")
    
    if MAX_SESSIONS <= 0:
        errors.append("MAX_SESSIONS must be greater than 0")
    
    if not SESSION_PREFIX:
        errors.append("SESSION_PREFIX is required")
    
    if not SESSION_PATTERNS:
        errors.append("At least one SESSION_PATTERN is required")
    
    return errors

def get_channel_config(channel_name):
    """
    Get configuration for a specific channel
    """
    # Set the channel name and reload configuration
    global CHANNEL_NAME
    CHANNEL_NAME = channel_name
    
    # Re-import to apply channel-specific settings
    import importlib
    import sys
    if __name__ in sys.modules:
        importlib.reload(sys.modules[__name__])
    
    return {
        'channel_name': CHANNEL_NAME,
        'display_name': CHANNEL_DISPLAY_NAME,
        'max_sessions': MAX_SESSIONS,
        'session_prefix': SESSION_PREFIX,
        'channel_url': CHANNEL_URL,
        'session_patterns': SESSION_PATTERNS,
        'json_file': JSON_FILE,
        'custom_rules': CUSTOM_TITLE_CLEANING_RULES.get(CHANNEL_NAME, []),
        'detection_config': CUSTOM_SESSION_DETECTION.get(CHANNEL_NAME, {}),
    }

if __name__ == "__main__":
    # Validate configuration when run directly
    errors = validate_channel_config()
    if errors:
        print("Configuration errors:")
        for error in errors:
            print(f"  - {error}")
    else:
        print(f"Configuration for '{CHANNEL_NAME}' is valid!")
        print(f"Display Name: {CHANNEL_DISPLAY_NAME}")
        print(f"Max Sessions: {MAX_SESSIONS}")
        print(f"Session Prefix: {SESSION_PREFIX}")