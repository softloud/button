"""
NodeEngine - Individual Node Execution and Interaction Handler
==============================================================

This module manages the execution of individual game nodes, handling user
interaction, content display, and state transitions. It provides the core
gameplay mechanics for the text-based adventure experience.

The engine supports different edge selector types (auto, random, choice, etc.)
and manages the display of narrative content with contextual feedback for
random decision points.

Classes:
    NodeEngine: Core node execution and interaction management

Key Features:
    - Dynamic content display from game data
    - User input handling with visual prompts
    - Edge selector logic (auto, random, choice, start, end)
    - Contextual feedback for random transitions
    - Developer mode debugging information
"""

from .button_dat import ButtonDat
import random
import pandas as pd
import sys
import termios
import tty
import textwrap


class NodeEngine:
    """
    Core engine for executing individual game nodes and managing interactions.
    
    The NodeEngine handles all aspects of individual node execution, from
    displaying narrative content to processing user input and determining
    the next state transition. It supports multiple edge selector types
    and provides rich debugging information in developer mode.
    
    Key Responsibilities:
    - Display node content (title, intro, event text)
    - Handle user input and interaction prompts
    - Execute edge selector logic for state transitions
    - Provide contextual feedback for random outcomes
    - Generate detailed debug information
    
    Attributes:
        button_dat (ButtonDat): Game data source and validator
        current_node (str): Currently active node identifier
        game_running (bool): Engine state control flag
        developer_mode (bool): Debug information display toggle
        
    Edge Selector Types:
        auto: Automatic progression to first available connection
        random: Random selection from available connections  
        choice: User choice between multiple options (future feature)
        start: Initial game state selector
        end: Terminal state with no progression
    """
    
    def __init__(self, button_dat: ButtonDat, starting_node: str = "start_game", developer_mode: bool = False):
        """
        Initialize the node engine with game data and configuration.
        
        Sets up the engine with access to game data and configures
        the starting state and display mode preferences.
        
        Args:
            button_dat (ButtonDat): Initialized game data manager
            starting_node (str): Initial node identifier. Defaults to "start_game"
            developer_mode (bool): Enable detailed debug output. Defaults to False
        """
        self.button_dat = button_dat
        self.current_node = starting_node
        self.game_running = True
        self.developer_mode = developer_mode
    
    def wrap_text(self, text, width=80):
        """
        Wrap text to fit console width with proper line breaks.
        
        Args:
            text (str): Text to wrap
            width (int): Maximum line width. Defaults to 80 characters
            
        Returns:
            str: Text with appropriate line breaks
        """
        if not text:
            return text
        
        # Use textwrap to break long lines
        wrapped_lines = textwrap.wrap(text, width=width)
        return '\n'.join(wrapped_lines)
    
    def get_arrow_key_input(self):
        """
        Get arrow key input without requiring Enter.
        
        Captures direct arrow key presses using terminal raw mode.
        Handles escape sequences for arrow keys and provides fallback
        for Enter key and Ctrl+C interrupt.
        
        Returns:
            str: Key identifier ('RIGHT', 'LEFT', 'UP', 'DOWN', 'ENTER', or None)
            
        Raises:
            KeyboardInterrupt: If user presses Ctrl+C
        """
        try:
            # Save terminal settings
            old_settings = termios.tcgetattr(sys.stdin)
            tty.setraw(sys.stdin.fileno())
            
            # Read key input
            key = sys.stdin.read(1)
            
            # Handle arrow keys (they come as escape sequences)
            if key == '\x1b':  # ESC sequence
                key += sys.stdin.read(2)
                if key == '\x1b[C':  # Right arrow
                    return 'RIGHT'
                elif key == '\x1b[D':  # Left arrow  
                    return 'LEFT'
                elif key == '\x1b[A':  # Up arrow
                    return 'UP'
                elif key == '\x1b[B':  # Down arrow
                    return 'DOWN'
            elif key == '\r' or key == '\n':  # Enter key (fallback)
                return 'ENTER'
            elif key == '\x03':  # Ctrl+C
                raise KeyboardInterrupt
            
            return None
        finally:
            # Restore terminal settings
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)
        
    def display_title(self, node_name: str):
        """Display title of node with separation"""
        title = self.get_node_column_text(node_name, 'title_text')
        if title:
            print("\n" + "=" * 50)
            print(f"  {title.upper()}")
            print("=" * 50)
        else:
            print(f"\n=== {node_name.replace('_', ' ').title()} ===")
    
    def display_intro(self, node_name: str):
        """
        Display intro text for the node with proper text wrapping.
        
        Args:
            node_name (str): Node identifier to get intro text for
        """
        intro = self.get_node_column_text(node_name, 'intro_text')
        if intro:
            wrapped_intro = self.wrap_text(intro)
            print(f"\n{wrapped_intro}")
            print()  # Add extra line for spacing
    
    def display_event(self, node_name: str):
        """
        Display event text for the node with proper text wrapping.
        
        Args:
            node_name (str): Node identifier to get event text for
        """
        event = self.get_node_column_text(node_name, 'event_text')
        if event:
            wrapped_event = self.wrap_text(event)
            print(f"\n{wrapped_event}")

    def get_user_input(self, node_name: str):
        """
        Get user input with visual prompt for available choices.
        
        Uses arrow key input for intuitive navigation. Currently supports
        single choice scenarios with right arrow progression.
        
        Args:
            node_name (str): Current node identifier
            
        Returns:
            str: User input indicator ('RIGHT' for progression)
            
        Raises:
            ValueError: If 'pbn' text is missing from game data
        """
        pbn_text = self.button_dat.get_text_by_id("pbn")
        if not pbn_text:
            raise ValueError("Missing 'pbn' text in game data - required for user input prompts")
        
        pbn_node = self.get_node_column_text(node_name, 'pbn')
        
        # Get available connections to determine valid choices
        connections = self.button_dat.get_connections(node_name)
        
        if len(connections) == 1:
            # Single choice - show right arrow prompt
            prompt = f"{pbn_text} {pbn_node}: → (press right arrow)"
            wrapped_prompt = self.wrap_text(prompt)
            print(wrapped_prompt, end='', flush=True)

            while True:
                key = self.get_arrow_key_input()
                if key == 'RIGHT':
                    print(" ✓")  # Show confirmation
                    return 'RIGHT'
                elif key in ['ENTER']:  # Allow Enter as fallback
                    print(" ✓")
                    return 'RIGHT'
                # Ignore other keys and keep waiting
        else:
            # Multiple choices - will implement later when needed
            prompt = f"{pbn_text} {pbn_node}: → (press right arrow)"
            wrapped_prompt = self.wrap_text(prompt)
            print(wrapped_prompt, end='', flush=True)
            
            while True:
                key = self.get_arrow_key_input()
                if key == 'RIGHT':
                    print(" ✓")
                    return 'RIGHT'
                elif key in ['ENTER']:
                    print(" ✓")
                    return 'RIGHT'
    
    def get_edge_outro_text(self, from_node: str, to_node: str):
        """Get outro text for a specific edge from the edges DataFrame"""
        if hasattr(self.button_dat, 'edges_df') and 'outro_text' in self.button_dat.edges_df.columns:
            # Look for the specific edge
            edge_data = self.button_dat.edges_df[
                (self.button_dat.edges_df['source'] == from_node) & 
                (self.button_dat.edges_df['target'] == to_node)
            ]
            if not edge_data.empty:
                outro = edge_data.iloc[0]['outro_text']
                # Return text if it's not NaN/empty
                return outro if pd.notna(outro) and str(outro).strip() else None
        return None

    def get_combined_outro_text(self, from_node: str, to_node: str):
        """Get the combined edge feedback + outro text (same as what's displayed) - only for random selectors"""
        # Get outro text from the edge data
        outro = self.get_edge_outro_text(from_node, to_node)
        
        # Only add edge feedback for random edge selectors
        edge_selector = self.get_edge_selector(from_node)
        edge_feedback = ""
        
        if edge_selector == 'random':
            # Get desired status for this edge
            is_desired = self.get_edge_desired_status(from_node, to_node)
            
            # Get appropriate edge feedback text
            if is_desired is not None:
                if is_desired:
                    edge_feedback = self.button_dat.get_text_by_id("edge_good")
                    if not edge_feedback:
                        raise ValueError("Missing 'edge_good' text in game data - required for positive random edge feedback")
                else:
                    edge_feedback = self.button_dat.get_text_by_id("edge_bad")
                    if not edge_feedback:
                        raise ValueError("Missing 'edge_bad' text in game data - required for negative random edge feedback")
        
        # Simple concatenation: edge_feedback + outro_text (only if random)
        combined_parts = []
        if edge_feedback:
            combined_parts.append(edge_feedback)
        if outro:
            combined_parts.append(outro)
            
        return " ".join(combined_parts) if combined_parts else None

    def get_edge_desired_status(self, from_node: str, to_node: str):
        """Get whether this edge transition is desired (TRUE/FALSE)"""
        if hasattr(self.button_dat, 'edges_df') and 'desired' in self.button_dat.edges_df.columns:
            edge_data = self.button_dat.edges_df[
                (self.button_dat.edges_df['source'] == from_node) & 
                (self.button_dat.edges_df['target'] == to_node)
            ]
            if not edge_data.empty:
                desired_val = edge_data.iloc[0]['desired']
                # Convert to boolean if it's a string
                if isinstance(desired_val, str):
                    return desired_val.upper() == 'TRUE'
                else:
                    return bool(desired_val)
        return None

    def display_outro(self, node_name: str, next_node: str = None):
        """
        Display outro text for the transition between nodes with proper text wrapping.
        
        For random edge selectors, adds appropriate feedback (edge_good/edge_bad)
        before the outro text. All text is wrapped to 80 characters for readable
        console output.
        
        Args:
            node_name (str): Current node identifier
            next_node (str, optional): Target node identifier
        """
        if next_node:
            # Get outro text from the edge data
            outro = self.get_edge_outro_text(node_name, next_node)
            
            # Only add edge feedback for random edge selectors
            edge_selector = self.get_edge_selector(node_name)
            edge_feedback = ""
            
            if edge_selector == 'random':
                # Get desired status for this edge
                is_desired = self.get_edge_desired_status(node_name, next_node)
                
                # Get appropriate edge feedback text
                if is_desired is not None:
                    if is_desired:
                        edge_feedback = self.button_dat.get_text_by_id("edge_good")
                        if not edge_feedback:
                            raise ValueError("Missing 'edge_good' text in game data - required for positive random edge feedback")
                    else:
                        edge_feedback = self.button_dat.get_text_by_id("edge_bad")
                        if not edge_feedback:
                            raise ValueError("Missing 'edge_bad' text in game data - required for negative random edge feedback")
            
            # Simple concatenation: edge_feedback + outro_text (only if random)
            combined_parts = []
            if edge_feedback:
                combined_parts.append(edge_feedback)
            if outro:
                combined_parts.append(outro)
                
            if combined_parts:
                combined_text = " ".join(combined_parts)
                wrapped_text = self.wrap_text(combined_text)
                print(f"\n{wrapped_text}")
                print()  # Add extra line for spacing

    def get_node_column_text(self, node_name: str, column_name: str):
        """Get text from a specific column in the nodes DataFrame"""
        if 'node' in self.button_dat.nodes_df.columns and column_name in self.button_dat.nodes_df.columns:
            node_data = self.button_dat.nodes_df[self.button_dat.nodes_df['node'] == node_name]
            if not node_data.empty:
                text = node_data.iloc[0][column_name]
                # Return text if it's not NaN/empty
                return text if pd.notna(text) and text.strip() else None
        return None
    
    def get_edge_selector(self, node_name: str):
        """Get the edge selector type for a node"""
        if 'node' in self.button_dat.nodes_df.columns and 'edge_selector' in self.button_dat.nodes_df.columns:
            node_data = self.button_dat.nodes_df[self.button_dat.nodes_df['node'] == node_name]
            if not node_data.empty:
                return node_data.iloc[0]['edge_selector']
        return 'auto'  # Default to auto progression
    
    def determine_next_node(self, current_node: str):
        """Determine next node based on edge_selector and game logic"""
        edge_selector = self.get_edge_selector(current_node)
        connections = self.button_dat.get_connections(current_node)
        
        if not connections:
            return None  # End of game
            
        if edge_selector == 'auto':
            # Automatic progression - take first available connection
            return connections[0]
        elif edge_selector == 'random':
            # Random selection from available connections
            return random.choice(connections)
        elif edge_selector == 'end':
            # End node - no progression
            return None
        else:
            # For now, default to first connection (will expand for choice/input later)
            return connections[0] if connections else None
    
    def run_single_node(self, node_name: str = None):
        """Run a single node - for development and testing"""
        if node_name is None:
            node_name = self.current_node
            
        if self.developer_mode:
            print(f"\n🎮 Running single node: {node_name}")
        
        # Execute node sequence
        self.display_title(node_name)
        self.display_intro(node_name)
        self.display_event(node_name)
        
        # Get user interaction
        user_input = self.get_user_input(node_name)
        
        # Determine what happens next before displaying outro
        next_node = self.determine_next_node(node_name)
        
        # Display outro with context of where we're going
        self.display_outro(node_name, next_node)
        
        # Developer mode: Show development information
        if self.developer_mode:
            self.display_developer_info(node_name, next_node, user_input)
            
        return next_node
    
    def display_developer_info(self, node_name: str, next_node: str, user_input: str):
        """Display developer information separate from game content"""
        print(f"\n{'='*60}")
        print("🔧 DEVELOPER MODE - DEBUG INFO")
        print("="*60)
        
        print(f"📍 Current Node: {node_name}")
        print(f"🎯 Edge Selector: {self.get_edge_selector(node_name)}")
        
        connections = self.button_dat.get_connections(node_name)
        print(f"🔗 Available Connections: {connections}")
        
        if next_node:            
            print(f"➡️  Next Node: {next_node}")
            
            # Show whether this was a desired edge selection
            is_desired = self.get_edge_desired_status(node_name, next_node)
            if is_desired is not None:
                desired_symbol = "✅" if is_desired else "⚠️"
                print(f"🎯 Edge Desired: {is_desired} {desired_symbol}")
        else:
            print(f"🏁 Game End: No more connections")
            
        print(f"⌨️  User Input: '{user_input}'")
        print(f"✅ Node Execution Complete")
        print("="*60)