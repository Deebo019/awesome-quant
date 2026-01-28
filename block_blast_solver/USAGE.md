# Block Blast Solver - Usage Guide

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set Up API Key

Choose one of these methods:

**Method A: Environment Variable**
```bash
export OPENAI_API_KEY='sk-your-key-here'
```

**Method B: .env File**
```bash
cp .env.example .env
# Edit .env and add your API key
```

**Method C: In-App Entry**
- Enter your API key in the Streamlit sidebar when the app starts

### 3. Run the Application

**Option 1: Using the run script**
```bash
./run.sh
```

**Option 2: Direct streamlit command**
```bash
streamlit run app.py
```

The app will open at `http://localhost:8501`

## Application Modes

### 📤 Upload Screenshot Mode

1. Click "Upload Screenshot" in the sidebar
2. Choose a PNG/JPG file of your Block Blast game
3. Click "Analyze Screenshot" to extract game state
4. Review the extracted grid and pieces
5. Click "Find Best Move" to get the solution
6. View the highlighted move and evaluation

**Tips for best results:**
- Use high-resolution screenshots
- Ensure the entire 8×8 grid is visible
- Include all three piece options at the bottom
- Avoid shadows or glare on the screen
- Crop to just the game area if possible

### ✏️ Manual Entry Mode

1. Select "Manual Entry" in the sidebar
2. Click cells in the grid editor to toggle occupied/empty
3. Define your pieces:
   - Enter cell coordinates as `row,col` pairs
   - One pair per line
   - Example:
     ```
     0,0
     0,1
     1,0
     ```
4. Click "Find Best Move"

**Coordinate System:**
- (0,0) is top-left
- First number is row (0-7 from top to bottom)
- Second number is column (0-7 from left to right)

### 📊 Demo Mode

1. Select "Demo Mode" in the sidebar
2. Click "Generate Demo Data"
3. Experiment with the solver using sample data

## Understanding the Output

### Move Score

The score indicates how good the move is. Higher is better.

**Score Components:**
- **+100 per line cleared** - Main priority
- **-10 per hole created** - Avoid isolated empty cells
- **+1 to +100 for coverage** - Keep board clear
- **+5 to +15 bonus** - For rows/columns close to complete

**Example Scores:**
- `200+` - Excellent (clears lines)
- `100-200` - Good (sets up future clears)
- `50-100` - Decent (maintains board state)
- `<50` - Suboptimal (may create problems)

### Move Details

The app displays:

1. **Score** - Overall move quality
2. **Lines Cleared** - Number of rows/columns cleared (0-16 max)
3. **Piece Number** - Which of the 3 available pieces (1, 2, or 3)
4. **Position** - (row, col) where to place the piece's origin

### Visual Preview

- **Before Move** - Current grid with highlighted placement
  - Yellow/amber cells show where the piece will go
  
- **After Move** - Grid state after placement and line clears
  - Shows the final state you'll have after the move

## Advanced Features

### Edit Mode

If the AI misidentifies your grid:

1. Toggle "Edit Mode" in the sidebar
2. Click cells to correct them
3. Turn off Edit Mode
4. Click "Find Best Move" again

### Top 5 Moves

Check the "Show Top 5 Moves" box to see:
- Alternative move options
- Comparison of different strategies
- Backup plans if your first choice doesn't work out

### Multiple Orientations

The solver automatically:
- Tries all rotations (90°, 180°, 270°)
- Tests horizontal and vertical flips
- Finds all unique placements

You don't need to manually rotate pieces!

## Programmatic Usage

### Basic Example

```python
import numpy as np
from block_blast_solver import BlockShape, BlockBlastSolver

# Create grid
grid = np.zeros((8, 8), dtype=bool)
grid[0, 0:3] = True

# Create pieces
pieces = [
    BlockShape([(0, 0), (0, 1)], "domino"),
    BlockShape([(0, 0)], "single"),
]

# Solve
solver = BlockBlastSolver(grid, pieces)
best_move = solver.find_best_move()

print(f"Place piece {best_move.piece_index} at {best_move.position}")
print(f"Score: {best_move.score:.2f}")
```

### Using Standard Pieces

```python
from block_blast_solver import STANDARD_PIECES

pieces = [
    STANDARD_PIECES["line_3_h"],
    STANDARD_PIECES["l_4_1"],
    STANDARD_PIECES["square_4"],
]
```

### Vision API

```python
from PIL import Image
from block_blast_solver import VisionAnalyzer

analyzer = VisionAnalyzer(api_key="your-key")
result = analyzer.analyze_screenshot(Image.open("screenshot.png"))

if result:
    grid = result['grid']
    pieces = result['pieces']
```

### Rendering

