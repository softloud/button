"""
ButtonGame - Main Game Loop and State Management
===============================================

This module contains the core game orchestration logic, managing the overall
game flow, state transitions, and player journey tracking for the satirical
data science adventure game.

Classes:
    ButtonGame: Primary game controller managing state, transitions, and modes

Dependencies:
    - ButtonDat: Game data aggregation and validation
    - NodeEngine: Individual node execution and interaction handling
"""

from .button_dat import ButtonDat
from .node_engine import NodeEngine
import textwrap


class ButtonGame:
    """
    Main game controller managing state, flow, and player journey.
    
    The ButtonGame class orchestrates the entire game experience, from initial
    setup through completion. It manages the game loop, tracks player progress,
    and provides both production (clean) and developer (debug) modes.
    
    Key Responsibilities:
    - Initialize and coordinate game subsystems (data, engine)
    - Execute main game loop with state transitions
    - Track and log complete player journey
    - Provide development and debugging capabilities
    - Generate comprehensive game summaries
    
    Attributes:
        game_data (ButtonDat): Game content and validation manager
        engine (NodeEngine): Individual node execution engine
        game_path (list): Complete record of player's journey
        current_node (str): Current position in the game graph
        game_running (bool): Main loop control flag
        developer_mode (bool): Debug information display toggle
    """
    
    def __init__(self, developer_mode: bool = False):
        """
        Initialize game with data loading and engine setup.
        
        Creates a new game instance, loads all game data from external sources
        (Google Sheets), initializes the node execution engine, and sets up
        journey tracking and state management.
        
        Args:
            developer_mode (bool): Enable detailed debug output. Defaults to False
        """
        self.game_data = ButtonDat()
        self.engine = NodeEngine(self.game_data, developer_mode=developer_mode)
        self.game_path = []
        self.current_node = "start_game"
        self.game_running = True
        self.developer_mode = developer_mode
        
        # Initialize path tracking
        self.log_transition(None, self.current_node, "start")
    
    def log_transition(self, from_node, to_node, edge_selector="auto", outro_text=None, is_desired=None):
        """
        Record a transition in the player's journey.
        
        Maintains a comprehensive log of all state transitions including
        the narrative context and technical details for later summary
        generation and debugging purposes.
        
        Args:
            from_node (str or None): Source node identifier (None for game start)
            to_node (str): Target node identifier
            edge_selector (str): Type of transition logic used
            outro_text (str, optional): Narrative text shown during transition
            is_desired (bool, optional): Whether this was the intended outcome
        """
        self.game_path.append({
            'from': from_node,
            'to': to_node,
            'edge_selector': edge_selector,
            'outro_text': outro_text,
            'is_desired': is_desired
        })
    
    def get_edge_info(self, from_node, to_node):
        """
        Get comprehensive edge information for transition logging.
        
        Retrieves both the narrative outro text and the desired status
        for a specific node transition, handling edge feedback for 
        random selectors appropriately.
        
        Returns:
            tuple: (combined_outro_text, is_desired_boolean)
                combined_outro_text includes edge feedback for random transitions
        """
        # Get the combined outro text (includes edge feedback for random selectors)
        combined_outro = self.engine.get_combined_outro_text(from_node, to_node)
        is_desired = self.engine.get_edge_desired_status(from_node, to_node)
        
        return combined_outro, is_desired
    
    def play_full_game(self):
        """
        Execute the complete game experience from start to finish.
        
        Runs the main game loop, managing state transitions and user
        interactions until reaching a terminal state. Automatically
        displays the journey summary upon completion.
        """
        if self.developer_mode:
            print("🔧 Development mode: Full game experience")
        
        while self.game_running and self.current_node:
            # Run the current node
            next_node = self.engine.run_single_node(self.current_node)
            
            if next_node:
                # Get edge information for logging
                edge_selector = self.engine.get_edge_selector(self.current_node)
                outro_text, is_desired = self.get_edge_info(self.current_node, next_node)
                
                # Log the transition with all details
                self.log_transition(self.current_node, next_node, edge_selector, outro_text, is_desired)
                
                # Move to next node
                self.current_node = next_node
            else:
                # End of game
                self.game_running = False
        
        # Show final summary
        self.show_game_summary()
    
    def play_single_node(self, node_name: str):
        """
        Execute a single node for development and testing purposes.
        
        Runs an individual node in isolation with developer mode enabled,
        useful for testing specific game states and narrative content.
        
        Args:
            node_name (str): Node identifier to execute
            
        Returns:
            str or None: Next node identifier or None if terminal
        """
        if not self.developer_mode:
            print(f"🔧 Development mode: Single node ({node_name})")
        
        # Create a temporary developer-mode engine for single node testing
        dev_engine = NodeEngine(self.game_data, developer_mode=True)
        return dev_engine.run_single_node(node_name)
    
    def show_game_summary(self):
        """Show the player's journey through the game with full narrative"""
        print(f"\n{'='*60}")
        print("🗺️  Your Journey Through the Data Science World")
        print("="*60)
        
        for i, step in enumerate(self.game_path):
            if i == 0:
                continue  # Skip initial "start" entry
                
            # Show the transition
            from_node = step['from'].replace('_', ' ').title()
            to_node = step['to'].replace('_', ' ').title()
            print(f"\n{i}. {from_node} → {to_node}")
            
            # Show outro text if available (now includes edge feedback)
            if step.get('outro_text'):
                # Wrap the outro text for consistent formatting
                wrapped_outro = textwrap.fill(step['outro_text'], width=80, 
                                            initial_indent="   � ", subsequent_indent="   ")
                print(wrapped_outro)
                
            # Show technical details only in developer mode
            if self.developer_mode:
                edge_selector = step.get('edge_selector', 'unknown')
                desired_status = "✅" if step.get('is_desired') else "⚠️" if step.get('is_desired') is False else "❓"
                print(f"   🔧 [{edge_selector}] {desired_status}")
        
        print(f"\nTotal nodes visited: {len(self.game_path)}")
        print("Thanks for playing!")
    
    def get_available_nodes(self):
        """Get list of available nodes for development/testing"""
        return self.game_data.get_all_nodes()