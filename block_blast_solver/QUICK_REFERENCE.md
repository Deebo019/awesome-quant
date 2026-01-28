# 🚀 Block Blast Solver - Quick Reference Card

## Installation (One-Time Setup)

```bash
cd block_blast_solver
pip install -r requirements.txt
export OPENAI_API_KEY='your-api-key'
```

## Running the Application

```bash
# Method 1: Direct
streamlit run app.py

# Method 2: Using script
./run.sh
```

## Verify Setup

```bash
python verify_installation.py
python test_solver.py
```

## Quick Usage Guide

### 1. Demo Mode (Fastest - No API Key Needed)
1. Open app → Select "Demo Mode"
2. Click "Generate Demo Data"
3. Click "Find Best Move"

### 2. Screenshot Analysis (Requires API Key)
1. Take screenshot of Block Blast game
2. Upload → Click "Analyze Screenshot"
3. Click "Find Best Move"
4. Follow the yellow highlighted placement

### 3. Manual Entry
1. Select "Manual Entry"
2. Click cells to toggle them
3. Define pieces (format: `row,col`)
4. Click "Find Best Move"

## File Structure

```
block_blast_solver/
├── app.py              # Main application
├── solver.py           # Solving algorithm
├── image_analyzer.py   # Vision API
├── block_shapes.py     # Piece definitions
├── grid_renderer.py    # Visualization
├── utils.py           # Helpers
├── config.py          # Settings
├── requirements.txt   # Dependencies
├── README.md          # Full documentation
└── test_solver.py     # Tests
```

## Key Commands

```bash
# Run app
streamlit run app.py

# Test installation
python verify_installation.py

# Run tests
python test_solver.py

# View examples
python example_usage.py

# Generate sample
python generate_sample_screenshot.py
```

## API Quick Reference

```python
from block_blast_solver import *
import numpy as np

# Create grid
grid = np.zeros((8, 8), dtype=bool)

# Define pieces
pieces = [BlockShape([(0,0), (0,1)], "domino")]

# Solve
solver = BlockBlastSolver(grid, pieces)
move = solver.find_best_move()

# Get result
print(f"Place piece {move.piece_index} at {move.position}")
print(f"Score: {move.score:.2f}")
```

## Configuration

Edit `config.py`:

```python
GRID_SIZE = 8                    # Grid size
CELL_SIZE = 50                   # Render size (pixels)
COLOR_OCCUPIED = (67, 97, 238)   # Blue
SCORE_ROW_CLEAR = 100            # Line bonus
SCORE_HOLE_PENALTY = -10         # Hole penalty
```

## Understanding Scores

- **200+** = Excellent (clears lines)
- **100-200** = Good (sets up clears)
- **50-100** = Decent
- **<50** = Suboptimal

## Troubleshooting

| Problem | Solution |
|---------|----------|
| "No module named..." | `pip install -r requirements.txt` |
| "API key not found" | Set `OPENAI_API_KEY` environment variable |
| "Failed to analyze" | Use Manual Entry mode instead |
| "No valid moves" | Check grid and pieces are correct |

## Documentation Quick Links

- **Quick Start**: [QUICKSTART.md](QUICKSTART.md)
- **Full Guide**: [README.md](README.md)
- **Usage Details**: [USAGE.md](USAGE.md)
- **Architecture**: [PROJECT.md](PROJECT.md)
- **All Docs**: [INDEX.md](INDEX.md)

## Common Piece Formats

Manual entry format (row,col):

```
# Domino horizontal
0,0
0,1

# L-shape
0,0
1,0
1,1

# Single
0,0
```

## Keyboard Shortcuts (in app)

- `Ctrl+R` - Rerun app
- `Ctrl+Shift+R` - Clear cache
- `Esc` - Close dialogs

## Standard Pieces Available

- 1-cell: single
- 2-cell: dominoes
- 3-cell: lines, L-shapes
- 4-cell: square, T, L, Z
- 5-cell: lines, plus, extended

All with automatic rotations!

## Performance Tips

1. Use Manual Entry for speed
2. Demo Mode doesn't need API
3. Screenshot analysis: 2-5 seconds
4. Solving: <1 second
5. Cache is automatic

## Security Best Practices

1. Never commit `.env` file
2. Use environment variables
3. Or enter key in sidebar
4. Key is password-protected in UI

## Getting Help

1. Check [USAGE.md](USAGE.md) troubleshooting
2. Run `python verify_installation.py`
3. Run `python test_solver.py`
4. Check example: `python example_usage.py`

## Version Info

- **Version**: 1.0.0
- **Python**: 3.10+ required
- **Status**: Production Ready ✅

---

**Quick Start**: `streamlit run app.py` → Select Demo Mode → Generate Data → Find Best Move

**Need help?** See [INDEX.md](INDEX.md) for complete documentation navigation.

---

*Keep this card handy for quick reference!* 📋