```python
from block_blast_solver import GridRenderer

renderer = GridRenderer(cell_size=50)
img = renderer.render_grid(grid, highlight_cells=[(0, 0), (0, 1)])
img.save("output.png")
```

## Tips and Tricks

### Getting Better Screenshots

1. **Use Device Screenshots** - Better than photos of screens
2. **Full Screen** - Maximize the game before capturing
3. **Clean Interface** - Hide notifications or overlays
4. **Good Lighting** - If photographing a screen
5. **Steady Hand** - Avoid blurry photos

### Strategy Tips

1. **Line Clears First** - Always prioritize moves that clear lines
2. **Avoid Holes** - Don't create isolated empty cells
3. **Think Ahead** - Check the top 5 moves for alternative strategies
4. **Corner Awareness** - Corners are hardest to clear
5. **Keep Options Open** - Maintain as much empty space as possible

### Performance Optimization

For faster solving:
1. Use Manual Entry for quick puzzles
2. Close other apps to free memory
3. Use smaller screenshots (API processes faster)
4. Cache your API key (don't re-enter each time)

## Troubleshooting

### "Failed to analyze screenshot"

**Possible causes:**
- Screenshot doesn't show the full grid
- Image is too blurry or low resolution
- Game UI is different from expected format
- API rate limit reached

**Solutions:**
- Retake a clearer screenshot
- Use Manual Entry mode instead
- Check your internet connection
- Verify API key is valid

### "No valid moves available"

**Causes:**
- All positions are filled
- Pieces are too large for remaining space
- Grid or pieces were entered incorrectly

**Solutions:**
- Check grid state in Edit Mode
- Verify piece definitions
- Try Demo Mode to ensure solver works

### Vision API Errors

**"API key not found"**
- Set OPENAI_API_KEY environment variable
- Or enter key in sidebar

**"Rate limit exceeded"**
- Wait a moment before trying again
- Check your OpenAI account usage

**"Invalid response format"**
- Screenshot may be unclear
- Try Manual Entry mode
- Check that screenshot shows Block Blast game

### Import Errors

**"No module named 'streamlit'"**
```bash
pip install -r requirements.txt
```

**"No module named 'block_blast_solver'"**
```bash
# Run from the parent directory
cd /path/to/project
python block_blast_solver/app.py
```

## API Reference

### BlockShape

```python
BlockShape(cells: List[Tuple[int, int]], name: str = "")
```

**Methods:**
- `rotate_90()` - Rotate 90° clockwise
- `rotate_180()` - Rotate 180°
- `rotate_270()` - Rotate 270° clockwise
- `flip_horizontal()` - Mirror horizontally
- `flip_vertical()` - Mirror vertically
- `get_all_orientations()` - Get all unique rotations/flips

### BlockBlastSolver

```python
BlockBlastSolver(grid: np.ndarray, pieces: List[BlockShape])
```

**Methods:**
- `find_best_move()` - Returns best Move or None
- `get_top_moves(n: int = 5)` - Returns list of top N moves
- `evaluate_position(grid, lines_cleared)` - Returns score for position

### Move

**Attributes:**
- `piece_index` - Which piece (0, 1, or 2)
- `position` - (row, col) placement position
- `piece_cells` - List of (row, col) offsets
- `score` - Evaluated score
- `lines_cleared` - Number of lines cleared
- `resulting_grid` - Grid state after move

### GridRenderer

```python
GridRenderer(cell_size: int = 50)
```

**Methods:**
- `render_grid(grid, highlight_cells, preview_cells)` - Render grid as PIL Image
- `render_piece(piece_cells, color)` - Render piece as PIL Image
- `render_grid_with_move(grid, move_cells, move_position)` - Render move preview

### VisionAnalyzer

```python
VisionAnalyzer(api_key: Optional[str] = None)
```

**Methods:**
- `analyze_screenshot(image: Image, retry_count: int = 3)` - Returns dict with 'grid' and 'pieces'

## Examples

See `example_usage.py` for comprehensive examples:

```bash
python example_usage.py
```

Run the test suite:

```bash
python test_solver.py
```

## Configuration

Edit `config.py` to customize:

- Grid size (default: 8×8)
- Cell rendering size
- Colors for visualization
- Scoring weights
- Vision API parameters

## Performance

**Typical Performance:**
- Vision API analysis: 2-5 seconds
- Solver computation: <1 second
- Grid rendering: <0.1 seconds

**Optimization:**
- Results are cached in session state
- Block orientations are pre-computed
- Only valid placements are evaluated

## Getting Help

1. Check this usage guide
2. Read the README.md
3. Run the test suite to verify installation
4. Try example_usage.py for code examples
5. Use Demo Mode to verify functionality

---

**Version:** 1.0.0  
**Last Updated:** 2024
