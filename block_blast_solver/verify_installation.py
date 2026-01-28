"""
Installation verification script for Block Blast Solver.

Run this script to verify that all dependencies are installed
and the application is ready to use.
"""
import sys
import os

def check_python_version():
    """Check if Python version is 3.10 or higher."""
    version = sys.version_info
    if version.major >= 3 and version.minor >= 10:
        print(f"✓ Python {version.major}.{version.minor}.{version.micro} (OK)")
        return True
    else:
        print(f"✗ Python {version.major}.{version.minor}.{version.micro} (Need 3.10+)")
        return False

def check_import(module_name, package_name=None):
    """Check if a module can be imported."""
    if package_name is None:
        package_name = module_name
    
    try:
        __import__(module_name)
        print(f"✓ {package_name} (installed)")
        return True
    except ImportError:
        print(f"✗ {package_name} (missing)")
        return False

def check_api_key():
    """Check if OpenAI API key is set."""
    key = os.getenv('OPENAI_API_KEY')
    if key:
        print(f"✓ OPENAI_API_KEY (set)")
        return True
    else:
        print(f"⚠ OPENAI_API_KEY (not set - you can enter it in the app)")
        return False

def check_file_exists(filename):
    """Check if a required file exists."""
    # Get the directory where this script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    filepath = os.path.join(script_dir, filename)
    
    if os.path.exists(filepath):
        print(f"✓ {filename} (found)")
        return True
    else:
        print(f"✗ {filename} (missing)")
        return False

def main():
    """Run all verification checks."""
    print("=" * 60)
    print("Block Blast Solver - Installation Verification")
    print("=" * 60)
    print()
    
    all_ok = True
    
    # Check Python version
    print("Checking Python version...")
    all_ok &= check_python_version()
    print()
    
    # Check required packages
    print("Checking required packages...")
    all_ok &= check_import('numpy', 'numpy')
    all_ok &= check_import('PIL', 'Pillow')
    all_ok &= check_import('streamlit', 'streamlit')
    all_ok &= check_import('openai', 'openai')
    all_ok &= check_import('dotenv', 'python-dotenv')
    print()
    
    # Check core modules
    print("Checking core modules...")
    try:
        from block_shapes import BlockShape
        from solver import BlockBlastSolver
        from image_analyzer import VisionAnalyzer
        from grid_renderer import GridRenderer
        from utils import validate_grid
        print("✓ All core modules (OK)")
        print()
    except ImportError as e:
        print(f"✗ Core modules import failed: {e}")
        all_ok = False
        print()
    
    # Check required files
    print("Checking required files...")
    all_ok &= check_file_exists('app.py')
    all_ok &= check_file_exists('solver.py')
    all_ok &= check_file_exists('image_analyzer.py')
    all_ok &= check_file_exists('block_shapes.py')
    all_ok &= check_file_exists('grid_renderer.py')
    all_ok &= check_file_exists('requirements.txt')
    print()
    
    # Check API key
    print("Checking API configuration...")
    check_api_key()
    print()
    
    # Run a quick functional test
    print("Running functional tests...")
    try:
        import numpy as np
        from block_shapes import BlockShape
        from solver import BlockBlastSolver
        
        # Create a simple test case
        grid = np.zeros((8, 8), dtype=bool)
        pieces = [BlockShape([(0, 0)], "test")]
        solver = BlockBlastSolver(grid, pieces)
        move = solver.find_best_move()
        
        if move is not None:
            print("✓ Solver functional test (passed)")
        else:
            print("✗ Solver functional test (failed)")
            all_ok = False
    except Exception as e:
        print(f"✗ Functional test error: {e}")
        all_ok = False
    
    print()
    print("=" * 60)
    
    if all_ok:
        print("✅ All checks passed! The application is ready to use.")
        print()
        print("To start the application, run:")
        print("  streamlit run app.py")
        print()
        print("Or use the quick start script:")
        print("  ./run.sh")
    else:
        print("⚠️  Some checks failed. Please review the errors above.")
        print()
        print("To install missing dependencies:")
        print("  pip install -r requirements.txt")
        print()
        print("To set API key:")
        print("  export OPENAI_API_KEY='your-key-here'")
    
    print("=" * 60)
    
    return 0 if all_ok else 1

if __name__ == "__main__":
    sys.exit(main())
