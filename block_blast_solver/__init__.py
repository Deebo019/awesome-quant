"""
Block Blast Solver - A complete puzzle solver using GPT-4o Vision API.
"""

__version__ = "1.0.0"

from block_blast_solver.block_shapes import BlockShape, STANDARD_PIECES
from block_blast_solver.solver import BlockBlastSolver, solve_puzzle, Move
from block_blast_solver.image_analyzer import VisionAnalyzer, create_sample_data
from block_blast_solver.grid_renderer import GridRenderer, render_pieces_row
from block_blast_solver.utils import validate_grid, list_to_grid, grid_to_list

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
