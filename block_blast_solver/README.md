# 🧩 Block Blast Solver

A complete puzzle solver application for Block Blast using Python, Streamlit, and GPT-4o Vision API.

## Features

- **🔍 AI-Powered Image Analysis**: Upload a screenshot and let GPT-4o Vision API extract the game state
- **🎯 Smart Solver Algorithm**: Finds optimal moves by maximizing line clears and minimizing board fragmentation
- **🎨 Visual Grid Renderer**: Beautiful PIL-based visualization of game states and moves
- **✏️ Manual Edit Mode**: Correct AI misinterpretations or manually enter game states
- **📊 Move Scoring**: See detailed evaluation metrics for suggested moves
- **🏆 Top Moves Ranking**: View top 5 best moves with visual previews

## Installation

### Prerequisites

- Python 3.10 or higher
- OpenAI API key (for Vision API access)

### Setup

1. Clone or download this repository:
```bash
cd block_blast_solver
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up your OpenAI API key (choose one method):

**Option A: Environment Variable**
```bash
export OPENAI_API_KEY='your-api-key-here'
```

**Option B: .env File**
Create a `.env` file in the project directory:
```
OPENAI_API_KEY=your-api-key-here
```

**Option C: Enter in App**
You can also enter the API key directly in the Streamlit sidebar when running the app.

## Usage

### Running the Application

Start the Streamlit app:
```bash
streamlit run app.py
```

The app will open in your default web browser at `http://localhost:8501`.

### Using the Solver

#### 1. Upload Screenshot Mode
- Take a screenshot of your Block Blast game
- Upload it using the file uploader
- Click "Analyze Screenshot" to extract game state
- Click "Find Best Move" to get the optimal move
- View the visual preview showing where to place the piece

#### 2. Manual Entry Mode
- Toggle cells to create your grid state
- Define available pieces using coordinate pairs
- Click "Find Best Move" to solve

#### 3. Demo Mode
- Click "Generate Demo Data" to try the solver with sample data
- Great for testing without a screenshot

### Understanding the Output

The solver provides:
- **Score**: Numerical evaluation of the move (higher is better)
- **Lines Cleared**: Number of rows/columns cleared by the move
- **Position**: Where to place the piece (row, column)
- **Visual Preview**: Side-by-side comparison of before/after states

## Architecture

### Module Overview

```
block_blast_solver/
├── app.py                 # Main Streamlit application
├── image_analyzer.py      # GPT-4o Vision API integration
├── block_shapes.py        # Block definitions and rotations
├── solver.py              # Core solving algorithm
├── grid_renderer.py       # PIL-based visualization
├── utils.py               # Helper functions
├── config.py              # Settings and constants
└── requirements.txt       # Python dependencies
```

### Key Components

#### `block_shapes.py`
- Defines all Block Blast piece types (single cells, dominoes, L-shapes, etc.)
- Handles piece rotations and reflections
- Supports all standard pieces plus custom shapes

#### `solver.py`
- Implements scoring heuristic based on:
  - Line clears (highest priority)
  - Hole avoidance (prevents isolated empty cells)
  - Board coverage (keeps maximum open space)
- Uses greedy algorithm with look-ahead evaluation

#### `image_analyzer.py`
- Interfaces with GPT-4o Vision API
- Extracts 8×8 grid state and available pieces
- Includes validation and retry logic
- Provides sample data fallback

#### `grid_renderer.py`
- Renders grids and pieces as PNG images
- Highlights best moves and previews
- Creates comparison visualizations

#### `app.py`
- Streamlit web interface
- Session state management
- Interactive grid editor
- Real-time solving and visualization

## Algorithm Details

### Scoring Heuristic

The solver evaluates moves using multiple criteria:

1. **Line Clears** (+100 points per line)
   - Prioritizes moves that clear complete rows/columns

2. **Hole Penalty** (-10 points per hole)
   - Avoids creating isolated empty cells

3. **Coverage Bonus** (up to +100 points)
   - Rewards keeping the board clear for future moves

4. **Near-Complete Lines** (+5 to +15 points)
   - Bonus for rows/columns close to completion

5. **Fragmentation Penalty** (-5 points per extra group)
   - Prefers contiguous empty space

### Block Shapes Supported

The solver supports all standard Block Blast pieces:

