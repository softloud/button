import pytest
import networkx as nx
import matplotlib.pyplot as plt
import os
from button_1.classes.story_graph import StoryGraph


class TestStoryGraph:
    """Test suite for StoryGraph class"""

    def test_story_graph_initialization(self):
        """Test that StoryGraph initializes correctly"""
        story = StoryGraph()
        
        # Test inheritance - should have edges_df and nodes_df from ButtonDat
        assert hasattr(story, 'edges_df'), "StoryGraph should inherit edges_df from ButtonDat"
        assert hasattr(story, 'nodes_df'), "StoryGraph should inherit nodes_df from ButtonDat"
        assert not story.edges_df.empty, "Edges DataFrame should not be empty after initialization"
        assert not story.nodes_df.empty, "Nodes DataFrame should not be empty after initialization"
        
        # Test graph creation
        assert hasattr(story, 'graph'), "StoryGraph should have a graph attribute"
        assert isinstance(story.graph, nx.DiGraph), "Graph should be a NetworkX DiGraph"

    def test_graph_structure(self):
        """Test that the graph structure is correct"""
        story = StoryGraph()
        
        # Test that graph has nodes and edges
        assert len(story.graph.nodes()) > 0, "Graph should have nodes"
        assert len(story.graph.edges()) > 0, "Graph should have edges"
        
        # Test that it's a directed graph
        assert story.graph.is_directed(), "Graph should be directed"

    def test_graph_data_consistency(self):
        """Test that graph data matches DataFrame data"""
        story = StoryGraph()
        
        # Number of edges in graph should match DataFrame rows
        assert len(story.graph.edges()) == len(story.edges_df), "Graph edges should match edges DataFrame rows"
        
        # Check that source/target columns exist in DataFrame
        assert 'source' in story.edges_df.columns, "Edges DataFrame should have 'source' column"
        assert 'target' in story.edges_df.columns, "Edges DataFrame should have 'target' column"

    def test_plot_graph_method(self):
        """Test that plot_graph method works without errors"""
        story = StoryGraph()
        
        # This should not raise any exceptions
        try:
            story.plot_graph()
            # Close the plot to avoid display issues in testing
            plt.close('all')
        except Exception as e:
            pytest.fail(f"plot_graph() raised an exception: {e}")

    def test_save_graph_method(self):
        """Test that save_graph method creates a file"""
        story = StoryGraph()
        
        # First plot, then save
        story.plot_graph()
        story.save_graph()
        
        # Check that the file was created
        assert os.path.exists("button_1/vis/graph.png"), "Graph PNG file should be created"
        
        # Clean up
        plt.close('all')

    def test_create_and_save_graph_method(self):
        """Test the convenience method"""
        story = StoryGraph()
        
        # This should not raise any exceptions and should create the file
        try:
            story.create_and_save_graph()
            assert os.path.exists("button_1/vis/graph.png"), "Graph PNG file should be created"
        except Exception as e:
            pytest.fail(f"create_and_save_graph() raised an exception: {e}")
        finally:
            # Clean up
            plt.close('all')

    def test_graph_nodes_are_strings(self):
        """Test that graph nodes are strings as expected"""
        story = StoryGraph()
        
        # All nodes should be strings
        for node in story.graph.nodes():
            assert isinstance(node, str), f"Node {node} should be a string"

    def test_graph_has_expected_structure(self):
        """Test that graph has some expected properties"""
        story = StoryGraph()
        
        # Graph should be connected (or at least have a path from start to some end)
        assert len(story.graph.nodes()) >= 2, "Graph should have at least 2 nodes"
        
        # Should have some node with no incoming edges (start node)
        start_nodes = [n for n in story.graph.nodes() if story.graph.in_degree(n) == 0]
        assert len(start_nodes) > 0, "Graph should have at least one start node (no incoming edges)"

    @pytest.fixture(autouse=True)
    def cleanup_files(self):
        """Clean up test files after each test"""
        yield
        # Clean up any created PNG files
        if os.path.exists("button_1/vis/graph.png"):
            try:
                os.remove("button_1/vis/graph.png")
            except OSError:
                pass  # File might not exist or be in use
        plt.close('all')  # Close all matplotlib figures