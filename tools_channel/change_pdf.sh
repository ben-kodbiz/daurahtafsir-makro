#!/bin/zsh

# Loop through all session_x.html files
for i in $(seq 1 115); do
  filename="session_${i}.html"

  # Check if the file exists
  if [ -f "$filename" ]; then
    # Ensure existing http or https paths are replaced with the new base URL
    sed -i -E 's#https?://[^"]+/daurahtafsir-makro/#https://ben-kodbiz.github.io/daurahtafsir-makro/#g' "$filename"

    # Append the new base URL to relative paths
    sed -i -E 's#(<iframe[^>]*src=")(\.\./pdfs/)([^"]+)#\1https://ben-kodbiz.github.io/daurahtafsir-makro/pdfs/\3#' "$filename"
    sed -i -E 's#(<a[^>]*href=")(\.\./pdfs/)([^"]+)#\1https://ben-kodbiz.github.io/daurahtafsir-makro/pdfs/\3#' "$filename"

    echo "Updated file: $filename"
  else
    echo "File not found: $filename"
  fi
done

echo "All session files updated."
