#!/usr/bin/env python3
"""
Module Entry Point for Press A Button Now
==========================================

This file enables running the game as a Python module using:
    python -m button_1

When executed, it imports and calls the main() function from the package's
__init__.py file, which handles all game initialization, menu presentation,
and mode selection.

This follows Python's standard convention for making packages executable
as modules while keeping the main game logic centralized in the package's
main initialization file.

Usage:
    python -m button_1              # Run the full interactive game
    uv run python -m button_1       # Run with uv environment manager

Environment Requirements:
    - .env file with Google Sheets API credentials
    - Python packages: pandas, networkx, matplotlib, python-dotenv, requests
"""

from . import main

if __name__ == "__main__":
    main()