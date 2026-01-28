"""
Main Streamlit application for Block Blast Solver.
"""
import streamlit as st
import numpy as np
from PIL import Image
import os
from typing import Optional, List, Tuple

from image_analyzer import VisionAnalyzer, create_sample_data
from solver import BlockBlastSolver, Move
from grid_renderer import GridRenderer, render_pieces_row
from block_shapes import BlockShape
from config import GRID_SIZE
from utils import validate_grid


# Page configuration
st.set_page_config(
    page_title="Block Blast Solver",
    page_icon="🧩",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #4361ee;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.5rem;
        font-weight: bold;
        color: #3a0ca3;
        margin-top: 1rem;
        margin-bottom: 0.5rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)


def initialize_session_state():
    """Initialize Streamlit session state variables."""
    if 'grid' not in st.session_state:
        st.session_state.grid = None
    if 'pieces' not in st.session_state:
        st.session_state.pieces = None
    if 'best_move' not in st.session_state:
        st.session_state.best_move = None
    if 'uploaded_image' not in st.session_state:
        st.session_state.uploaded_image = None
    if 'edit_mode' not in st.session_state:
        st.session_state.edit_mode = False
    if 'api_key' not in st.session_state:
        st.session_state.api_key = os.getenv('OPENAI_API_KEY', '')


def render_grid_editor(grid: np.ndarray) -> np.ndarray:
    """
    Render an interactive grid editor.
    
    Args:
        grid: Current grid state
        
    Returns:
        Updated grid state
    """
    st.markdown('<div class="sub-header">Grid Editor (Click to Toggle Cells)</div>', 
                unsafe_allow_html=True)
    
    edited_grid = grid.copy()
    
    # Create a grid of checkboxes
    cols_per_row = GRID_SIZE
    
    for row in range(GRID_SIZE):
        cols = st.columns(cols_per_row)
        for col in range(GRID_SIZE):
            with cols[col]:
                # Use a unique key for each cell
                key = f"cell_{row}_{col}"
                new_value = st.checkbox(
                    label="",
                    value=bool(edited_grid[row, col]),
                    key=key,
                    label_visibility="collapsed"
                )
                edited_grid[row, col] = new_value
    
    return edited_grid


