#!/bin/bash
# Quick start script for running the game with Docker

set -e

echo "🎮 Press A Button Now - Docker Setup"
echo "====================================="

# Check if .env file exists
if [[ ! -f .env ]]; then
    echo "❌ Error: .env file not found!"
    echo ""
    echo "Please create a .env file with your Google Sheets credentials:"
    echo "BUTTON_SHEET_ID=your_google_sheets_id"
    echo "BUTTON_SHEET_EDGES_GID=edges_tab_gid"
    echo "BUTTON_SHEET_NODES_GID=nodes_tab_gid"
    echo "BUTTON_SHEET_TEXT_GID=text_tab_gid"
    echo "BUTTON_SHEET_TITLES_GID=titles_tab_gid"
    echo ""
    exit 1
fi

echo "✅ Found .env file"

# Build the Docker image
echo "🔨 Building Docker image..."
docker build -t press-a-button-now .

echo "✅ Docker image built successfully!"
echo ""
echo "🚀 Starting the game..."
echo "   (Press Ctrl+C to exit)"
echo ""

# Run the container interactively
docker run --rm -it \
    --env-file .env \
    --name button-game-session \
    press-a-button-now

echo ""
echo "🎯 Game session ended. Thanks for playing!"