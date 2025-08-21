#!/bin/zsh

# Check if there are any PDF files in the current directory
if [ -z "$(ls *.pdf 2>/dev/null)" ]; then
    echo "No PDF files found in the current directory."
    exit 0
fi

# Convert each PDF file to HTML
for pdf_file in *.pdf; do
    base_name="${pdf_file%.pdf}"
    echo "Converting '$pdf_file' to '$base_name.html'..."
    pdf2htmlEX "$pdf_file" "$base_name.html"
    if [ $? -eq 0 ]; then
        echo "Successfully converted '$pdf_file' to '$base_name.html'."
    else
        echo "Failed to convert '$pdf_file'."
    fi
    echo
done

echo "All conversions completed."
