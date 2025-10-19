#!/usr/bin/env python3
"""Extract individual shapes from a DXF file"""

import sys
import re

def parse_dxf_shapes(filename):
    """Parse DXF file and extract all spline entities with their bounding boxes"""
    with open(filename, 'r') as f:
        lines = [line.strip() for line in f.readlines()]
    
    shapes = []
    i = 0
    shape_num = 0
    
    while i < len(lines):
        if lines[i] == 'SPLINE':
            shape_num += 1
            # Find the entity data
            start_line = i
            coords_x = []
            coords_y = []
            
            # Parse until we hit the next entity or end
            j = i + 1
            while j < len(lines) and lines[j] not in ['SPLINE', 'ENDSEC', 'ENDBLK']:
                # Code 10 = X coordinate
                if lines[j] == '10' and j + 1 < len(lines):
                    try:
                        coords_x.append(float(lines[j + 1]))
                    except:
                        pass
                # Code 20 = Y coordinate  
                elif lines[j] == '20' and j + 1 < len(lines):
                    try:
                        coords_y.append(float(lines[j + 1]))
                    except:
                        pass
                j += 1
            
            if coords_x and coords_y:
                min_x = min(coords_x)
                max_x = max(coords_x)
                min_y = min(coords_y)
                max_y = max(coords_y)
                width = max_x - min_x
                height = max_y - min_y
                
                shapes.append({
                    'num': shape_num,
                    'start_line': start_line,
                    'end_line': j,
                    'min_x': min_x,
                    'max_x': max_x,
                    'min_y': min_y,
                    'max_y': max_y,
                    'width': width,
                    'height': height,
                    'center_x': (min_x + max_x) / 2,
                    'center_y': (min_y + max_y) / 2
                })
            
            i = j
        else:
            i += 1
    
    return shapes, lines

def extract_shape(lines, shape_info, output_file):
    """Extract a single shape and create a new DXF file"""
    
    # DXF header
    header = """  0
SECTION
  2
HEADER
  9
$ACADVER
  1
AC1018
  9
$INSBASE
 10
0.0
 20
0.0
 30
0.0
  9
$EXTMIN
 10
{min_x}
 20
{min_y}
 30
0.0
  9
$EXTMAX
 10
{max_x}
 20
{max_y}
 30
0.0
  0
ENDSEC
  0
SECTION
  2
TABLES
  0
TABLE
  2
LAYER
 70
1
  0
LAYER
  2
0
 70
0
 62
7
  6
CONTINUOUS
  0
ENDTAB
  0
ENDSEC
  0
SECTION
  2
ENTITIES
""".format(
        min_x=shape_info['min_x'],
        max_x=shape_info['max_x'],
        min_y=shape_info['min_y'],
        max_y=shape_info['max_y']
    )
    
    # Extract the shape data
    shape_data = '\n'.join(lines[shape_info['start_line']:shape_info['end_line']])
    
    # DXF footer
    footer = """  0
ENDSEC
  0
EOF
"""
    
    with open(output_file, 'w') as f:
        f.write(header)
        f.write(shape_data)
        f.write('\n')
        f.write(footer)
    
    print(f"Shape extracted to: {output_file}")

def main():
    input_file = 'frontX3.dxf'
    
    print("Parsing DXF file...")
    shapes, lines = parse_dxf_shapes(input_file)
    
    print(f"\nFound {len(shapes)} spline shapes\n")
    
    # Filter for bottom-left shapes (lower X and Y coordinates)
    # Sort by position: bottom-left first
    shapes_sorted = sorted(shapes, key=lambda s: (s['center_y'], s['center_x']))
    
    print("Shapes sorted by position (bottom-left first):")
    print("=" * 80)
    for i, shape in enumerate(shapes_sorted[:20]):  # Show first 20
        print(f"Shape #{shape['num']}: "
              f"Position: ({shape['min_x']:.2f}, {shape['min_y']:.2f}) to ({shape['max_x']:.2f}, {shape['max_y']:.2f})")
        print(f"  Center: ({shape['center_x']:.2f}, {shape['center_y']:.2f}), "
              f"Size: {shape['width']:.2f} x {shape['height']:.2f}")
        print()
    
    # Find large oval shapes in bottom left (assuming bottom-left means low x, low y)
    print("\nLarge shapes in bottom-left area:")
    print("=" * 80)
    large_shapes = [s for s in shapes_sorted if s['width'] > 3 and s['height'] > 3 and 
                    s['center_x'] < 20 and s['center_y'] < 20]
    
    for shape in large_shapes[:10]:
        print(f"Shape #{shape['num']}: Size: {shape['width']:.2f} x {shape['height']:.2f}, "
              f"Center: ({shape['center_x']:.2f}, {shape['center_y']:.2f})")
    
    if large_shapes:
        print(f"\nExtracting shape #{large_shapes[0]['num']} (the first large oval in bottom-left)...")
        extract_shape(lines, large_shapes[0], 'extracted_oval.dxf')
    else:
        print("\nNo large oval shapes found in bottom-left. Extracting first shape...")
        extract_shape(lines, shapes_sorted[0], 'extracted_shape.dxf')

if __name__ == '__main__':
    main()
