"""
Grid rendering and visualization using PIL.
"""
from typing import List, Tuple, Optional
import numpy as np
from PIL import Image, ImageDraw, ImageFont

from block_blast_solver.config import (
    GRID_SIZE, CELL_SIZE, COLOR_OCCUPIED, COLOR_EMPTY, 
    COLOR_HIGHLIGHT, COLOR_GRID_LINE, COLOR_BLOCK_PREVIEW
)


class GridRenderer:
    """Renders Block Blast grids as images."""
    
    def __init__(self, cell_size: int = CELL_SIZE):
        """
        Initialize renderer.
        
        Args:
            cell_size: Size of each cell in pixels
        """
        self.cell_size = cell_size
        self.grid_pixel_size = GRID_SIZE * cell_size
    
    def render_grid(self, grid: np.ndarray, 
                   highlight_cells: Optional[List[Tuple[int, int]]] = None,
                   preview_cells: Optional[List[Tuple[int, int]]] = None) -> Image.Image:
        """
        Render a grid as an image.
        
        Args:
            grid: 8x8 boolean array
            highlight_cells: List of (row, col) cells to highlight (for best move)
            preview_cells: List of (row, col) cells to show as preview
            
        Returns:
            PIL Image of the rendered grid
        """
        # Create image with white background
        img = Image.new('RGB', (self.grid_pixel_size, self.grid_pixel_size), 'white')
        draw = ImageDraw.Draw(img)
        
        highlight_set = set(highlight_cells) if highlight_cells else set()
        preview_set = set(preview_cells) if preview_cells else set()
        
        # Draw cells
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                x1 = col * self.cell_size
                y1 = row * self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size
                
                # Determine cell color
                if (row, col) in preview_set:
                    color = COLOR_BLOCK_PREVIEW
                elif (row, col) in highlight_set:
                    color = COLOR_HIGHLIGHT
                elif grid[row, col]:
                    color = COLOR_OCCUPIED
                else:
                    color = COLOR_EMPTY
                
                # Draw filled rectangle
                draw.rectangle([x1, y1, x2, y2], fill=color, outline=COLOR_GRID_LINE)
        
        return img
    
    def render_piece(self, piece_cells: List[Tuple[int, int]], 
                    color: Tuple[int, int, int] = COLOR_OCCUPIED) -> Image.Image:
        """
        Render a piece as an image.
        
        Args:
            piece_cells: List of (row, col) cells in the piece
            color: RGB color for the piece
            
        Returns:
            PIL Image of the piece
        """
        if not piece_cells:
            return Image.new('RGB', (self.cell_size, self.cell_size), 'white')
        
        # Calculate bounding box
        min_row = min(r for r, c in piece_cells)
        max_row = max(r for r, c in piece_cells)
        min_col = min(c for r, c in piece_cells)
        max_col = max(c for r, c in piece_cells)
        
        width = (max_col - min_col + 1) * self.cell_size
        height = (max_row - min_row + 1) * self.cell_size
        
        # Create image
        img = Image.new('RGB', (width, height), 'white')
        draw = ImageDraw.Draw(img)
        
        # Draw cells
        for row, col in piece_cells:
            # Adjust to bounding box
            adjusted_row = row - min_row
            adjusted_col = col - min_col
            
            x1 = adjusted_col * self.cell_size
            y1 = adjusted_row * self.cell_size
            x2 = x1 + self.cell_size
            y2 = y1 + self.cell_size
            
            draw.rectangle([x1, y1, x2, y2], fill=color, outline=COLOR_GRID_LINE)
        
        return img
    
    def render_grid_with_move(self, grid: np.ndarray, 
                             move_cells: List[Tuple[int, int]],
                             move_position: Tuple[int, int]) -> Image.Image:
        """
        Render grid with a move highlighted.
        
        Args:
            grid: Current grid state
            move_cells: Piece cells (relative coordinates)
            move_position: Position where piece will be placed
            
        Returns:
            PIL Image showing the move
        """
        # Calculate absolute positions of the move
        row_offset, col_offset = move_position
        absolute_cells = [(r + row_offset, c + col_offset) for r, c in move_cells]
        
        return self.render_grid(grid, highlight_cells=absolute_cells)
    
    def create_comparison_image(self, original_img: Image.Image,
                               rendered_grid: Image.Image,
                               padding: int = 20) -> Image.Image:
        """
        Create side-by-side comparison of original and rendered images.
        
        Args:
            original_img: Original screenshot
            rendered_grid: Rendered grid image
            padding: Padding between images
            
        Returns:
            Combined image
        """
        # Resize original to match rendered grid height
        aspect_ratio = original_img.width / original_img.height
        new_height = rendered_grid.height
        new_width = int(new_height * aspect_ratio)
        original_resized = original_img.resize((new_width, new_height), 
                                               Image.Resampling.LANCZOS)
        
        # Create combined image
        total_width = original_resized.width + rendered_grid.width + padding * 3
        total_height = rendered_grid.height + padding * 2
        
        combined = Image.new('RGB', (total_width, total_height), 'white')
        
        # Paste images
        combined.paste(original_resized, (padding, padding))
        combined.paste(rendered_grid, 
                      (original_resized.width + padding * 2, padding))
        
        return combined
    
    def add_text_overlay(self, img: Image.Image, text: str, 
                        position: Tuple[int, int] = (10, 10),
                        font_size: int = 20) -> Image.Image:
        """
        Add text overlay to an image.
        
        Args:
            img: Image to add text to
            text: Text to add
            position: (x, y) position for text
            font_size: Font size
            
        Returns:
            Image with text overlay
        """
        img_copy = img.copy()
        draw = ImageDraw.Draw(img_copy)
        
        try:
            # Try to use a nice font
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 
                                     font_size)
        except:
            # Fall back to default font
            font = ImageFont.load_default()
        
        # Draw text with background for visibility
        bbox = draw.textbbox(position, text, font=font)
        draw.rectangle(bbox, fill='white')
        draw.text(position, text, fill='black', font=font)
        
        return img_copy


def render_pieces_row(pieces: List[List[Tuple[int, int]]], 
                     cell_size: int = CELL_SIZE) -> Image.Image:
    """
    Render multiple pieces in a horizontal row.
    
    Args:
        pieces: List of piece cell lists
        cell_size: Size of each cell in pixels
        
    Returns:
        Combined image of all pieces
    """
    renderer = GridRenderer(cell_size)
    piece_images = [renderer.render_piece(piece) for piece in pieces]
    
    if not piece_images:
        return Image.new('RGB', (cell_size, cell_size), 'white')
    
    # Calculate total width
    total_width = sum(img.width for img in piece_images) + (len(piece_images) + 1) * 10
    max_height = max(img.height for img in piece_images) + 20
    
    # Create combined image
    combined = Image.new('RGB', (total_width, max_height), 'white')
    
    # Paste pieces with spacing
    x_offset = 10
    for img in piece_images:
        y_offset = (max_height - img.height) // 2
        combined.paste(img, (x_offset, y_offset))
        x_offset += img.width + 10
    
    return combined
