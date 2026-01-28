"""
Core solving algorithm for Block Blast.
"""
from typing import List, Tuple, Optional, Dict
import numpy as np
from dataclasses import dataclass
from functools import lru_cache

from block_blast_solver.config import (
    SCORE_ROW_CLEAR, SCORE_COL_CLEAR, SCORE_HOLE_PENALTY, SCORE_COVERAGE
)
from block_blast_solver.utils import (
    can_place_piece, place_piece, clear_complete_lines, count_holes, 
    calculate_coverage, get_all_valid_placements
)
from block_blast_solver.block_shapes import BlockShape


@dataclass
class Move:
    """Represents a single move with its evaluation."""
    piece_index: int  # Which of the 3 pieces (0, 1, 2)
    position: Tuple[int, int]  # (row, col) where to place
    piece_cells: List[Tuple[int, int]]  # The piece shape
    score: float  # Evaluated score for this move
    lines_cleared: int  # Number of lines cleared by this move
    resulting_grid: np.ndarray  # Grid state after move
    
    def __repr__(self) -> str:
        return (f"Move(piece={self.piece_index}, pos={self.position}, "
                f"score={self.score:.2f}, lines={self.lines_cleared})")


class BlockBlastSolver:
    """Solver for Block Blast puzzle game."""
    
    def __init__(self, grid: np.ndarray, pieces: List[BlockShape]):
        """
        Initialize solver.
        
        Args:
            grid: 8x8 boolean array representing current game state
            pieces: List of available BlockShape pieces (typically 3)
        """
        self.grid = grid.copy()
        self.pieces = pieces
        self.best_move: Optional[Move] = None
    
    def evaluate_position(self, grid: np.ndarray, lines_cleared: int) -> float:
        """
        Evaluate a grid position with a scoring heuristic.
        
        Args:
            grid: Grid state to evaluate
            lines_cleared: Number of lines cleared to reach this state
            
        Returns:
            Score for this position (higher is better)
        """
        score = 0.0
        
        # Priority 1: Reward line clears
        score += lines_cleared * SCORE_ROW_CLEAR
        
        # Priority 2: Penalize holes
        holes = count_holes(grid)
        score += holes * SCORE_HOLE_PENALTY
        
        # Priority 3: Prefer keeping board clear
        coverage = calculate_coverage(grid)
        score += (1.0 - coverage) * SCORE_COVERAGE * 100
        
        # Additional heuristics
        
        # Bonus for rows/columns close to complete
        for row in range(8):
            occupied = np.sum(grid[row, :])
            if occupied >= 6:  # Close to complete
                score += (occupied - 5) * 5
        
        for col in range(8):
            occupied = np.sum(grid[:, col])
            if occupied >= 6:  # Close to complete
                score += (occupied - 5) * 5
        
        # Penalty for fragmentation (many small groups of empty cells)
        # This encourages keeping empty space contiguous
        empty_groups = self._count_empty_groups(grid)
        if empty_groups > 3:
            score -= (empty_groups - 3) * 5
        
        return score
    
    def _count_empty_groups(self, grid: np.ndarray) -> int:
        """Count number of contiguous groups of empty cells."""
        visited = np.zeros_like(grid, dtype=bool)
        groups = 0
        
        def dfs(r: int, c: int):
            """Depth-first search to mark connected empty cells."""
            if (r < 0 or r >= 8 or c < 0 or c >= 8 or 
                visited[r, c] or grid[r, c]):
                return
            
            visited[r, c] = True
            dfs(r+1, c)
            dfs(r-1, c)
            dfs(r, c+1)
            dfs(r, c-1)
        
        for row in range(8):
            for col in range(8):
                if not grid[row, col] and not visited[row, col]:
                    dfs(row, col)
                    groups += 1
        
        return groups
    
    def find_best_move(self) -> Optional[Move]:
        """
        Find the best move from current position.
        
        Returns:
            Best Move object or None if no moves available
        """
        all_moves = []
        
        # Try each available piece
        for piece_idx, piece in enumerate(self.pieces):
            # Try all orientations of the piece
            for orientation in piece.get_all_orientations():
                piece_cells = orientation.cells
                
                # Try all valid positions
                valid_positions = get_all_valid_placements(self.grid, piece_cells)
                
                for position in valid_positions:
                    # Simulate the move
                    new_grid = place_piece(self.grid, piece_cells, position)
                    new_grid, lines_cleared = clear_complete_lines(new_grid)
                    
                    # Evaluate this position
                    score = self.evaluate_position(new_grid, lines_cleared)
                    
                    move = Move(
                        piece_index=piece_idx,
                        position=position,
                        piece_cells=piece_cells,
                        score=score,
                        lines_cleared=lines_cleared,
                        resulting_grid=new_grid
                    )
                    
                    all_moves.append(move)
        
        # Return best move if any exist
        if all_moves:
            self.best_move = max(all_moves, key=lambda m: m.score)
            return self.best_move
        
        return None
    
    def get_top_moves(self, n: int = 5) -> List[Move]:
        """
        Get top N moves ranked by score.
        
        Args:
            n: Number of top moves to return
            
        Returns:
            List of top Move objects
        """
        all_moves = []
        
        for piece_idx, piece in enumerate(self.pieces):
            for orientation in piece.get_all_orientations():
                piece_cells = orientation.cells
                valid_positions = get_all_valid_placements(self.grid, piece_cells)
                
                for position in valid_positions:
                    new_grid = place_piece(self.grid, piece_cells, position)
                    new_grid, lines_cleared = clear_complete_lines(new_grid)
                    score = self.evaluate_position(new_grid, lines_cleared)
                    
                    move = Move(
                        piece_index=piece_idx,
                        position=position,
                        piece_cells=piece_cells,
                        score=score,
                        lines_cleared=lines_cleared,
                        resulting_grid=new_grid
                    )
                    
                    all_moves.append(move)
        
        # Sort by score and return top N
        all_moves.sort(key=lambda m: m.score, reverse=True)
        return all_moves[:n]


def solve_puzzle(grid: np.ndarray, pieces: List[BlockShape]) -> Optional[Move]:
    """
    Main entry point for solving a Block Blast puzzle.
    
    Args:
        grid: 8x8 boolean array representing current game state
        pieces: List of available BlockShape pieces
        
    Returns:
        Best Move or None if no moves available
    """
    solver = BlockBlastSolver(grid, pieces)
    return solver.find_best_move()
