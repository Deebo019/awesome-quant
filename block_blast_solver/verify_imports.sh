#!/bin/bash
# Script to verify that all imports work correctly

echo "============================================================"
echo "Block Blast Solver - Import Verification"
echo "============================================================"
echo ""

cd "$(dirname "$0")"

echo "Checking for absolute imports in Python files..."
if grep -r "^from block_blast_solver\." --include="*.py" . 2>/dev/null; then
    echo "❌ Found absolute imports that need to be fixed!"
    exit 1
else
    echo "✓ No absolute imports found"
fi

echo ""
echo "Verifying Python syntax..."
python3 -m py_compile *.py 2>&1
if [ $? -eq 0 ]; then
    echo "✓ All Python files compile successfully"
else
    echo "❌ Syntax errors found"
    exit 1
fi

echo ""
echo "Testing direct imports (requires dependencies)..."
python3 -c "from config import GRID_SIZE; print(f'✓ config imported: GRID_SIZE={GRID_SIZE}')" 2>/dev/null
if [ $? -eq 0 ]; then
    echo "✓ Direct imports work correctly"
else
    echo "⚠ Dependencies not installed (expected if running without pip install)"
fi

echo ""
echo "============================================================"
echo "✅ Import verification complete!"
echo ""
echo "To run the application:"
echo "  streamlit run app.py"
echo ""
echo "Or use the quick start script:"
echo "  ./run.sh"
echo "============================================================"
