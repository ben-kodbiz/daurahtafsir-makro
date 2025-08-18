#!/bin/zsh

# Loop through all session_x.html files
for i in $(seq 1 80); do
  filename="session_${i}.html"

  # Check if the file exists
  if [ -f "$filename" ]; then
    # Use sed to remove the Other Materials section spanning multiple lines
    sed -i '' -e '/<h3 class="section-heading">Other Materials<\/h3>/,/<\/div>/d' "$filename"

    echo "Updated file: $filename"
  else
    echo "File not found: $filename"
  fi
done

echo "All session files processed."
