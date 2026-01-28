"""
Generate a sample Block Blast screenshot for testing.

This creates a realistic-looking game screenshot that can be used
to test the Vision API without needing an actual game screenshot.
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np
from PIL import Image, ImageDraw, ImageFont
from block_blast_solver import GridRenderer, BlockShape, STANDARD_PIECES


def generate_sample_screenshot(output_path: str = "sample_screenshot.png"):
    """
    Generate a realistic Block Blast game screenshot.
    
    Args:
        output_path: Path where to save the screenshot
    """
    print("Generating sample Block Blast screenshot...")
    
    # Create a realistic game state
    grid = np.zeros((8, 8), dtype=bool)
    
    # Add some occupied cells to create an interesting pattern
    grid[0, 0:5] = True      # Partial row
    grid[1, 0:3] = True      # Partial row
    grid[2, 0:2] = True      # Partial row
    grid[3, 0] = True        # Single cell
    grid[0:4, 0] = True      # Partial column
    grid[5, 5:8] = True      # Another pattern
    grid[6, 6:8] = True      
    grid[7, 7] = True        
    
    print("Grid pattern created:")
    for row in grid:
        print("  ", " ".join("█" if cell else "·" for cell in row))
    
    # Create sample pieces
    pieces = [
        STANDARD_PIECES["line_3_h"],
        STANDARD_PIECES["l_3_1"],
        STANDARD_PIECES["single"],
    ]
    
    print(f"\nPieces: {len(pieces)}")
    for i, piece in enumerate(pieces):
        print(f"  {i+1}. {piece.name}")
    
    # Create the screenshot image
    cell_size = 60
    padding = 40
    piece_spacing = 30
    
    # Calculate dimensions
    grid_size = 8 * cell_size
    piece_row_height = 4 * cell_size  # Space for pieces at bottom
    total_width = grid_size + 2 * padding
    total_height = grid_size + piece_row_height + 3 * padding
    
    # Create image with game-like background
    img = Image.new('RGB', (total_width, total_height), (245, 245, 250))
    draw = ImageDraw.Draw(img)
    
    # Add title
    try:
        title_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 30)
        label_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 20)
    except:
        title_font = ImageFont.load_default()
        label_font = ImageFont.load_default()
    
    # Draw title
    title = "Block Blast"
    title_bbox = draw.textbbox((0, 0), title, font=title_font)
    title_width = title_bbox[2] - title_bbox[0]
    draw.text(((total_width - title_width) // 2, 10), title, fill=(67, 97, 238), font=title_font)
    
    # Render grid
    renderer = GridRenderer(cell_size=cell_size)
    grid_img = renderer.render_grid(grid)
    
    # Paste grid
    grid_y = padding + 40
    img.paste(grid_img, (padding, grid_y))
    
    # Draw "Available Pieces" label
    label_y = grid_y + grid_size + 20
    draw.text((padding, label_y), "Available Pieces:", fill=(0, 0, 0), font=label_font)
    
    # Render and paste pieces
    pieces_y = label_y + 40
    piece_x = padding
    
    for i, piece in enumerate(pieces):
        piece_img = renderer.render_piece(piece.cells)
        
        # Center piece in its space
        piece_space = (grid_size - piece_spacing * 2) // 3
        x_offset = piece_x + (piece_space - piece_img.width) // 2
        y_offset = pieces_y + (piece_row_height - 80 - piece_img.height) // 2
        
        # Draw piece container
        container_x1 = piece_x
        container_y1 = pieces_y
        container_x2 = piece_x + piece_space
        container_y2 = pieces_y + piece_row_height - 80
        draw.rectangle([container_x1, container_y1, container_x2, container_y2], 
                      outline=(200, 200, 200), width=2)
        
        # Paste piece
        img.paste(piece_img, (x_offset, y_offset))
        
        piece_x += piece_space + piece_spacing
    
    # Save
    img.save(output_path)
    print(f"\n✓ Sample screenshot saved to: {output_path}")
    print(f"  Image size: {img.size[0]}x{img.size[1]} pixels")
    
    return img


def main():
    """Generate sample screenshots."""
    print("=" * 60)
    print("Sample Screenshot Generator")
    print("=" * 60)
    print()
    
    # Generate default screenshot
    generate_sample_screenshot("sample_screenshot.png")
    
    print("\nYou can now use this screenshot to test:")
    print("  1. Upload it in the Streamlit app")
    print("  2. Test the Vision API analysis")
    print("  3. Verify the solver works correctly")
    print()


if __name__ == "__main__":
    main()