def display_move_details(move: Move):
    """Display detailed information about a move."""
    st.markdown('<div class="sub-header">Move Details</div>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Score", f"{move.score:.2f}")
    
    with col2:
        st.metric("Lines Cleared", move.lines_cleared)
    
    with col3:
        st.metric("Piece", f"#{move.piece_index + 1}")
    
    with col4:
        st.metric("Position", f"({move.position[0]}, {move.position[1]})")
    
    # Show piece shape
    st.markdown("**Piece Shape:**")
    renderer = GridRenderer(cell_size=30)
    piece_img = renderer.render_piece(move.piece_cells)
    st.image(piece_img, width=150)


def main():
    """Main application function."""
    initialize_session_state()
    
    # Header
    st.markdown('<div class="main-header">🧩 Block Blast Solver</div>', 
                unsafe_allow_html=True)
    st.markdown("Upload a screenshot of your Block Blast game and get the best move!")
    
    # Sidebar
    with st.sidebar:
        st.header("⚙️ Settings")
        
        # API Key input
        api_key_input = st.text_input(
            "OpenAI API Key",
            value=st.session_state.api_key,
            type="password",
            help="Enter your OpenAI API key or set OPENAI_API_KEY environment variable"
        )
        
        if api_key_input:
            st.session_state.api_key = api_key_input
            os.environ['OPENAI_API_KEY'] = api_key_input
        
        st.divider()
        
        # Mode selection
        st.header("🎮 Mode")
        mode = st.radio(
            "Choose input mode:",
            ["Upload Screenshot", "Manual Entry", "Demo Mode"],
            help="Upload a screenshot, manually enter the grid, or try demo mode"
        )
        
        st.divider()
        
        # Edit mode toggle
        if st.session_state.grid is not None:
            st.session_state.edit_mode = st.toggle(
                "✏️ Edit Mode",
                value=st.session_state.edit_mode,
                help="Toggle to manually edit the grid"
            )
    
    # Main content
    if mode == "Demo Mode":
        st.info("📊 Demo Mode: Using sample data to demonstrate the solver.")
        
        if st.button("Generate Demo Data"):
            data = create_sample_data()
            st.session_state.grid = data['grid']
            st.session_state.pieces = data['pieces']
            st.session_state.best_move = None
            st.success("Demo data loaded!")
            st.rerun()
    
    elif mode == "Upload Screenshot":
        st.header("📤 Upload Screenshot")
        
        uploaded_file = st.file_uploader(
            "Choose a Block Blast screenshot",
            type=['png', 'jpg', 'jpeg'],
            help="Upload a clear screenshot of your Block Blast game"
        )
        
        if uploaded_file is not None:
            st.session_state.uploaded_image = Image.open(uploaded_file)
            
            # Display uploaded image
            st.image(st.session_state.uploaded_image, 
                    caption="Uploaded Screenshot", 
                    width=300)
            
            # Analyze button
            if st.button("🔍 Analyze Screenshot", type="primary"):
                if not st.session_state.api_key:
                    st.error("⚠️ Please enter your OpenAI API key in the sidebar!")
                else:
                    with st.spinner("Analyzing screenshot with GPT-4o Vision..."):
                        try:
                            analyzer = VisionAnalyzer(api_key=st.session_state.api_key)
                            result = analyzer.analyze_screenshot(st.session_state.uploaded_image)
                            
                            if result:
                                st.session_state.grid = result['grid']
                                st.session_state.pieces = result['pieces']
                                st.session_state.best_move = None
                                st.success("✅ Analysis complete!")
                                st.rerun()
                            else:
                                st.error("❌ Failed to analyze screenshot. Try manual entry or check your image.")
                        except Exception as e:
                            st.error(f"❌ Error: {str(e)}")
    
    elif mode == "Manual Entry":
        st.header("✏️ Manual Entry")
        st.info("Create a grid manually by toggling cells below.")
        
        if st.session_state.grid is None:
            st.session_state.grid = np.zeros((GRID_SIZE, GRID_SIZE), dtype=bool)
        
        # Show grid editor
        st.session_state.grid = render_grid_editor(st.session_state.grid)
        
        # Manual piece entry
        st.markdown('<div class="sub-header">Available Pieces</div>', 
                   unsafe_allow_html=True)
        
        num_pieces = st.number_input("Number of pieces", min_value=1, max_value=3, value=3)
        
        pieces = []
        for i in range(num_pieces):
            with st.expander(f"Piece {i + 1}"):
                cells_input = st.text_area(
                    f"Cells for piece {i + 1}",
                    value="0,0\n0,1",
                    help="Enter cells as row,col pairs (one per line)",
                    key=f"piece_{i}"
                )
                
                try:
                    cells = []
                    for line in cells_input.strip().split('\n'):
                        if line.strip():
                            r, c = map(int, line.split(','))
                            cells.append((r, c))
                    
                    if cells:
                        piece = BlockShape(cells, f"manual_{i}")
                        pieces.append(piece)
                        
                        # Preview piece
                        renderer = GridRenderer(cell_size=30)
                        piece_img = renderer.render_piece(piece.cells)
                        st.image(piece_img, width=150)
                except Exception as e:
                    st.error(f"Invalid format: {e}")
        
        if pieces:
            st.session_state.pieces = pieces
    
    # Display current state and solve
    if st.session_state.grid is not None and st.session_state.pieces is not None:
        st.divider()
        
        # Edit mode
        if st.session_state.edit_mode:
            st.markdown('<div class="sub-header">Edit Grid</div>', 
                       unsafe_allow_html=True)
            st.session_state.grid = render_grid_editor(st.session_state.grid)
        
        # Display grid and pieces
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<div class="sub-header">Current Grid</div>', 
                       unsafe_allow_html=True)
            renderer = GridRenderer()
            grid_img = renderer.render_grid(st.session_state.grid)
            st.image(grid_img, use_container_width=True)
        
        with col2:
            st.markdown('<div class="sub-header">Available Pieces</div>', 
                       unsafe_allow_html=True)
            piece_cells = [piece.cells for piece in st.session_state.pieces]
            pieces_img = render_pieces_row(piece_cells)
            st.image(pieces_img, use_container_width=True)
        
        # Solve button
        if st.button("🎯 Find Best Move", type="primary"):
            with st.spinner("Solving puzzle..."):
                try:
                    solver = BlockBlastSolver(
                        st.session_state.grid,
                        st.session_state.pieces
                    )
                    best_move = solver.find_best_move()
                    
                    if best_move:
                        st.session_state.best_move = best_move
                        st.success("✅ Best move found!")
                        st.rerun()
                    else:
                        st.warning("⚠️ No valid moves available!")
                except Exception as e:
                    st.error(f"❌ Error solving puzzle: {str(e)}")
        
        # Display best move
        if st.session_state.best_move is not None:
            st.divider()
            st.markdown('<div class="sub-header">🏆 Best Move</div>', 
                       unsafe_allow_html=True)
            
            move = st.session_state.best_move
            
            # Display move details
            display_move_details(move)
            
            # Display visualization
            st.markdown("**Visual Preview:**")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**Before Move:**")
                renderer = GridRenderer()
                before_img = renderer.render_grid_with_move(
                    st.session_state.grid,
                    move.piece_cells,
                    move.position
                )
                st.image(before_img, use_container_width=True)
            
            with col2:
                st.markdown("**After Move (with line clears):**")
                after_img = renderer.render_grid(move.resulting_grid)
                st.image(after_img, use_container_width=True)
            
            # Show top moves
            if st.checkbox("Show Top 5 Moves"):
                st.markdown('<div class="sub-header">Top 5 Moves</div>', 
                           unsafe_allow_html=True)
                
                solver = BlockBlastSolver(
                    st.session_state.grid,
                    st.session_state.pieces
                )
                top_moves = solver.get_top_moves(5)
                
                for i, move in enumerate(top_moves):
                    with st.expander(f"Move {i + 1}: Score {move.score:.2f}"):
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.write(f"**Piece:** #{move.piece_index + 1}")
                            st.write(f"**Position:** {move.position}")
                            st.write(f"**Lines Cleared:** {move.lines_cleared}")
                        
                        with col2:
                            renderer = GridRenderer(cell_size=25)
                            preview_img = renderer.render_grid_with_move(
                                st.session_state.grid,
                                move.piece_cells,
                                move.position
                            )
                            st.image(preview_img, width=200)
    
    # Footer
    st.divider()
    st.markdown("""
    <div style="text-align: center; color: #666; padding: 1rem;">
        <p>Built with Streamlit, GPT-4o Vision API, and Python</p>
        <p>Upload a screenshot or manually enter your game state to get optimal move suggestions</p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
