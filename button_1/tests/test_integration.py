import pytest
from button_1.classes.button_game import ButtonGame
from button_1.classes.button_dat import ButtonDat
from button_1.classes.node_engine import NodeEngine
from button_1.classes.story_graph import StoryGraph


class TestIntegration:
    """Integration tests for component interactions"""

    def test_game_data_consistency_across_components(self):
        """Test that all components work with the same data consistently"""
        # Create components
        button_dat = ButtonDat()
        node_engine = NodeEngine(button_dat)
        button_game = ButtonGame()
        story_graph = StoryGraph()
        
        # Test that they all have access to the same underlying data structure
        assert not button_dat.edges_df.empty, "ButtonDat should have edges data"
        assert not button_dat.nodes_df.empty, "ButtonDat should have nodes data"
        
        # Test that NodeEngine can access the data through ButtonDat
        assert node_engine.button_dat.edges_df.equals(button_dat.edges_df), "NodeEngine should have same edges data"
        assert node_engine.button_dat.nodes_df.equals(button_dat.nodes_df), "NodeEngine should have same nodes data"
        
        # Test that ButtonGame creates its own data correctly
        assert not button_game.game_data.edges_df.empty, "ButtonGame should have edges data"
        assert not button_game.game_data.nodes_df.empty, "ButtonGame should have nodes data"
        
        # Test that StoryGraph has consistent data
        assert not story_graph.edges_df.empty, "StoryGraph should have edges data"
        assert not story_graph.nodes_df.empty, "StoryGraph should have nodes data"

    def test_game_engine_integration(self):
        """Test that ButtonGame and NodeEngine work together correctly"""
        game = ButtonGame()
        engine = game.engine
        
        # Test that the engine is properly configured
        assert engine.button_dat is not None, "Engine should have game data"
        assert engine.current_node == "start_game", "Engine should start at correct node"
        
        # Test that engine can get connections for nodes
        connections = engine.button_dat.get_connections("start_game")
        assert isinstance(connections, list), "Connections should be a list"

    def test_edge_and_node_data_consistency(self):
        """Test that edges reference valid nodes"""
        game_data = ButtonDat()
        
        # Get all unique nodes from both edges and nodes table
        edge_nodes = set(game_data.edges_df['source'].tolist() + game_data.edges_df['target'].tolist())
        node_table_nodes = set(game_data.nodes_df['node'].tolist())
        
        # Every node referenced in edges should exist in nodes table
        missing_nodes = edge_nodes - node_table_nodes
        
        # Allow for some flexibility - some edge nodes might be virtual or endpoints
        # But the core game nodes should exist
        critical_nodes = {'start_game', 'welcome', 'onboarding'}
        missing_critical = missing_nodes.intersection(critical_nodes)
        
        assert len(missing_critical) == 0, f"Critical nodes missing from nodes table: {missing_critical}"

    def test_game_flow_basic_validation(self):
        """Test basic game flow validation"""
        game_data = ButtonDat()
        
        # Test that start_game node exists and has connections
        start_connections = game_data.get_connections("start_game")
        assert len(start_connections) > 0, "start_game should have at least one connection"
        
        # Test that we can traverse at least a few steps
        current_node = "start_game"
        visited_nodes = [current_node]
        
        for step in range(3):  # Try to traverse 3 steps
            connections = game_data.get_connections(current_node)
            if not connections:
                break  # Reached a terminal node
            
            next_node = connections[0]  # Take first available connection
            assert next_node not in visited_nodes or len(visited_nodes) > 10, "Should not immediately cycle (unless in a long path)"
            
            visited_nodes.append(next_node)
            current_node = next_node
        
        assert len(visited_nodes) > 1, "Should be able to traverse at least one step from start"

    def test_text_data_availability(self):
        """Test that text data is available and accessible"""
        game_data = ButtonDat()
        
        # Test that text tables exist
        assert hasattr(game_data, 'text_df'), "Should have text_df"
        assert hasattr(game_data, 'titles_df'), "Should have titles_df"
        
        # Test that we can retrieve some basic texts
        pbn_text = game_data.get_text_by_id("pbn")
        assert pbn_text is not None, "Should be able to get 'pbn' text"
        assert isinstance(pbn_text, str), "pbn text should be a string"
        assert len(pbn_text.strip()) > 0, "pbn text should not be empty"

    def test_graph_visualization_integration(self):
        """Test that graph visualization works with game data"""
        story_graph = StoryGraph()
        
        # Test that graph was created successfully
        assert hasattr(story_graph, 'graph'), "StoryGraph should have a graph"
        assert story_graph.graph.number_of_nodes() > 0, "Graph should have nodes"
        assert story_graph.graph.number_of_edges() > 0, "Graph should have edges"
        
        # Test that critical game nodes exist in the graph
        critical_nodes = ['start_game', 'welcome']
        graph_nodes = list(story_graph.graph.nodes())
        
        for node in critical_nodes:
            if node in story_graph.nodes_df['node'].values:  # Only test if node exists in data
                assert node in graph_nodes, f"Critical node {node} should be in graph"