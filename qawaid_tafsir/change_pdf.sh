#!/bin/zsh

# Loop through all session_x.html files
for i in $(seq 1 115); do
  filename="session_${i}.html"

  # Check if the file exists
  if [ -f "$filename" ]; then
    # Ensure existing http paths are converted to https
    sed -i -E 's#http://kodbiz.github.io/daurahtafsir-makro/pdfs/#https://kodbiz.github.io/daurahtafsir-makro/pdfs/#g' "$filename"

    # Append https:// URL to relative paths
    sed -i -E 's#(<iframe[^>]*src=")(\.\./pdfs/)([^"]+)#\1https://kodbiz.github.io/daurahtafsir-makro/pdfs/\3#' "$filename"
    sed -i -E 's#(<a[^>]*href=")(\.\./pdfs/)([^"]+)#\1https://kodbiz.github.io/daurahtafsir-makro/pdfs/\3#' "$filename"

    echo "Updated file: $filename"
  else
    echo "File not found: $filename"
  fi
done

echo "All session files updated."
