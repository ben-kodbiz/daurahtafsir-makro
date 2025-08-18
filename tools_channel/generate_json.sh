#!/bin/bash

# Generate JSON entries for sessions 21-120
echo "Generating JSON entries..."

# Create the additional JSON entries
for i in {21..120}; do
    echo "        { \"session_number\": $i, \"title\": \"Sesi $i – Usul Dirayat Hadis\", \"youtube_link\": \"placeholder$i\" },"
done > additional_sessions.json

# Remove the last comma from the last line
sed -i '$ s/,$//' additional_sessions.json

echo "Generated additional_sessions.json with entries for sessions 21-120"
echo "You can now append this to the main JSON file"