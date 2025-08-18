#!/usr/bin/env python3
"""
Deployment Configuration for Channel Automation Tools
Settings for deployment, hosting, and production environments
"""

# =============================================================================
# DEPLOYMENT ENVIRONMENT SETTINGS
# =============================================================================

# Environment Configuration
ENVIRONMENT = "development"  # Options: "development", "staging", "production"
DEBUG_MODE = True  # Enable debug mode for development

# Server Configuration
SERVER_HOST = "localhost"
SERVER_PORT = 8000
SERVER_PROTOCOL = "http"  # "http" or "https"

# Base URLs for different environments
BASE_URLS = {
    "development": f"{SERVER_PROTOCOL}://{SERVER_HOST}:{SERVER_PORT}",
    "staging": "https://staging.yourdomain.com",
    "production": "https://yourdomain.com"
}

# =============================================================================
# FILE PATHS AND DIRECTORIES
# =============================================================================

# Project Structure
PROJECT_ROOT = "/data/work/dev/daurahtafsir-makro"
TOOLS_DIR = "tools_channel"
TEMPLATES_DIR = "templates"
STATIC_DIR = "static"
BACKUP_DIR = "backups"
LOGS_DIR = "logs"

# Output Directories
OUTPUT_DIRS = {
    "html": ".",  # HTML files in channel root
    "json": ".",  # JSON files in channel root
    "css": ".",   # CSS files in channel root
    "js": ".",    # JavaScript files in channel root
    "assets": "assets",  # Asset files
    "images": "images",  # Image files
}

# =============================================================================
# AUTOMATION SETTINGS
# =============================================================================

# Batch Processing
BATCH_SIZE = 50  # Number of items to process in each batch
MAX_CONCURRENT_JOBS = 4  # Maximum concurrent automation jobs

# Retry Configuration
MAX_RETRIES = 3
RETRY_DELAY = 5  # Seconds between retries
EXPONENTIAL_BACKOFF = True  # Use exponential backoff for retries

# Timeout Settings
REQUEST_TIMEOUT = 30  # Seconds for HTTP requests
VIDEO_EXTRACTION_TIMEOUT = 300  # Seconds for video extraction
HTML_GENERATION_TIMEOUT = 60  # Seconds for HTML generation

# =============================================================================
# EXTERNAL SERVICES
# =============================================================================

# YouTube Configuration
YOUTUBE_CONFIG = {
    "api_key": "",  # YouTube Data API key (optional)
    "max_results": 50,  # Maximum results per API call
    "rate_limit_delay": 1,  # Delay between API calls (seconds)
    "use_api": False,  # Use YouTube API instead of yt-dlp when possible
}

# yt-dlp Configuration
YT_DLP_CONFIG = {
    "extract_flat": True,  # Extract metadata only
    "quiet": True,  # Suppress output
    "no_warnings": True,  # Suppress warnings
    "ignoreerrors": True,  # Continue on errors
    "socket_timeout": 30,  # Socket timeout
    "retries": 3,  # Number of retries
}

# =============================================================================
# SECURITY SETTINGS
# =============================================================================

# API Security
API_RATE_LIMIT = 100  # Requests per minute
REQUIRE_API_KEY = False  # Require API key for automation endpoints
ALLOWED_ORIGINS = ["*"]  # CORS allowed origins

# File Security
ALLOWED_FILE_EXTENSIONS = [".html", ".css", ".js", ".json", ".md", ".txt"]
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB maximum file size
SANITIZE_FILENAMES = True  # Sanitize uploaded filenames

# =============================================================================
# MONITORING AND LOGGING
# =============================================================================

# Logging Configuration
LOGGING_CONFIG = {
    "level": "INFO",  # DEBUG, INFO, WARNING, ERROR, CRITICAL
    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    "file_rotation": True,  # Enable log file rotation
    "max_file_size": 10 * 1024 * 1024,  # 10MB per log file
    "backup_count": 5,  # Keep 5 backup log files
}

# Performance Monitoring
MONITORING = {
    "enable_metrics": True,  # Enable performance metrics
    "track_execution_time": True,  # Track execution times
    "track_memory_usage": True,  # Track memory usage
    "metrics_file": "automation_metrics.json",  # Metrics output file
}

# Health Checks
HEALTH_CHECKS = {
    "enable": True,  # Enable health checks
    "interval": 300,  # Health check interval (seconds)
    "endpoints": [  # Endpoints to check
        "/",
        "/health",
    ],
    "timeout": 10,  # Health check timeout (seconds)
}

# =============================================================================
# BACKUP AND RECOVERY
# =============================================================================

