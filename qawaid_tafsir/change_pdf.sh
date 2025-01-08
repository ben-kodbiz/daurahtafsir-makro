#!/bin/zsh

# Loop through all session_x.html files
for i in $(seq 1 115); do
  filename="session_${i}.html"

  # Check if the file exists
  if [ -f "$filename" ]; then
    # Update the iframe src attribute
    sed -i -E 's#(<iframe[^>]*src=")(\.\./pdfs/)([^"]+)#\1http://kodbiz.github.io/daurahtafsir-makro/pdfs/\3#' "$filename"

    # Update the anchor href attribute
    sed -i -E 's#(<a[^>]*href=")(\.\./pdfs/)([^"]+)#\1http://kodbiz.github.io/daurahtafsir-makro/pdfs/\3#' "$filename"

    echo "Updated file: $filename"
  else
    echo "File not found: $filename"
  fi
done

echo "All session files updated."
