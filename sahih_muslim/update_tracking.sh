#!/bin/bash
# Script to update Kitab implementation status

KITAB_TRACKING_FILE="KITAB_TRACKING.md"

# Function to update status
update_status() {
    local kitab_number=$1
    local status=$2
    local sessions=$3
    local notes=$4
    
    # Create backup
    cp "$KITAB_TRACKING_FILE" "${KITAB_TRACKING_FILE}.backup"
    
    # Update the status in the tracking file
    # This is a simple approach - in a real implementation, you might want to use a more sophisticated method
    echo "Updating Kitab $kitab_number status to $status"
    
    # For now, we'll just print what would be updated
    echo "Kitab Number: $kitab_number"
    echo "New Status: $status"
    echo "Sessions: $sessions"
    echo "Notes: $notes"
    
    echo "Please manually update the $KITAB_TRACKING_FILE with this information"
    echo "Backup created as ${KITAB_TRACKING_FILE}.backup"
}

# Show usage
show_usage() {
    echo "Usage: $0 <kitab_number> <status> [sessions] [notes]"
    echo ""
    echo "Status options:"
    echo "  completed    - Mark as completed"
    echo "  in-progress  - Mark as in progress"
    echo "  planned      - Mark as planned"
    echo "  not-started  - Mark as not started"
    echo ""
    echo "Examples:"
    echo "  $0 2 completed 15 \"All sessions processed\""
    echo "  $0 3 in-progress 5 \"Processing videos\""
    echo "  $0 4 planned 0 \"Scheduled for next month\""
}

# Main script
if [[ $# -lt 2 ]]; then
    show_usage
    exit 1
fi

KITAB_NUMBER=$1
STATUS_INPUT=$2
SESSIONS=${3:-"TBD"}
NOTES=${4:-" "}

# Convert status to emoji
case $STATUS_INPUT in
    completed|Completed)
        STATUS="✅ Completed"
        ;;
    in-progress|In-progress|In-progress)
        STATUS="🔄 In Progress"
        ;;
    planned|Planned)
        STATUS="⏳ Planned"
        ;;
    not-started|Not-started|Notstarted)
        STATUS="❌ Not Started"
        ;;
    *)
        STATUS="$STATUS_INPUT"
        ;;
esac

update_status "$KITAB_NUMBER" "$STATUS" "$SESSIONS" "$NOTES"