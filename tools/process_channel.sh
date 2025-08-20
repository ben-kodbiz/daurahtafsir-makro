#!/bin/bash

# Channel Processor Wrapper Script
# This script provides a simple interface to the Python channel processor

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TOOLS_DIR="$SCRIPT_DIR"

# Check if Python 3 is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 is not installed or not in PATH"
    exit 1
fi

# Check if yt-dlp is available
if ! command -v yt-dlp &> /dev/null; then
    echo "❌ Error: yt-dlp is not installed or not in PATH"
    echo "Please install yt-dlp: pip install yt-dlp"
    exit 1
fi

# Function to show usage
show_usage() {
    echo "📺 Channel Processor Tool"
    echo "========================="
    echo "A tool for processing YouTube channels and creating web modules"
    echo ""
    echo "Usage:"
    echo "  $0 <channel_url> --name <module_name> --description <description> [options]"
    echo ""
    echo "Required arguments:"
    echo "  channel_url              YouTube channel URL"
    echo "  --name <module_name>     Name of the module"
    echo "  --description <desc>     Description of the module"
    echo ""
    echo "Optional arguments:"
    echo "  --output <dir>           Output directory (default: ./output)"
    echo "  --max-videos <number>    Maximum number of videos to process"
    echo "  --config <file>          Configuration file (default: config.ini)"
    echo "  --help                   Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 https://www.youtube.com/@channel --name \"My Module\" --description \"Description of my module\""
    echo "  $0 https://www.youtube.com/@channel --name \"My Module\" --description \"Description\" --output ./mymodule --max-videos 50"
}

# Parse command line arguments
CHANNEL_URL=""
MODULE_NAME=""
MODULE_DESCRIPTION=""
OUTPUT_DIR=""
MAX_VIDEOS=""
CONFIG_FILE=""

# Check if help is requested
for arg in "$@"; do
    if [[ "$arg" == "--help" ]] || [[ "$arg" == "-h" ]]; then
        show_usage
        exit 0
    fi
done

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --name)
            MODULE_NAME="$2"
            shift 2
            ;;
        --description)
            MODULE_DESCRIPTION="$2"
            shift 2
            ;;
        --output)
            OUTPUT_DIR="$2"
            shift 2
            ;;
        --max-videos)
            MAX_VIDEOS="$2"
            shift 2
            ;;
        --config)
            CONFIG_FILE="$2"
            shift 2
            ;;
        *)
            if [[ -z "$CHANNEL_URL" ]]; then
                CHANNEL_URL="$1"
            fi
            shift
            ;;
    esac
done

# Validate required arguments
if [[ -z "$CHANNEL_URL" ]]; then
    echo "❌ Error: Channel URL is required"
    show_usage
    exit 1
fi

if [[ -z "$MODULE_NAME" ]]; then
    echo "❌ Error: Module name is required (--name)"
    show_usage
    exit 1
fi

if [[ -z "$MODULE_DESCRIPTION" ]]; then
    echo "❌ Error: Module description is required (--description)"
    show_usage
    exit 1
fi

# Build command arguments
CMD_ARGS=("$CHANNEL_URL" --name "$MODULE_NAME" --description "$MODULE_DESCRIPTION")

if [[ -n "$OUTPUT_DIR" ]]; then
    CMD_ARGS+=(--output "$OUTPUT_DIR")
fi

if [[ -n "$MAX_VIDEOS" ]]; then
    CMD_ARGS+=(--max-videos "$MAX_VIDEOS")
fi

if [[ -n "$CONFIG_FILE" ]]; then
    CMD_ARGS+=(--config "$CONFIG_FILE")
fi

# Run the Python script
echo "🚀 Processing channel: $CHANNEL_URL"
echo "📋 Module name: $MODULE_NAME"
echo "📝 Description: $MODULE_DESCRIPTION"

if [[ -n "$OUTPUT_DIR" ]]; then
    echo "📁 Output directory: $OUTPUT_DIR"
fi

if [[ -n "$MAX_VIDEOS" ]]; then
    echo "📊 Max videos: $MAX_VIDEOS"
fi

echo ""
echo "🔄 Starting channel processing..."

python3 "$TOOLS_DIR/channel_processor.py" "${CMD_ARGS[@]}"

EXIT_CODE=$?

if [[ $EXIT_CODE -eq 0 ]]; then
    echo ""
    echo "✅ Channel processing completed successfully!"
    
    if [[ -n "$OUTPUT_DIR" ]]; then
        echo "📂 Output files are in: $OUTPUT_DIR"
    else
        echo "📂 Output files are in: $TOOLS_DIR/output"
    fi
else
    echo ""
    echo "❌ Channel processing failed!"
    exit $EXIT_CODE
fi