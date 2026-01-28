# 🚀 Quick Start Guide

Get up and running with Block Blast Solver in 5 minutes!

## Installation (1 minute)

```bash
cd block_blast_solver
pip install -r requirements.txt
```

## Setup API Key (1 minute)

Get an OpenAI API key from https://platform.openai.com/api-keys

Then set it up:

```bash
export OPENAI_API_KEY='your-key-here'
```

Or create a `.env` file:

```bash
echo "OPENAI_API_KEY=your-key-here" > .env
```

## Run the App (30 seconds)

```bash
streamlit run app.py
```

The app opens at `http://localhost:8501`

## Your First Solve (2 minutes)

### Option 1: Demo Mode (Fastest)
1. Select "Demo Mode" in sidebar
2. Click "Generate Demo Data"
3. Click "Find Best Move"
4. See the solution!

### Option 2: Upload Screenshot
1. Take a screenshot of your Block Blast game
2. Click "Upload Screenshot"
3. Upload your image
4. Click "Analyze Screenshot"
5. Click "Find Best Move"
6. Follow the highlighted suggestion!

### Option 3: Manual Entry
1. Select "Manual Entry"
2. Click cells to toggle them
3. Define your pieces (see coordinate format below)
4. Click "Find Best Move"

## Understanding the Output

The solver shows you:
- **Score**: Higher is better (200+ is excellent)
- **Position**: (row, col) where to place the piece
- **Visual**: Yellow cells show where to place

## Piece Coordinate Format

For manual entry, use `row,col` format:

```
0,0
0,1
1,0
```

This defines an L-shape:
```
█ █
█
```

## Tips

✅ **DO:**
- Use clear screenshots
- Prioritize moves with high scores
- Check "Top 5 Moves" for alternatives

❌ **DON'T:**
- Use blurry or partial screenshots
- Ignore the line clear opportunities
- Forget to set your API key

## Need Help?

- Run tests: `python test_solver.py`
- See examples: `python example_usage.py`
- Read full docs: `USAGE.md`
- Check README: `README.md`

## Next Steps

1. ✅ Try Demo Mode
2. ✅ Upload your first screenshot
3. ✅ Compare top 5 moves
4. ✅ Use Edit Mode to correct AI errors
5. ✅ Read USAGE.md for advanced features

---

**That's it! You're ready to solve Block Blast puzzles! 🎮**
