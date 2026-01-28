"""
Image analysis using GPT-4o Vision API.
"""
import base64
import json
from typing import Optional, Dict, List, Tuple
from io import BytesIO
import os

from PIL import Image
import numpy as np

from config import VISION_PROMPT, OPENAI_MODEL, VISION_MAX_TOKENS, GRID_SIZE
from block_shapes import BlockShape, parse_piece_from_vision
from utils import list_to_grid


class VisionAnalyzer:
    """Analyzes Block Blast screenshots using GPT-4o Vision API."""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize vision analyzer.
        
        Args:
            api_key: OpenAI API key (if None, will try to get from environment)
        """
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        
        if not self.api_key:
            raise ValueError(
                "OpenAI API key not found. Set OPENAI_API_KEY environment variable "
                "or provide api_key parameter."
            )
        
        # Lazy import to avoid issues if openai not installed
        try:
            from openai import OpenAI
            self.client = OpenAI(api_key=self.api_key)
        except ImportError:
            raise ImportError(
                "openai package not installed. Run: pip install openai"
            )
    
    def encode_image(self, image: Image.Image) -> str:
        """
        Encode PIL Image to base64 string.
        
        Args:
            image: PIL Image object
            
        Returns:
            Base64 encoded image string
        """
        buffered = BytesIO()
        image.save(buffered, format="PNG")
        return base64.b64encode(buffered.getvalue()).decode('utf-8')
    
    def analyze_screenshot(self, image: Image.Image, 
                          retry_count: int = 3) -> Optional[Dict]:
        """
        Analyze a Block Blast screenshot.
        
        Args:
            image: PIL Image of the game screenshot
            retry_count: Number of retries on failure
            
        Returns:
            Dictionary with 'grid' (np.ndarray) and 'pieces' (List[BlockShape])
            or None if analysis fails
        """
        # Resize image if too large (to reduce API costs)
        max_size = 1024
        if max(image.size) > max_size:
            ratio = max_size / max(image.size)
            new_size = tuple(int(dim * ratio) for dim in image.size)
            image = image.resize(new_size, Image.Resampling.LANCZOS)
        
        base64_image = self.encode_image(image)
        
        for attempt in range(retry_count):
            try:
                response = self.client.chat.completions.create(
                    model=OPENAI_MODEL,
                    messages=[
                        {
                            "role": "user",
                            "content": [
                                {
                                    "type": "text",
                                    "text": VISION_PROMPT
                                },
                                {
                                    "type": "image_url",
                                    "image_url": {
                                        "url": f"data:image/png;base64,{base64_image}"
                                    }
                                }
                            ]
                        }
                    ],
                    max_tokens=VISION_MAX_TOKENS
                )
                
                # Parse the response
                content = response.choices[0].message.content
                
                # Extract JSON from response (GPT might add text around it)
                result = self._extract_json(content)
                
                if result:
                    # Validate and parse the result
                    parsed = self._parse_vision_result(result)
                    if parsed:
                        return parsed
                
            except Exception as e:
                print(f"Vision API error (attempt {attempt + 1}/{retry_count}): {e}")
                if attempt == retry_count - 1:
                    return None
        
        return None
    
    def _extract_json(self, text: str) -> Optional[Dict]:
        """
        Extract JSON from text that might contain other content.
        
        Args:
            text: Text potentially containing JSON
            
        Returns:
            Parsed JSON dictionary or None
        """
        # Try to find JSON in the text
        start = text.find('{')
        end = text.rfind('}')
        
        if start != -1 and end != -1:
            json_str = text[start:end+1]
            try:
                return json.loads(json_str)
            except json.JSONDecodeError:
                pass
        
        # Try parsing the whole text as JSON
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            return None
    
    def _parse_vision_result(self, result: Dict) -> Optional[Dict]:
        """
        Parse and validate vision API result.
        
        Args:
            result: Raw JSON result from Vision API
            
        Returns:
            Dictionary with validated grid and pieces, or None if invalid
        """
        try:
            # Parse grid
            grid_list = result.get('grid', [])
            
            if len(grid_list) != GRID_SIZE * GRID_SIZE:
                print(f"Invalid grid size: {len(grid_list)} (expected {GRID_SIZE * GRID_SIZE})")
                return None
            
            grid = list_to_grid(grid_list)
            
            # Parse pieces
            pieces_data = result.get('pieces', [])
            
            if not pieces_data or len(pieces_data) > 3:
                print(f"Invalid number of pieces: {len(pieces_data)} (expected 1-3)")
                return None
            
            pieces = []
            for i, piece_data in enumerate(pieces_data):
                try:
                    piece = parse_piece_from_vision(piece_data)
                    pieces.append(piece)
                except Exception as e:
                    print(f"Error parsing piece {i}: {e}")
                    return None
            
            return {
                'grid': grid,
                'pieces': pieces
            }
            
        except Exception as e:
            print(f"Error parsing vision result: {e}")
            return None


def create_sample_data() -> Dict:
    """
    Create sample data for testing without Vision API.
    
    Returns:
        Dictionary with sample grid and pieces
    """
    # Create a sample grid with some occupied cells
    grid = np.zeros((GRID_SIZE, GRID_SIZE), dtype=bool)
    
    # Add some random occupied cells
    grid[0, 0] = True
    grid[0, 1] = True
    grid[1, 0] = True
    grid[3, 3] = True
    grid[3, 4] = True
    grid[5, 5] = True
    
    # Create sample pieces
    pieces = [
        BlockShape([(0, 0), (0, 1)], "domino_h"),  # Horizontal domino
        BlockShape([(0, 0), (1, 0), (1, 1)], "l_shape"),  # L-shape
        BlockShape([(0, 0)], "single"),  # Single cell
    ]
    
    return {
        'grid': grid,
        'pieces': pieces
    }
