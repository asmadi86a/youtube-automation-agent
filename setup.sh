#!/bin/bash

# YouTube Automation Agent - Setup Script
# This script automates the installation and configuration of the YouTube automation agent

set -e

echo "========================================"
echo "YouTube Automation Agent - Setup"
echo "========================================"
echo ""

# Check Python installation
echo "[1/6] Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed. Please install Python 3.8+ first."
    exit 1
fi
echo "✓ Python $(python3 --version | awk '{print $2}') found"
echo ""

# Create virtual environment
echo "[2/6] Setting up virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "✓ Virtual environment created"
else
    echo "✓ Virtual environment already exists"
fi
source venv/bin/activate
echo ""

# Install dependencies
echo "[3/6] Installing dependencies..."
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
echo "✓ Dependencies installed"
echo ""

# Create required directories
echo "[4/6] Creating required directories..."
mkdir -p videos shorts logs
echo "✓ Directories created: videos/, shorts/, logs/"
echo ""

# Setup environment file
echo "[5/6] Setting up environment configuration..."
if [ ! -f ".env" ]; then
    cp .env.example .env
    echo "✓ Created .env file from template"
    echo "⚠ IMPORTANT: Edit .env file and fill in your YouTube API credentials"
else
    echo "✓ .env file already exists"
fi
echo ""

# Final instructions
echo "[6/6] Setup complete!"
echo "========================================"
echo "✓ Installation completed successfully!"
echo "========================================"
echo ""
echo "Next steps:"
echo "1. Activate virtual environment:"
echo "   source venv/bin/activate"
echo ""
echo "2. Edit .env file with your YouTube API credentials:"
echo "   - Get credentials from: https://console.developers.google.com"
echo "   - Fill in YOUTUBE_CLIENT_ID, YOUTUBE_CLIENT_SECRET, etc."
echo ""
echo "3. Run the agent:"
echo "   python youtube_agent.py"
echo ""
echo "4. Or use Docker:"
echo "   docker build -t youtube-agent ."
echo "   docker run youtube-agent"
echo ""
echo "For more information, see README.md"
echo ""
