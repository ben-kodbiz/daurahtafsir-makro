#!/bin/bash
# Example usage of the Kitab Grid Enhancement Script

# Example 1: Enhance a kitab with basic parameters
echo "Example 1: Basic enhancement"
./enhance_kitab_grid.py video_data.txt --name "Kitab Haji" --description "Kitab Haji from Sahih Muslim series"

# Example 2: Enhance with custom output path
echo -e "\nExample 2: Custom output path"
./enhance_kitab_grid.py video_data.txt --name "Kitab Iman" --output "./enhanced_index.html"

# Example 3: Full enhancement with all parameters
echo -e "\nExample 3: Full enhancement"
./enhance_kitab_grid.py video_data.txt --name "Kitab Thaharah" --description "Kitab Thaharah from Sahih Muslim series" --output "./index.html"

echo -e "\n✅ Examples completed. Check the generated files."