"""
Block Blast Solver - A complete puzzle solver using GPT-4o Vision API.
"""

__version__ = "1.0.0"

from .block_shapes import BlockShape, STANDARD_PIECES
from .solver import BlockBlastSolver, solve_puzzle, Move
from .image_analyzer import VisionAnalyzer, create_sample_data
from .grid_renderer import GridRenderer, render_pieces_row
from .utils import validate_grid, list_to_grid, grid_to_list

__all__ = [
    'BlockShape',
    'STANDARD_PIECES',
    'BlockBlastSolver',
    'solve_puzzle',
    'Move',
    'VisionAnalyzer',
    'create_sample_data',
    'GridRenderer',
    'render_pieces_row',
    'validate_grid',
    'list_to_grid',
    'grid_to_list',
]
