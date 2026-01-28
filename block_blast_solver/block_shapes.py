"""
Block shape definitions and rotation logic for Block Blast.
"""
from typing import List, Tuple, Set
import numpy as np


class BlockShape:
    """Represents a block shape with its occupied cells."""
    
    def __init__(self, cells: List[Tuple[int, int]], name: str = ""):
        """
        Initialize a block shape.
        
        Args:
            cells: List of (row, col) tuples representing occupied cells
            name: Optional name for the block shape
        """
        self.cells = self._normalize(cells)
        self.name = name
        self.width = max(c[1] for c in self.cells) + 1 if self.cells else 0
        self.height = max(c[0] for c in self.cells) + 1 if self.cells else 0
    
    @staticmethod
    def _normalize(cells: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
        """Normalize cells to start from (0, 0)."""
        if not cells:
            return []
        
        min_row = min(c[0] for c in cells)
        min_col = min(c[1] for c in cells)
        
        normalized = [(r - min_row, c - min_col) for r, c in cells]
        return sorted(normalized)
    
    def rotate_90(self) -> 'BlockShape':
        """Rotate the block 90 degrees clockwise."""
        rotated = [(c, -r) for r, c in self.cells]
        return BlockShape(rotated, f"{self.name}_r90")
    
    def rotate_180(self) -> 'BlockShape':
        """Rotate the block 180 degrees."""
        rotated = [(-r, -c) for r, c in self.cells]
        return BlockShape(rotated, f"{self.name}_r180")
    
    def rotate_270(self) -> 'BlockShape':
        """Rotate the block 270 degrees clockwise."""
        rotated = [(-c, r) for r, c in self.cells]
        return BlockShape(rotated, f"{self.name}_r270")
    
    def flip_horizontal(self) -> 'BlockShape':
        """Flip the block horizontally."""
        flipped = [(r, -c) for r, c in self.cells]
        return BlockShape(flipped, f"{self.name}_fh")
    
    def flip_vertical(self) -> 'BlockShape':
        """Flip the block vertically."""
        flipped = [(-r, c) for r, c in self.cells]
        return BlockShape(flipped, f"{self.name}_fv")
    
    def get_all_orientations(self) -> List['BlockShape']:
        """Get all unique orientations of this block."""
        orientations = [
            self,
            self.rotate_90(),
            self.rotate_180(),
            self.rotate_270(),
            self.flip_horizontal(),
            self.flip_vertical(),
            self.flip_horizontal().rotate_90(),
            self.flip_horizontal().rotate_180(),
        ]
        
        # Remove duplicates by comparing cell sets
        unique = []
        seen_cells = set()
        
        for orientation in orientations:
            cell_tuple = tuple(orientation.cells)
            if cell_tuple not in seen_cells:
                seen_cells.add(cell_tuple)
                unique.append(orientation)
        
        return unique
    
    def __repr__(self) -> str:
        return f"BlockShape({self.cells}, name='{self.name}')"
    
    def __eq__(self, other) -> bool:
        return isinstance(other, BlockShape) and self.cells == other.cells
    
    def __hash__(self) -> bool:
        return hash(tuple(self.cells))


# Define all standard Block Blast pieces
STANDARD_PIECES = {
    # 1-cell
    "single": BlockShape([(0, 0)], "single"),
    
    # 2-cell (domino)
    "domino_h": BlockShape([(0, 0), (0, 1)], "domino_h"),
    "domino_v": BlockShape([(0, 0), (1, 0)], "domino_v"),
    
    # 3-cell straight
    "line_3_h": BlockShape([(0, 0), (0, 1), (0, 2)], "line_3_h"),
    "line_3_v": BlockShape([(0, 0), (1, 0), (2, 0)], "line_3_v"),
    
    # 3-cell L-shapes
    "l_3_1": BlockShape([(0, 0), (1, 0), (1, 1)], "l_3_1"),
    "l_3_2": BlockShape([(0, 0), (0, 1), (1, 0)], "l_3_2"),
    "l_3_3": BlockShape([(0, 0), (0, 1), (1, 1)], "l_3_3"),
    "l_3_4": BlockShape([(0, 1), (1, 0), (1, 1)], "l_3_4"),
    
    # 4-cell square
    "square_4": BlockShape([(0, 0), (0, 1), (1, 0), (1, 1)], "square_4"),
    
    # 4-cell line
    "line_4_h": BlockShape([(0, 0), (0, 1), (0, 2), (0, 3)], "line_4_h"),
    "line_4_v": BlockShape([(0, 0), (1, 0), (2, 0), (3, 0)], "line_4_v"),
    
    # 4-cell T-shape
    "t_4": BlockShape([(0, 0), (0, 1), (0, 2), (1, 1)], "t_4"),
    
    # 4-cell L-shapes
    "l_4_1": BlockShape([(0, 0), (1, 0), (2, 0), (2, 1)], "l_4_1"),
    "l_4_2": BlockShape([(0, 0), (1, 0), (2, 0), (0, 1)], "l_4_2"),
    
    # 4-cell Z-shapes
    "z_4_1": BlockShape([(0, 0), (0, 1), (1, 1), (1, 2)], "z_4_1"),
    "z_4_2": BlockShape([(0, 1), (0, 2), (1, 0), (1, 1)], "z_4_2"),
    
    # 5-cell line
    "line_5_h": BlockShape([(0, 0), (0, 1), (0, 2), (0, 3), (0, 4)], "line_5_h"),
    "line_5_v": BlockShape([(0, 0), (1, 0), (2, 0), (3, 0), (4, 0)], "line_5_v"),
    
    # 5-cell plus
    "plus_5": BlockShape([(0, 1), (1, 0), (1, 1), (1, 2), (2, 1)], "plus_5"),
    
    # 5-cell L-shapes
    "l_5_1": BlockShape([(0, 0), (1, 0), (2, 0), (3, 0), (3, 1)], "l_5_1"),
    
    # 5-cell T-shapes
    "t_5": BlockShape([(0, 0), (0, 1), (0, 2), (1, 1), (2, 1)], "t_5"),
}


def parse_piece_from_vision(piece_data: dict) -> BlockShape:
    """
    Parse a piece from Vision API output.
    
    Args:
        piece_data: Dictionary with 'cells' key containing list of [x, y] coordinates
        
    Returns:
        BlockShape instance
    """
    cells = piece_data.get('cells', [])
    # Convert [x, y] to (row, col) which is (y, x)
    cells_tuples = [(y, x) for x, y in cells]
    return BlockShape(cells_tuples)


def find_matching_piece(cells: List[Tuple[int, int]]) -> str:
    """
    Find the standard piece name that matches the given cells.
    
    Args:
        cells: List of (row, col) tuples
        
    Returns:
        Name of matching piece or 'custom'
    """
    test_shape = BlockShape(cells)
    
    for name, piece in STANDARD_PIECES.items():
        # Check if any orientation matches
        for orientation in piece.get_all_orientations():
            if orientation.cells == test_shape.cells:
                return name
    
    return "custom"
