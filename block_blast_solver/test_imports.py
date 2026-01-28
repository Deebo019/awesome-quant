#!/usr/bin/env python3
"""
Test script to verify all imports work correctly.
"""
import sys

def test_direct_imports():
    """Test direct imports from within the block_blast_solver directory."""
    print("Testing direct imports...")
    try:
        from config import GRID_SIZE
        print(f"  ✓ config: GRID_SIZE = {GRID_SIZE}")
        
        from block_shapes import BlockShape, STANDARD_PIECES
        print(f"  ✓ block_shapes: {len(STANDARD_PIECES)} standard pieces")
        
        from utils import validate_grid
        print("  ✓ utils: validate_grid imported")
        
        from solver import BlockBlastSolver, Move
        print("  ✓ solver: BlockBlastSolver and Move imported")
        
        from image_analyzer import VisionAnalyzer, create_sample_data
        print("  ✓ image_analyzer: VisionAnalyzer and create_sample_data imported")
        
        from grid_renderer import GridRenderer, render_pieces_row
        print("  ✓ grid_renderer: GridRenderer and render_pieces_row imported")
        
        print("\n✅ All direct imports working correctly!")
        return True
        
    except Exception as e:
        print(f"\n❌ Import failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_functionality():
    """Test basic functionality."""
    print("\nTesting basic functionality...")
    try:
        import numpy as np
        from block_shapes import BlockShape
        from solver import BlockBlastSolver
        from config import GRID_SIZE
        
        # Create a simple test case
        grid = np.zeros((GRID_SIZE, GRID_SIZE), dtype=bool)
        pieces = [BlockShape([(0, 0)], "test")]
        solver = BlockBlastSolver(grid, pieces)
        move = solver.find_best_move()
        
        if move is not None:
            print("  ✓ Solver found a move")
            print(f"    Position: {move.position}")
            print(f"    Score: {move.score:.2f}")
        else:
            print("  ✗ No move found (unexpected)")
            return False
        
        print("\n✅ Basic functionality test passed!")
        return True
        
    except Exception as e:
        print(f"\n❌ Functionality test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all tests."""
    print("=" * 60)
    print("Block Blast Solver - Import Test")
    print("=" * 60)
    print()
    
    # Test imports
    import_success = test_direct_imports()
    
    if not import_success:
        print("\nImports failed. Cannot proceed with functionality tests.")
        return 1
    
    # Test functionality
    func_success = test_functionality()
    
    print()
    print("=" * 60)
    if import_success and func_success:
        print("✅ ALL TESTS PASSED")
        print("\nYou can now run the app with:")
        print("  streamlit run app.py")
    else:
        print("❌ SOME TESTS FAILED")
        print("\nPlease check the errors above.")
    print("=" * 60)
    
    return 0 if (import_success and func_success) else 1

if __name__ == "__main__":
    sys.exit(main())
