#!/bin/bash

# Utility script for common channel processing tasks

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TOOLS_DIR="$SCRIPT_DIR"

show_menu() {
    echo "🔧 Channel Processing Utilities"
    echo "=============================="
    echo "1. Process new YouTube channel"
    echo "2. Update existing module with new videos"
    echo "3. Regenerate session files with new template"
    echo "4. Update video titles in existing module"
    echo "5. Check channel video count"
    echo "6. List available modules"
    echo "7. Help"
    echo "0. Exit"
    echo ""
}

process_new_channel() {
    echo "🆕 Process New YouTube Channel"
    echo "============================"
    
    read -p "Enter YouTube channel URL: " CHANNEL_URL
    if [[ -z "$CHANNEL_URL" ]]; then
        echo "❌ Channel URL is required"
        return 1
    fi
    
    read -p "Enter module name: " MODULE_NAME
    if [[ -z "$MODULE_NAME" ]]; then
        echo "❌ Module name is required"
        return 1
    fi
    
    read -p "Enter module description: " MODULE_DESCRIPTION
    if [[ -z "$MODULE_DESCRIPTION" ]]; then
        echo "❌ Module description is required"
        return 1
    fi
    
    read -p "Enter output directory (leave empty for default): " OUTPUT_DIR
    
    read -p "Enter maximum videos to process (leave empty for default): " MAX_VIDEOS
    
    # Build command
    CMD="$TOOLS_DIR/process_channel.sh $CHANNEL_URL --name \"$MODULE_NAME\" --description \"$MODULE_DESCRIPTION\""
    
    if [[ -n "$OUTPUT_DIR" ]]; then
        CMD="$CMD --output \"$OUTPUT_DIR\""
    fi
    
    if [[ -n "$MAX_VIDEOS" ]]; then
        CMD="$CMD --max-videos $MAX_VIDEOS"
    fi
    
    echo "🚀 Running: $CMD"
    eval $CMD
}

check_video_count() {
    echo "🔍 Check Channel Video Count"
    echo "=========================="
    
    read -p "Enter YouTube channel URL: " CHANNEL_URL
    if [[ -z "$CHANNEL_URL" ]]; then
        echo "❌ Channel URL is required"
        return 1
    fi
    
    echo "📊 Checking video count for: $CHANNEL_URL"
    yt-dlp --flat-playlist --print "%(id)s" "$CHANNEL_URL" 2>/dev/null | wc -l
}

show_help() {
    echo "❓ Help"
    echo "====="
    echo "This utility provides common tasks for processing YouTube channels:"
    echo ""
    echo "1. Process new channel - Create a new module from a YouTube channel"
    echo "2. Update existing module - Add new videos to an existing module"
    echo "3. Regenerate session files - Re-create session files with updated template"
    echo "4. Update video titles - Refresh titles in existing module"
    echo "5. Check video count - See how many videos a channel has"
    echo "6. List modules - Show all modules in the application"
    echo ""
    echo "For detailed usage, see: $TOOLS_DIR/README.md"
}

list_modules() {
    echo "📂 Available Modules"
    echo "=================="
    
    # Look for module directories
    MODULE_DIRS=$(find .. -maxdepth 2 -name "index.html" -path "*/session*" -printf "%h\n" | sort -u)
    
    if [[ -n "$MODULE_DIRS" ]]; then
        echo "Found modules:"
        for dir in $MODULE_DIRS; do
            # Get module name from directory
            module_name=$(basename "$dir")
            echo "  - $module_name ($(ls $dir/session*.html 2>/dev/null | wc -l) sessions)"
        done
    else
        echo "No modules found. Run 'Process new channel' to create one."
    fi
}

main() {
    while true; do
        show_menu
        read -p "Select an option (0-7): " choice
        
        case $choice in
            1)
                process_new_channel
                echo ""
                read -p "Press Enter to continue..."
                ;;
            2)
                echo "🚧 This feature is coming soon..."
                echo ""
                read -p "Press Enter to continue..."
                ;;
            3)
                echo "🚧 This feature is coming soon..."
                echo ""
                read -p "Press Enter to continue..."
                ;;
            4)
                echo "🚧 This feature is coming soon..."
                echo ""
                read -p "Press Enter to continue..."
                ;;
            5)
                check_video_count
                echo ""
                read -p "Press Enter to continue..."
                ;;
            6)
                list_modules
                echo ""
                read -p "Press Enter to continue..."
                ;;
            7)
                show_help
                echo ""
                read -p "Press Enter to continue..."
                ;;
            0)
                echo "👋 Goodbye!"
                exit 0
                ;;
            *)
                echo "❌ Invalid option. Please select 0-7."
                echo ""
                read -p "Press Enter to continue..."
                ;;
        esac
    done
}

# Run the main function
main