#!/bin/bash

# Block Blast Solver - Quick Start Script

echo "🧩 Block Blast Solver - Starting Application..."
echo ""

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 is not installed"
    exit 1
fi

# Check if streamlit is installed
if ! python3 -c "import streamlit" 2>/dev/null; then
    echo "📦 Installing dependencies..."
    pip install -q --break-system-packages -r requirements.txt || {
        echo "❌ Failed to install dependencies"
        exit 1
    }
fi

# Check for .env file
if [ -f ".env" ]; then
    echo "✓ Found .env file"
    export $(cat .env | grep -v '^#' | xargs)
else
    echo "⚠️  No .env file found. You can enter API key in the app."
fi

# Run the application
echo ""
echo "🚀 Starting Streamlit app..."
echo "   The app will open in your browser at http://localhost:8501"
echo ""
streamlit run app.py
