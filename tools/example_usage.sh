#!/bin/bash

# Example usage scripts for the channel processor

echo "Example 1: Process a channel with default settings"
echo "python3 channel_processor.py https://www.youtube.com/@example-channel \\"
echo "    --name \"Example Module\" \\"
echo "    --description \"An example module for demonstration\""
echo ""

echo "Example 2: Process with custom output directory and limits"
echo "python3 channel_processor.py https://www.youtube.com/@example-channel \\"
echo "    --name \"Custom Module\" \\"
echo "    --description \"A module with custom settings\" \\"
echo "    --output ../my_custom_module \\"
echo "    --max-videos 50 \\"
echo "    --delay 2.0"
echo ""

echo "Example 3: Process using the shell script wrapper"
echo "./process_channel.sh https://www.youtube.com/@example-channel \\"
echo "    --name \"Shell Script Module\" \\"
echo "    --description \"Module processed via shell script\" \\"
echo "    --output ../shell_script_module"