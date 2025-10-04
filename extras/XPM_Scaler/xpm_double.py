#!/usr/bin/env python3
"""
XPM Scaler - Doubles the size of an XPM file while preserving variable names and color definitions
Usage: python xpm_double.py input.xpm output.xpm
"""

import sys

def double_xpm_size(input_file, output_file):
    """Double the size of an XPM file while preserving all metadata"""
    
    # Read the XPM file
    with open(input_file, 'r') as f:
        lines = f.readlines()
    
    # Find the variable name line
    var_line_index = None
    for i, line in enumerate(lines):
        if line.strip().startswith("static char *"):
            var_line_index = i
            break
    
    if var_line_index is None:
        print("Error: Could not find variable declaration line")
        return False
    
    # Find the dimensions line (always right after variable declaration)
    dim_line_index = var_line_index + 1
    dim_line = lines[dim_line_index].strip()
    
    # Extract dimensions using string operations instead of regex
    dim_parts = dim_line.strip('"').split()
    if len(dim_parts) < 4:
        print("Error: Could not parse dimensions line")
        return False
    print(f"dim_parts: {dim_parts}")
    
    # Clean up the last dimension part which might have trailing characters
    dim_parts[3] = ''.join(c for c in dim_parts[3] if c.isdigit())
    
    width = int(dim_parts[0])
    height = int(dim_parts[1])
    num_colors = int(dim_parts[2])
    chars_per_pixel = int(dim_parts[3])
    
    print(f"Original dimensions: {width}x{height}")
    
    # Color definitions follow the dimension line
    color_start = dim_line_index + 1
    color_end = color_start + num_colors
    
    # Pixel data starts after color definitions
    pixel_start = color_end
    
    # Find the end of pixel data (line with "};")
    pixel_end = None
    for i in range(pixel_start, len(lines)):
        if "}" in lines[i] and ";" in lines[i]:
            pixel_end = i
            break
    
    if pixel_end is None:
        print("Error: Could not find end of pixel data")
        return False
    
    # Extract sections
    header = lines[:var_line_index + 1]  # Include variable line in header
    colors = lines[color_start:color_end]
    pixel_lines = lines[pixel_start:pixel_end + 1]
    
    # Create new dimensions line
    new_dim_parts = dim_parts.copy()
    new_dim_parts[0] = str(width * 2)
    new_dim_parts[1] = str(height * 2)
    new_dim_line = f'"{" ".join(new_dim_parts)}",\n'
    
    # Process pixel data to double its size
    scaled_pixels = []
    for i, line in enumerate(pixel_lines):
        line = line.rstrip('\r\n')
        
        # Skip lines without pixel data
        if '"' not in line:
            scaled_pixels.append(line + '\n')
            continue
        
        # Split line into parts
        prefix = line[:line.find('"')]
        pixel_data = line[line.find('"')+1:line.rfind('"')]
        suffix = line[line.rfind('"')+1:]
        
        # Skip empty pixel data
        if not pixel_data:
            scaled_pixels.append(line + '\n')
            continue
        
        # Double each pixel
        doubled_data = ""
        for j in range(0, len(pixel_data), chars_per_pixel):
            pixel = pixel_data[j:j+chars_per_pixel]
            doubled_data += pixel * 2
        
        # Add doubled line
        
        # Add duplicate line, except for the last line which contains '};'
        if i == len(pixel_lines) - 1 and '};' in line:
            scaled_pixels.append(f'{prefix}"{doubled_data}",\n')
            scaled_pixels.append(f'{prefix}"{doubled_data}"{suffix}\n')
        else:
            scaled_pixels.append(f'{prefix}"{doubled_data}"{suffix}\n')
            scaled_pixels.append(f'{prefix}"{doubled_data}"{suffix}\n')
    
    # Write the scaled XPM file
    with open(output_file, 'w') as f:
        # Write header
        for line in header:
            f.write(line)
        
        # Write new dimensions
        f.write(new_dim_line)
        
        # Write color definitions
        for line in colors:
            f.write(line)
        
        # Write scaled pixel data
        for line in scaled_pixels:
            f.write(line)
        
    print(f"Successfully doubled size to {width*2}x{height*2}")
    print(f"Scaled XPM saved to {output_file}")
    return True

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python xpm_double.py input.xpm output.xpm")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    
    double_xpm_size(input_file, output_file)
