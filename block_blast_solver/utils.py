"""
Utility functions for Block Blast Solver.
"""
from typing import List, Tuple, Optional
import numpy as np
from block_blast_solver.config import GRID_SIZE


def validate_grid(grid: np.ndarray) -> bool:
    """
    Validate that grid is properly formatted.
    
    Args:
        grid: NumPy array representing the game grid
        
    Returns:
        True if valid, False otherwise
    """
    if not isinstance(grid, np.ndarray):
        return False
    
    if grid.shape != (GRID_SIZE, GRID_SIZE):
        return False
    
    if grid.dtype != bool and grid.dtype != int:
        return False
    
    return True


def grid_to_list(grid: np.ndarray) -> List[bool]:
    """
    Convert 2D grid to flat list.
    
    Args:
        grid: 2D NumPy array
        
    Returns:
        Flat list of boolean values
    """
    return grid.flatten().tolist()


def list_to_grid(grid_list: List[bool]) -> np.ndarray:
    """
    Convert flat list to 2D grid.
    
    Args:
        grid_list: Flat list of 64 boolean values
        
    Returns:
        8x8 NumPy array
    """
    if len(grid_list) != GRID_SIZE * GRID_SIZE:
        raise ValueError(f"Grid list must have {GRID_SIZE * GRID_SIZE} elements")
    
    return np.array(grid_list, dtype=bool).reshape(GRID_SIZE, GRID_SIZE)


def can_place_piece(grid: np.ndarray, piece_cells: List[Tuple[int, int]], 
                    position: Tuple[int, int]) -> bool:
    """
    Check if a piece can be placed at a given position.
    
    Args:
        grid: Current game grid
        piece_cells: List of (row, col) offsets for the piece
        position: (row, col) position to place the piece
        
    Returns:
        True if piece can be placed, False otherwise
    """
    row, col = position
    
    for dr, dc in piece_cells:
        new_row, new_col = row + dr, col + dc
        
        # Check bounds
        if not (0 <= new_row < GRID_SIZE and 0 <= new_col < GRID_SIZE):
            return False
        
        # Check if cell is already occupied
        if grid[new_row, new_col]:
            return False
    
    return True


def place_piece(grid: np.ndarray, piece_cells: List[Tuple[int, int]], 
                position: Tuple[int, int]) -> np.ndarray:
    """
    Place a piece on the grid (returns new grid, doesn't modify original).
    
    Args:
        grid: Current game grid
        piece_cells: List of (row, col) offsets for the piece
        position: (row, col) position to place the piece
        
    Returns:
        New grid with piece placed
    """
    new_grid = grid.copy()
    row, col = position
    
    for dr, dc in piece_cells:
        new_row, new_col = row + dr, col + dc
        new_grid[new_row, new_col] = True
    
    return new_grid


def clear_complete_lines(grid: np.ndarray) -> Tuple[np.ndarray, int]:
    """
    Clear complete rows and columns, return new grid and number cleared.
    
    Args:
        grid: Current game grid
        
    Returns:
        Tuple of (new_grid, num_lines_cleared)
    """
    new_grid = grid.copy()
    lines_cleared = 0
    
    # Clear complete rows
    for row in range(GRID_SIZE):
        if np.all(new_grid[row, :]):
            new_grid[row, :] = False
            lines_cleared += 1
    
    # Clear complete columns
    for col in range(GRID_SIZE):
        if np.all(new_grid[:, col]):
            new_grid[:, col] = False
            lines_cleared += 1
    
    return new_grid, lines_cleared


def count_holes(grid: np.ndarray) -> int:
    """
    Count isolated empty cells (holes) in the grid.
    A hole is an empty cell surrounded mostly by occupied cells.
    
    Args:
        grid: Current game grid
        
    Returns:
        Number of holes
    """
    holes = 0
    
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            if not grid[row, col]:  # Empty cell
                # Count occupied neighbors
                occupied_neighbors = 0
                total_neighbors = 0
                
                for dr in [-1, 0, 1]:
                    for dc in [-1, 0, 1]:
                        if dr == 0 and dc == 0:
                            continue
                        
                        new_row, new_col = row + dr, col + dc
                        
                        if 0 <= new_row < GRID_SIZE and 0 <= new_col < GRID_SIZE:
                            total_neighbors += 1
                            if grid[new_row, new_col]:
                                occupied_neighbors += 1
                
                # If more than half neighbors are occupied, it's a hole
                if total_neighbors > 0 and occupied_neighbors / total_neighbors > 0.5:
                    holes += 1
    
    return holes


def calculate_coverage(grid: np.ndarray) -> float:
    """
    Calculate how much of the grid is occupied (0.0 to 1.0).
    
    Args:
        grid: Current game grid
        
    Returns:
        Fraction of grid that is occupied
    """
    return np.sum(grid) / (GRID_SIZE * GRID_SIZE)


def get_all_valid_placements(grid: np.ndarray, 
                             piece_cells: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
    """
    Get all valid positions where a piece can be placed.
    
    Args:
        grid: Current game grid
        piece_cells: List of (row, col) offsets for the piece
        
    Returns:
        List of valid (row, col) positions
    """
    valid_positions = []
    
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            if can_place_piece(grid, piece_cells, (row, col)):
                valid_positions.append((row, col))
    
    return valid_positions
