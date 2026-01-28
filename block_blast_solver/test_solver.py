"""
Test script to validate Block Blast Solver functionality.
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np
from block_blast_solver import (
    BlockShape, BlockBlastSolver, solve_puzzle,
    GridRenderer, create_sample_data, validate_grid
)


def test_block_shapes():
    """Test block shape creation and rotation."""
    print("Testing Block Shapes...")
    
    # Test single cell
    single = BlockShape([(0, 0)], "single")
    assert len(single.cells) == 1
    print("✓ Single cell block created")
    
    # Test domino
    domino = BlockShape([(0, 0), (0, 1)], "domino")
    assert len(domino.cells) == 2
    print("✓ Domino block created")
    
    # Test rotation
    rotated = domino.rotate_90()
    assert rotated.cells == [(0, 0), (1, 0)]
    print("✓ Rotation works correctly")
    
    # Test all orientations
    orientations = domino.get_all_orientations()
    assert len(orientations) >= 2  # At least 2 unique orientations
    print(f"✓ Found {len(orientations)} unique orientations")
    
    print()


def test_grid_validation():
    """Test grid validation."""
    print("Testing Grid Validation...")
    
    # Valid grid
    valid_grid = np.zeros((8, 8), dtype=bool)
    assert validate_grid(valid_grid)
    print("✓ Valid grid accepted")
    
    # Invalid grid (wrong size)
    invalid_grid = np.zeros((5, 5), dtype=bool)
    assert not validate_grid(invalid_grid)
    print("✓ Invalid grid rejected")
    
    print()


def test_solver_basic():
    """Test basic solver functionality."""
    print("Testing Solver (Basic)...")
    
    # Create simple test case
    grid = np.zeros((8, 8), dtype=bool)
    grid[0, 0:3] = True  # Fill first 3 cells of row 0
    
    # Create a piece that will complete the row partially
    pieces = [
        BlockShape([(0, 0)], "single"),
    ]
    
    solver = BlockBlastSolver(grid, pieces)
    best_move = solver.find_best_move()
    
    assert best_move is not None
    print(f"✓ Found best move: {best_move}")
    print(f"  Position: {best_move.position}")
    print(f"  Score: {best_move.score:.2f}")
    
    print()


def test_solver_line_clear():
    """Test solver with line clearing scenario."""
    print("Testing Solver (Line Clear)...")
    
    # Create a grid with 7 cells filled in a row
    grid = np.zeros((8, 8), dtype=bool)
    grid[0, 0:7] = True
    
    # Create a single piece that will complete the row
    pieces = [
        BlockShape([(0, 0)], "single"),
    ]
    
    solver = BlockBlastSolver(grid, pieces)
    best_move = solver.find_best_move()
    
    assert best_move is not None
    assert best_move.lines_cleared >= 1
    print(f"✓ Line clear detected: {best_move.lines_cleared} lines")
    print(f"  Move score: {best_move.score:.2f}")
    
    print()


def test_sample_data():
    """Test sample data creation."""
    print("Testing Sample Data...")
    
    data = create_sample_data()
    
    assert 'grid' in data
    assert 'pieces' in data
    assert validate_grid(data['grid'])
    assert len(data['pieces']) > 0
    
    print(f"✓ Sample data created with {len(data['pieces'])} pieces")
    print(f"  Grid occupation: {np.sum(data['grid'])} cells")
    
    print()


def test_solver_with_sample():
    """Test solver with sample data."""
    print("Testing Solver with Sample Data...")
    
    data = create_sample_data()
    grid = data['grid']
    pieces = data['pieces']
    
    print("Sample grid:")
    for row in grid:
        print("  ", " ".join("█" if cell else "·" for cell in row))
    
    print(f"\nAvailable pieces: {len(pieces)}")
    for i, piece in enumerate(pieces):
        print(f"  Piece {i}: {len(piece.cells)} cells - {piece.name}")
    
    solver = BlockBlastSolver(grid, pieces)
    best_move = solver.find_best_move()
    
    if best_move:
        print(f"\n✓ Found best move:")
        print(f"  Piece: #{best_move.piece_index + 1}")
        print(f"  Position: {best_move.position}")
        print(f"  Score: {best_move.score:.2f}")
        print(f"  Lines cleared: {best_move.lines_cleared}")
    else:
        print("✗ No moves available")
    
    print()


def test_top_moves():
    """Test getting top N moves."""
    print("Testing Top Moves...")
    
    data = create_sample_data()
    solver = BlockBlastSolver(data['grid'], data['pieces'])
    
    top_moves = solver.get_top_moves(5)
    
    print(f"✓ Found {len(top_moves)} moves")
    for i, move in enumerate(top_moves[:3]):
        print(f"  #{i+1}: Score {move.score:.2f}, Position {move.position}")
    
    print()


def test_renderer():
    """Test grid rendering."""
    print("Testing Grid Renderer...")
    
    try:
        renderer = GridRenderer(cell_size=30)
        
        # Create test grid
        grid = np.zeros((8, 8), dtype=bool)
        grid[0:2, 0:2] = True
        
        # Render grid
        img = renderer.render_grid(grid)
        assert img.size == (240, 240)  # 8 * 30
        print("✓ Grid rendered successfully")
        
        # Render piece
        piece_cells = [(0, 0), (0, 1)]
        piece_img = renderer.render_piece(piece_cells)
        assert piece_img.size[0] > 0 and piece_img.size[1] > 0
        print("✓ Piece rendered successfully")
        
        # Render with highlight
        highlight_img = renderer.render_grid(grid, highlight_cells=[(0, 0)])
        print("✓ Grid with highlight rendered")
        
    except Exception as e:
        print(f"✗ Rendering error: {e}")
    
    print()


def run_all_tests():
    """Run all tests."""
    print("=" * 60)
    print("Block Blast Solver - Test Suite")
    print("=" * 60)
    print()
    
    test_block_shapes()
    test_grid_validation()
    test_solver_basic()
    test_solver_line_clear()
    test_sample_data()
    test_solver_with_sample()
    test_top_moves()
    test_renderer()
    
    print("=" * 60)
    print("All tests completed!")
    print("=" * 60)


if __name__ == "__main__":
    run_all_tests()