- **1-cell**: Single block
- **2-cell**: Horizontal/vertical dominoes
- **3-cell**: Lines, L-shapes in all rotations
- **4-cell**: Square, T-shape, L-shapes, Z-shapes
- **5-cell**: Long lines, plus shape, extended L-shapes

Each piece is automatically tested in all valid orientations.

## Configuration

Edit `config.py` to customize:

```python
# Grid settings
GRID_SIZE = 8
CELL_SIZE = 50  # Rendering size

# Colors (RGB tuples)
COLOR_OCCUPIED = (67, 97, 238)
COLOR_EMPTY = (240, 240, 245)
COLOR_HIGHLIGHT = (255, 193, 7)

# Solver scoring weights
SCORE_ROW_CLEAR = 100
SCORE_HOLE_PENALTY = -10
```

## API Usage

### Programmatic Usage

You can also use the solver programmatically:

```python
import numpy as np
from block_blast_solver import BlockBlastSolver, BlockShape

# Define grid (8×8 boolean array)
grid = np.zeros((8, 8), dtype=bool)
grid[0, 0] = True
grid[0, 1] = True

# Define available pieces
pieces = [
    BlockShape([(0, 0), (0, 1)], "domino"),
    BlockShape([(0, 0), (1, 0), (1, 1)], "l_shape"),
]

# Solve
solver = BlockBlastSolver(grid, pieces)
best_move = solver.find_best_move()

if best_move:
    print(f"Best move: Place piece {best_move.piece_index} at {best_move.position}")
    print(f"Score: {best_move.score:.2f}")
    print(f"Lines cleared: {best_move.lines_cleared}")
```

### Vision API Usage

```python
from PIL import Image
from block_blast_solver import VisionAnalyzer

# Initialize analyzer
analyzer = VisionAnalyzer(api_key="your-key-here")

# Analyze screenshot
img = Image.open("screenshot.png")
result = analyzer.analyze_screenshot(img)

if result:
    grid = result['grid']
    pieces = result['pieces']
    print(f"Extracted {len(pieces)} pieces")
```

## Troubleshooting

### Vision API Issues

**Problem**: "Failed to analyze screenshot"
- **Solution**: Ensure the screenshot clearly shows the 8×8 grid and available pieces
- Try using manual entry mode to verify the expected format
- Check that your API key is valid and has Vision API access

**Problem**: Incorrect grid extraction
- **Solution**: Use Edit Mode to manually correct misidentified cells
- Ensure the screenshot is high quality and well-lit
- Try cropping to just the game area

### Solver Issues

**Problem**: "No valid moves available"
- **Solution**: Verify that at least one piece can fit in at least one position
- Check that pieces are defined correctly (use the piece preview)

**Problem**: Solver is slow
- **Solution**: The solver tests all piece orientations and positions
- For complex scenarios with many options, this is expected
- Consider reducing MAX_SEARCH_DEPTH in config.py

## Performance

- **Vision API**: ~2-5 seconds per screenshot analysis
- **Solver**: <1 second for typical game states
- **Rendering**: <0.1 seconds per grid visualization

## Limitations

- Requires clear, unobstructed screenshots of the game
- Limited to 8×8 grid size (standard Block Blast)
- Vision API requires internet connection and API credits
- Solver uses greedy algorithm (doesn't look ahead multiple moves)

## Future Enhancements

Potential improvements:

- [ ] Multi-move look-ahead (planning sequences)
- [ ] Game state tracking (score, progress over time)
- [ ] OCR integration as fallback to Vision API
- [ ] Mobile app version
- [ ] Batch processing of multiple screenshots
- [ ] A/B testing of different scoring heuristics
- [ ] Real-time video feed analysis

## License

MIT License - feel free to use and modify for your own projects.

## Credits

Built with:
- [Streamlit](https://streamlit.io/) - Web interface
- [OpenAI GPT-4o Vision](https://openai.com/) - Image analysis
- [Pillow](https://python-pillow.org/) - Image processing
- [NumPy](https://numpy.org/) - Numerical computations

## Contributing

Contributions are welcome! Areas for improvement:

1. Better scoring heuristics
2. Additional block shape definitions
3. Improved Vision API prompts
4. UI/UX enhancements
5. Test coverage

## Support

For issues or questions:
1. Check the Troubleshooting section
2. Review the code documentation
3. Open an issue on the repository

---

**Happy solving! 🎮🧩**
