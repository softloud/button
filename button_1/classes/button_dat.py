"""
ButtonDat - Game Data Aggregation and Validation
=================================================

This module provides comprehensive data management for the text-based adventure
game, aggregating content from multiple Google Sheets sources and providing
validation and query interfaces for game logic.

The ButtonDat class serves as the central data hub, loading and coordinating
edges, nodes, and text data while providing convenient methods for game
state queries and content retrieval.

Classes:
    ButtonDat: Main data aggregator and query interface

Data Sources:
    - edges: State transition definitions with outro text and desired flags
    - nodes: Node definitions with titles, content, and edge selectors  
    - text: Reusable text snippets and UI elements

Key Features:
    - Automatic Google Sheets data loading with rate limiting
    - Comprehensive data validation with detailed error reporting
    - Convenient query methods for game logic
    - Robust connection mapping for state transitions
"""

from .button_df import ButtonDf
import time


class ButtonDat:
    """
    Comprehensive data manager for the text-based adventure game.
    
    ButtonDat serves as the central data hub, loading content from multiple
    Google Sheets sources and providing validation and query interfaces
    for all game logic. It coordinates edges, nodes, and text data while
    implementing rate limiting to avoid API restrictions.
    
    The class provides high-level methods for common game queries like
    finding node connections, validating data integrity, and retrieving
    text content, abstracting away the complexity of working with
    multiple data sources.
    
    Attributes:
        edges_df (pd.DataFrame): State transition definitions
        nodes_df (pd.DataFrame): Node content and configuration
        text_df (pd.DataFrame): Reusable text snippets
        
    Data Structure:
        edges: source, target, outro_text, desired
        nodes: node, edge_selector, title_text, intro_text, event_text, pbn
        text: id_text, text_type, text_context, text
    """
    
    def __init__(self):
        """
        Initialize with comprehensive data loading from Google Sheets.
        
        Loads three primary datasets (edges, nodes, text) with appropriate
        rate limiting between requests to avoid Google Sheets API restrictions.
        Each dataset is loaded via ButtonDf scrapers with automatic retry logic.
        
        Raises:
            ConnectionError: If Google Sheets data cannot be accessed
            ValueError: If required data columns are missing or malformed
            
        Note:
            Requires .env file with appropriate Google Sheets API credentials
            and sheet configuration for the 'edges', 'nodes', and 'text' tabs.
        """
        # Add small delays to avoid Google Sheets rate limiting
        
        # Load edges data - state transitions and outcomes
        self._edges_scraper = ButtonDf('edges')
        self.edges_df = self._edges_scraper.df
        time.sleep(0.5)  # Rate limiting delay
        
        # Load nodes data - individual node definitions
        self._nodes_scraper = ButtonDf('nodes')
        self.nodes_df = self._nodes_scraper.df
        time.sleep(0.5)  # Rate limiting delay
        
        # Load text data - reusable content snippets
        self._text_scraper = ButtonDf('text')
        self.text_df = self._text_scraper.df

    @property
    def edges(self):
        """Get edges DataFrame (for backward compatibility)"""
        return self.edges_df
    
    @property 
    def nodes(self):
        """Get nodes DataFrame (for backward compatibility)"""
        return self.nodes_df
    
    @property
    def text(self):
        """Get text DataFrame"""
        return self.text_df
        
    def get_node_info(self, node_name):
        """Get information about a specific node"""
        if 'node' in self.nodes_df.columns:
            node_data = self.nodes_df[self.nodes_df['node'] == node_name]
            if not node_data.empty:
                return node_data.iloc[0].to_dict()
        return None
        
    def get_connections(self, node_name):
        """Get all connections (edges) from a specific node"""
        connections = self.edges_df[self.edges_df['source'] == node_name]
        return connections['target'].tolist()
        
    def get_all_nodes(self):
        """Get list of all unique nodes in the game"""
        # Get unique nodes from both source and target columns
        edge_nodes = set(self.edges_df['source'].tolist() + self.edges_df['target'].tolist())
        
        # If nodes DataFrame has a 'node' column, include those too
        if 'node' in self.nodes_df.columns:
            node_list_nodes = set(self.nodes_df['node'].tolist())
            return list(edge_nodes.union(node_list_nodes))
        
        return list(edge_nodes)
        
    def get_text_by_id(self, text_id):
        """Get text content by id_text"""
        if 'id_text' in self.text_df.columns:
            text_data = self.text_df[self.text_df['id_text'] == text_id]
            if not text_data.empty:
                return text_data.iloc[0]['text']
        return None
    
    def get_texts_by_type(self, text_type):
        """Get all texts of a specific type"""
        if 'text_type' in self.text_df.columns:
            return self.text_df[self.text_df['text_type'] == text_type]
        return None
    
    def get_node_texts(self, node_name):
        """Get all texts associated with a specific node"""
        # Assuming text IDs follow pattern: node_name_text_type
        node_texts = {}
        if 'id_text' in self.text_df.columns:
            for _, row in self.text_df.iterrows():
                if row['id_text'].startswith(f"{node_name}_"):
                    text_type = row.get('text_type', 'unknown')
                    node_texts[text_type] = row['text']
        return node_texts
        
    def validate_data(self):
        """Validate that the game data is consistent"""
        issues = []
        
        # Check if edges DataFrame is not empty
        if self.edges_df.empty:
            issues.append("Edges DataFrame is empty")
            
        # Check if nodes DataFrame is not empty  
        if self.nodes_df.empty:
            issues.append("Nodes DataFrame is empty")
            
        # Check if text DataFrame is not empty
        if self.text_df.empty:
            issues.append("Text DataFrame is empty")
            
        # Check required columns exist
        if 'source' not in self.edges_df.columns:
            issues.append("Edges DataFrame missing 'source' column")
        if 'target' not in self.edges_df.columns:
            issues.append("Edges DataFrame missing 'target' column")
        if 'id_text' not in self.text_df.columns:
            issues.append("Text DataFrame missing 'id_text' column")
        if 'text_type' not in self.text_df.columns:
            issues.append("Text DataFrame missing 'text_type' column")
        if 'text' not in self.text_df.columns:
            issues.append("Text DataFrame missing 'text' column")
            
        return issues if issues else None
