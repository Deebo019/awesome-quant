"""
Example usage of Block Blast Solver API.

This demonstrates how to use the solver programmatically
without the Streamlit UI.
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np
from block_blast_solver import (
    BlockShape, BlockBlastSolver, GridRenderer,
    STANDARD_PIECES
)


def example_1_basic_usage():
    """Example 1: Basic solver usage."""
    print("=" * 60)
    print("Example 1: Basic Solver Usage")
    print("=" * 60)
    
    # Create a simple grid with some occupied cells
    grid = np.zeros((8, 8), dtype=bool)
    grid[0, 0:3] = True  # Fill first 3 cells of row 0
    grid[1, 0:2] = True  # Fill first 2 cells of row 1
    
    print("\nCurrent grid:")
    for row in grid:
        print("  ", " ".join("█" if cell else "·" for cell in row))
    
    # Define available pieces
    pieces = [
        BlockShape([(0, 0), (0, 1)], "domino_h"),      # Horizontal domino
        BlockShape([(0, 0), (1, 0)], "domino_v"),      # Vertical domino
        BlockShape([(0, 0)], "single"),                # Single cell
    ]
    
    print(f"\nAvailable pieces: {len(pieces)}")
    for i, piece in enumerate(pieces):
        print(f"  Piece {i+1}: {piece.name} ({len(piece.cells)} cells)")
    
    # Solve
    print("\nSolving...")
    solver = BlockBlastSolver(grid, pieces)
    best_move = solver.find_best_move()
    
    if best_move:
        print(f"\n✓ Best move found!")
        print(f"  Place piece #{best_move.piece_index + 1} at position {best_move.position}")
        print(f"  Score: {best_move.score:.2f}")
        print(f"  Lines cleared: {best_move.lines_cleared}")
        
        print("\nGrid after move:")
        for row in best_move.resulting_grid:
            print("  ", " ".join("█" if cell else "·" for cell in row))
    else:
        print("\n✗ No valid moves available")
    
    print()


def example_2_line_clearing():
    """Example 2: Line clearing scenario."""
    print("=" * 60)
    print("Example 2: Line Clearing")
    print("=" * 60)
    
    # Create a grid with an almost-complete row
    grid = np.zeros((8, 8), dtype=bool)
    grid[0, 0:7] = True  # Fill first 7 cells of row 0 (one missing)
    
    print("\nCurrent grid (row 0 is almost complete):")
    for i, row in enumerate(grid):
        marker = " <-- Almost complete!" if i == 0 else ""
        print(f"  Row {i}: " + " ".join("█" if cell else "·" for cell in row) + marker)
    
    # Single piece that can complete the row
    pieces = [BlockShape([(0, 0)], "single")]
    
    print(f"\nAvailable: 1 single cell piece")
    
    # Solve
    solver = BlockBlastSolver(grid, pieces)
    best_move = solver.find_best_move()
    
    if best_move:
        print(f"\n✓ Best move: Place at position {best_move.position}")
        print(f"  Score: {best_move.score:.2f}")
        print(f"  Lines cleared: {best_move.lines_cleared} ⭐")
        
        print("\nGrid after move and line clear:")
        for i, row in enumerate(best_move.resulting_grid):
            marker = " <-- Row cleared!" if i == 0 else ""
            print(f"  Row {i}: " + " ".join("█" if cell else "·" for cell in row) + marker)
    
    print()


def example_3_multiple_pieces():
    """Example 3: Using standard pieces."""
    print("=" * 60)
    print("Example 3: Standard Pieces")
    print("=" * 60)
    
    # Create a grid
    grid = np.zeros((8, 8), dtype=bool)
    grid[0:2, 0:2] = True  # 2x2 square in corner
    grid[5, 5] = True      # Single cell
    
    print("\nCurrent grid:")
    for row in grid:
        print("  ", " ".join("█" if cell else "·" for cell in row))
    
    # Use some standard pieces
    pieces = [
        STANDARD_PIECES["line_3_h"],
        STANDARD_PIECES["l_3_1"],
        STANDARD_PIECES["square_4"],
    ]
    
    print(f"\nAvailable standard pieces: {len(pieces)}")
    for i, piece in enumerate(pieces):
        print(f"  {i+1}. {piece.name}")
    
    # Solve
    solver = BlockBlastSolver(grid, pieces)
    top_moves = solver.get_top_moves(3)
    
    print(f"\n✓ Found {len(top_moves)} possible moves")
    print("\nTop 3 moves:")
    for i, move in enumerate(top_moves):
        print(f"  {i+1}. Piece #{move.piece_index + 1} at {move.position} "
              f"(score: {move.score:.2f}, lines: {move.lines_cleared})")
    
    print()


def example_4_visualization():
    """Example 4: Using the renderer."""
    print("=" * 60)
    print("Example 4: Grid Visualization")
    print("=" * 60)
    
    # Create a grid
    grid = np.zeros((8, 8), dtype=bool)
    grid[0, 0:4] = True
    grid[1, 0:3] = True
    grid[2, 0:2] = True
    
    print("\nCreating visualization...")
    
    # Create renderer
    renderer = GridRenderer(cell_size=40)
    
    # Render grid
    grid_img = renderer.render_grid(grid)
    grid_img.save("/tmp/block_blast_grid.png")
    print("  ✓ Grid saved to /tmp/block_blast_grid.png")
    
    # Render with highlighted move
    highlight_cells = [(3, 3), (3, 4), (4, 3)]
    highlight_img = renderer.render_grid(grid, highlight_cells=highlight_cells)
    highlight_img.save("/tmp/block_blast_highlight.png")
    print("  ✓ Highlighted grid saved to /tmp/block_blast_highlight.png")
    
    # Render a piece
    piece = STANDARD_PIECES["l_3_1"]
    piece_img = renderer.render_piece(piece.cells)
    piece_img.save("/tmp/block_blast_piece.png")
    print("  ✓ Piece saved to /tmp/block_blast_piece.png")
    
    print(f"\nImage size: {grid_img.size[0]}x{grid_img.size[1]} pixels")
    print()


def example_5_complex_scenario():
    """Example 5: Complex game scenario."""
    print("=" * 60)
    print("Example 5: Complex Scenario")
    print("=" * 60)
    
    # Create a more complex grid
    grid = np.zeros((8, 8), dtype=bool)
    
    # Create a pattern
    grid[0, 0:6] = True      # Partial row
    grid[1, 0:4] = True      # Partial row
    grid[2:5, 0] = True      # Partial column
    grid[3, 2:6] = True      # Partial row
    grid[5:8, 5] = True      # Partial column
    
    print("\nComplex grid pattern:")
    for row in grid:
        print("  ", " ".join("█" if cell else "·" for cell in row))
    
    # Multiple pieces with different shapes
    pieces = [
        STANDARD_PIECES["line_3_h"],
        STANDARD_PIECES["l_4_1"],
        STANDARD_PIECES["t_4"],
    ]
    
    print(f"\nAvailable pieces: {len(pieces)}")
    
    # Solve and get top moves
    solver = BlockBlastSolver(grid, pieces)
    top_moves = solver.get_top_moves(5)
    
    print(f"\n✓ Found {len(top_moves)} possible moves")
    print("\nTop 5 moves ranked by score:")
    for i, move in enumerate(top_moves):
        piece = pieces[move.piece_index]
        print(f"\n  {i+1}. Score: {move.score:.2f}")
        print(f"     Piece: {piece.name}")
        print(f"     Position: {move.position}")
        print(f"     Lines cleared: {move.lines_cleared}")
        
        # Show cells occupied
        occupied = len(move.piece_cells)
        print(f"     Cells placed: {occupied}")
    
    # Show the best move visually
    if top_moves:
        best = top_moves[0]
        print("\n  Best move visualization:")
        
        # Show where the piece will be placed
        visual_grid = grid.copy()
        for dr, dc in best.piece_cells:
            r, c = best.position[0] + dr, best.position[1] + dc
            if 0 <= r < 8 and 0 <= c < 8:
                visual_grid[r, c] = True
        
        for row in visual_grid:
            print("    ", " ".join("█" if cell else "·" for cell in row))
    
    print()


def main():
    """Run all examples."""
    print("\n" + "=" * 60)
    print("Block Blast Solver - API Examples")
    print("=" * 60)
    print()
    
    example_1_basic_usage()
    input("Press Enter to continue to next example...")
    
    example_2_line_clearing()
    input("Press Enter to continue to next example...")
    
    example_3_multiple_pieces()
    input("Press Enter to continue to next example...")
    
    example_4_visualization()
    input("Press Enter to continue to next example...")
    
    example_5_complex_scenario()
    
    print("=" * 60)
    print("All examples completed!")
    print("=" * 60)
    print()


if __name__ == "__main__":
    main()
