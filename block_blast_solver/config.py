"""
Configuration and constants for Block Blast Solver.
"""

# Grid settings
GRID_SIZE = 8
CELL_SIZE = 50  # pixels for rendering

# Colors for rendering (RGB)
COLOR_OCCUPIED = (67, 97, 238)  # Blue
COLOR_EMPTY = (240, 240, 245)  # Light gray
COLOR_HIGHLIGHT = (255, 193, 7)  # Amber for highlighting best move
COLOR_GRID_LINE = (200, 200, 200)  # Grid lines
COLOR_BLOCK_PREVIEW = (76, 175, 80)  # Green for block preview

# OpenAI API settings
OPENAI_MODEL = "gpt-4o"
VISION_MAX_TOKENS = 1000

# Solver settings
MAX_SEARCH_DEPTH = 3  # How many moves to look ahead
SCORE_ROW_CLEAR = 100  # Points for clearing a row
SCORE_COL_CLEAR = 100  # Points for clearing a column
SCORE_HOLE_PENALTY = -10  # Penalty for creating holes
SCORE_COVERAGE = 1  # Bonus for keeping board clear

# Vision API prompt
VISION_PROMPT = """Analyze this Block Blast game screenshot and extract:

1. The 8x8 game grid state (top-down, left-to-right)
   - Return as a list of 64 boolean values (true = occupied, false = empty)
   
2. The three available block pieces shown at the bottom
   - For each piece, provide the coordinates of occupied cells relative to a bounding box
   - Use format: [[x1,y1], [x2,y2], ...] where (0,0) is top-left

Return ONLY valid JSON in this exact format:
{
  "grid": [true, false, true, ...],  // 64 values
  "pieces": [
    {"cells": [[0,0], [0,1]]},       // piece 1
    {"cells": [[0,0], [1,0], [1,1]]}, // piece 2
    {"cells": [[0,0]]}                // piece 3
  ]
}

Be precise with cell positions. Empty cells should be false, occupied cells should be true."""
