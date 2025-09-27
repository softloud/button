import pytest
from button_1.classes.button_dat import ButtonDat


class TestButtonDat:
    """Test suite for ButtonDat class"""

    def test_button_dat_initialization(self):
        """Test that ButtonDat initializes correctly with both datasets"""
        game_data = ButtonDat()
        
        # Test that both DataFrames exist
        assert hasattr(game_data, 'edges_df'), "ButtonDat should have edges_df attribute"
        assert hasattr(game_data, 'nodes_df'), "ButtonDat should have nodes_df attribute"
        
        # Test DataFrames are not empty
        assert not game_data.edges_df.empty, "Edges DataFrame should not be empty"
        assert not game_data.nodes_df.empty, "Nodes DataFrame should not be empty"

    def test_property_access(self):
        """Test that properties work for backward compatibility"""
        game_data = ButtonDat()
        
        # Test property access
        edges = game_data.edges
        nodes = game_data.nodes
        
        assert edges is not None, "Edges property should return data"
        assert nodes is not None, "Nodes property should return data"
        
        # Test they're the same as the DataFrame attributes
        assert edges.equals(game_data.edges_df), "Edges property should match edges_df"
        assert nodes.equals(game_data.nodes_df), "Nodes property should match nodes_df"

    def test_required_columns_exist(self):
        """Test that required columns exist in the DataFrames"""
        game_data = ButtonDat()
        
        # Test edges DataFrame has required columns
        assert 'source' in game_data.edges_df.columns, "Edges should have 'source' column"
        assert 'target' in game_data.edges_df.columns, "Edges should have 'target' column"

    def test_get_connections(self):
        """Test getting connections from a node"""
        game_data = ButtonDat()
        
        # Get the first source node to test with
        if not game_data.edges_df.empty:
            test_node = game_data.edges_df.iloc[0]['source']
            connections = game_data.get_connections(test_node)
            
            assert isinstance(connections, list), "Connections should return a list"
            # Should have at least one connection since we used a source node
            assert len(connections) > 0, f"Node {test_node} should have connections"

    def test_get_all_nodes(self):
        """Test getting all unique nodes"""
        game_data = ButtonDat()
        
        all_nodes = game_data.get_all_nodes()
        
        assert isinstance(all_nodes, list), "get_all_nodes should return a list"
        assert len(all_nodes) > 0, "Should have at least some nodes"
        
        # All items should be strings
        for node in all_nodes:
            assert isinstance(node, str), f"Node {node} should be a string"

    def test_get_node_info(self):
        """Test getting information about a specific node"""
        game_data = ButtonDat()
        
        # Test with a node that might exist
        if not game_data.nodes_df.empty and 'node' in game_data.nodes_df.columns:
            test_node = game_data.nodes_df.iloc[0]['node']
            info = game_data.get_node_info(test_node)
            
            assert info is not None, f"Should get info for node {test_node}"
            assert isinstance(info, dict), "Node info should be a dictionary"
        
        # Test with non-existent node
        fake_info = game_data.get_node_info("nonexistent_node")
        assert fake_info is None, "Should return None for nonexistent node"

    def test_validate_data(self):
        """Test data validation"""
        game_data = ButtonDat()
        
        issues = game_data.validate_data()
        
        # Should either return None (no issues) or a list of issues
        assert issues is None or isinstance(issues, list), "Validation should return None or list"
        
        # If there are issues, they should be strings
        if issues:
            for issue in issues:
                assert isinstance(issue, str), "Each issue should be a string"

    def test_data_consistency(self):
        """Test that the two DataFrames have consistent data"""
        game_data = ButtonDat()
        
        # Get all nodes from edges
        edge_nodes = set(game_data.edges_df['source'].tolist() + 
                        game_data.edges_df['target'].tolist())
        
        # Should have some nodes
        assert len(edge_nodes) > 0, "Should have nodes from edges"
        
        # All nodes should be strings
        for node in edge_nodes:
            assert isinstance(node, str), f"Edge node {node} should be a string"