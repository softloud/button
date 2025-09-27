#!/usr/bin/env python3
"""
Press A Button Now - A Satirical Data Science Adventure Game
============================================================

A text-based adventure game that satirically explores the lived experience 
of working in data science. Players navigate through the typical data science 
workflow while experiencing the frustrations, loops, and unexpected turns 
that characterize real data work.

Game Features:
- Dynamic narrative sourced from Google Sheets
- Multiple game modes (production clean vs developer debug)
- Random decision points that mirror real data science uncertainty
- Comprehensive visualization of the narrative graph
- State tracking and journey summaries
- Consistent text wrapping and formatting for optimal console display

Architecture Overview:
- ButtonDf: Google Sheets data connector with retry logic
- ButtonDat: Game data aggregator and validator
- StoryGraph: NetworkX-based narrative visualization
- NodeEngine: Interactive game mechanics engine with text wrapping
- ButtonGame: Main game loop and state management

Usage:
    python -m button_1

Author: Your Name
License: MIT
Version: 1.0.0
"""

from .classes.button_game import ButtonGame

from dotenv import load_dotenv
load_dotenv()  # Ensure environment variables are loaded


def main():
    """
    Main entry point for the button game.
    
    Provides a menu-driven interface allowing users to choose between:
    1. Clean production game experience
    2. Developer mode with debug information  
    3. Single node development/testing mode
    4. View all available game nodes
    
    Handles initialization errors gracefully and provides helpful
    error messages for common configuration issues.
    
    Raises:
        Exception: If game data loading fails or .env configuration is missing
    """
    try:
        print("🎮 Welcome to 'Press A Button Now' - A Data Science Adventure!")
        print("Loading game...")
        
        # Initialize the game
        game = ButtonGame()
        
        print("✅ Game loaded successfully!")
        print("\nChoose your mode:")
        print("1. Play full game (clean production experience)")
        print("2. Play full game (developer mode with debug info)")
        print("3. Single node development mode")
        print("4. Show available nodes")
        
        choice = input("\nEnter your choice (1-4): ").strip()
        
        if choice == "1":
            # Production game mode - clean experience
            production_game = ButtonGame(developer_mode=False)
            production_game.play_full_game()
        elif choice == "2":
            # Developer game mode - with debug info
            dev_game = ButtonGame(developer_mode=True)
            dev_game.play_full_game()
        elif choice == "3":
            # Single node development
            game = ButtonGame()
            nodes = game.get_available_nodes()
            print(f"\nAvailable nodes: {', '.join(nodes[:5])}...")
            
            node_name = input("Enter node name (or press Enter for start_game): ").strip()
            if not node_name:
                node_name = "start_game"
                
            result = game.play_single_node(node_name)
            print(f"\nResult: Next node would be '{result}'")
        elif choice == "4":
            # Show all nodes
            game = ButtonGame()
            nodes = game.get_available_nodes()
            print(f"\nAll available nodes ({len(nodes)}):")
            for i, node in enumerate(nodes, 1):
                print(f"{i:2d}. {node}")
        else:
            print("Invalid choice. Starting production game...")
            production_game = ButtonGame(developer_mode=False)
            production_game.play_full_game()
            
    except Exception as e:
        print(f"❌ Error running game: {e}")
        print("Make sure your .env file has the required Google Sheets credentials.")


if __name__ == "__main__":
    main()