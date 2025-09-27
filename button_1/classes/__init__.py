"""
Game Classes Package - Core System Components
=============================================

This package contains all the core classes that implement the text-based
adventure game system. Each class has specific responsibilities in the
overall architecture, from data management to user interaction.

Architecture Overview:
    Data Layer:
        - ButtonDf: Google Sheets connector with retry logic
        - ButtonDat: Multi-source data aggregator and validator
    
    Visualization Layer:
        - StoryGraph: NetworkX-based narrative flow visualization
    
    Game Logic Layer:
        - NodeEngine: Individual node execution and interaction
        - ButtonGame: Main game loop and state management

Classes:
    ButtonDf: Google Sheets data scraper with exponential backoff
    ButtonDat: Comprehensive game data manager and validator
    StoryGraph: Network visualization of narrative structure  
    NodeEngine: Node execution engine with edge selector logic
    ButtonGame: Main game controller and journey tracker

Key Design Principles:
    - Separation of concerns between data, logic, and presentation
    - Robust error handling with clear user-facing messages
    - Comprehensive data validation with detailed reporting
    - Support for both production and developer modes
    - Extensible architecture for future feature additions

Data Flow:
    Google Sheets → ButtonDf → ButtonDat → NodeEngine → ButtonGame
                                      ↓
                                 StoryGraph (visualization)
"""

# Import all classes for easy access
from .button_df import ButtonDf
from .button_dat import ButtonDat
from .story_graph import StoryGraph
from .node_engine import NodeEngine
from .button_game import ButtonGame

__all__ = [
    'ButtonDf',
    'ButtonDat', 
    'StoryGraph',
    'NodeEngine',
    'ButtonGame'
]