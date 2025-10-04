#!/bin/bash

# Create the output directory if it doesn't exist
mkdir -p out_files

# Process each .xpm file in the files directory
for file in ./files/*.xpm; do
    # Get just the filename without path
    filename=$(basename "$file")
    
    # Create output filename.
    output_filename="${filename}"
    
    # Run the xpm_double.py script
    echo "Processing $filename..."
    python xpm_double.py "$file" "out_files/$output_filename"
done

echo "All files processed successfully!"