# Backup Configuration
BACKUP_CONFIG = {
    "enable_auto_backup": True,  # Enable automatic backups
    "backup_before_changes": True,  # Backup before making changes
    "backup_interval": 24,  # Hours between automatic backups
    "max_backups": 10,  # Maximum number of backups to keep
    "compress_backups": True,  # Compress backup files
    "backup_format": "tar.gz",  # Backup file format
}

# Recovery Configuration
RECOVERY_CONFIG = {
    "enable_auto_recovery": False,  # Enable automatic recovery
    "recovery_timeout": 300,  # Recovery timeout (seconds)
    "verify_after_recovery": True,  # Verify files after recovery
}

# =============================================================================
# NOTIFICATION SETTINGS
# =============================================================================

# Email Notifications (optional)
EMAIL_CONFIG = {
    "enable": False,  # Enable email notifications
    "smtp_server": "smtp.gmail.com",
    "smtp_port": 587,
    "username": "",  # Email username
    "password": "",  # Email password or app password
    "from_email": "",  # From email address
    "to_emails": [],  # List of recipient emails
    "notify_on_success": False,  # Notify on successful completion
    "notify_on_error": True,  # Notify on errors
}

# Webhook Notifications (optional)
WEBHOOK_CONFIG = {
    "enable": False,  # Enable webhook notifications
    "url": "",  # Webhook URL
    "secret": "",  # Webhook secret for verification
    "timeout": 10,  # Webhook timeout (seconds)
    "retry_on_failure": True,  # Retry failed webhooks
}

# =============================================================================
# PERFORMANCE OPTIMIZATION
# =============================================================================

# Caching Configuration
CACHE_CONFIG = {
    "enable": True,  # Enable caching
    "cache_type": "file",  # "file", "memory", "redis"
    "cache_dir": "cache",  # Cache directory for file-based cache
    "default_ttl": 3600,  # Default cache TTL (seconds)
    "max_cache_size": 100 * 1024 * 1024,  # 100MB maximum cache size
}

# Optimization Settings
OPTIMIZATION = {
    "minify_html": False,  # Minify HTML output
    "minify_css": False,  # Minify CSS output
    "minify_js": False,  # Minify JavaScript output
    "compress_json": False,  # Compress JSON output
    "optimize_images": False,  # Optimize image files
}

# =============================================================================
# DEVELOPMENT SETTINGS
# =============================================================================

# Development Tools
DEVELOPMENT = {
    "auto_reload": True,  # Auto-reload on file changes
    "debug_toolbar": True,  # Enable debug toolbar
    "profiling": False,  # Enable profiling
    "mock_external_apis": False,  # Mock external API calls
}

# Testing Configuration
TESTING = {
    "test_data_dir": "test_data",  # Test data directory
    "mock_youtube_responses": True,  # Mock YouTube API responses
    "test_timeout": 60,  # Test timeout (seconds)
    "generate_test_reports": True,  # Generate test reports
}

# =============================================================================
# UTILITY FUNCTIONS
# =============================================================================

def get_base_url():
    """Get the base URL for the current environment"""
    return BASE_URLS.get(ENVIRONMENT, BASE_URLS["development"])

def is_production():
    """Check if running in production environment"""
    return ENVIRONMENT == "production"

def is_development():
    """Check if running in development environment"""
    return ENVIRONMENT == "development"

def get_log_level():
    """Get the appropriate log level for the current environment"""
    if is_development():
        return "DEBUG"
    elif ENVIRONMENT == "staging":
        return "INFO"
    else:  # production
        return "WARNING"

def validate_deployment_config():
    """Validate deployment configuration"""
    errors = []
    
    if ENVIRONMENT not in ["development", "staging", "production"]:
        errors.append(f"Invalid ENVIRONMENT: {ENVIRONMENT}")
    
    if SERVER_PORT < 1 or SERVER_PORT > 65535:
        errors.append(f"Invalid SERVER_PORT: {SERVER_PORT}")
    
    if BATCH_SIZE <= 0:
        errors.append(f"BATCH_SIZE must be greater than 0: {BATCH_SIZE}")
    
    if MAX_CONCURRENT_JOBS <= 0:
        errors.append(f"MAX_CONCURRENT_JOBS must be greater than 0: {MAX_CONCURRENT_JOBS}")
    
    return errors

if __name__ == "__main__":
    # Validate configuration when run directly
    errors = validate_deployment_config()
    if errors:
        print("Deployment configuration errors:")
        for error in errors:
            print(f"  - {error}")
    else:
        print(f"Deployment configuration for '{ENVIRONMENT}' environment is valid!")
        print(f"Base URL: {get_base_url()}")
        print(f"Log Level: {get_log_level()}")
        print(f"Debug Mode: {DEBUG_MODE}")