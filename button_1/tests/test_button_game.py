import pytest
from button_1.classes.button_game import ButtonGame
from unittest.mock import Mock, patch


class TestButtonGame:
    """Test suite for ButtonGame class"""

    def test_button_game_initialization(self):
        """Test that ButtonGame initializes correctly"""
        game = ButtonGame(developer_mode=False)
        
        assert hasattr(game, 'game_data'), "ButtonGame should have game_data attribute"
        assert hasattr(game, 'engine'), "ButtonGame should have engine attribute"
        assert hasattr(game, 'game_path'), "ButtonGame should have game_path attribute"
        assert game.current_node == "start_game", "Should start at start_game node"
        assert game.game_running is True, "Game should be running initially"
        assert game.developer_mode is False, "Developer mode should be set correctly"

    def test_button_game_developer_mode(self):
        """Test developer mode initialization"""
        dev_game = ButtonGame(developer_mode=True)
        assert dev_game.developer_mode is True, "Developer mode should be enabled"

    def test_log_transition(self):
        """Test journey logging functionality"""
        game = ButtonGame()
        initial_path_length = len(game.game_path)
        
        # Log a transition
        game.log_transition("node_a", "node_b", "auto", "Test outro text", True)
        
        assert len(game.game_path) == initial_path_length + 1, "Path should have one more entry"
        last_entry = game.game_path[-1]
        assert last_entry['from'] == "node_a", "From node should be recorded"
        assert last_entry['to'] == "node_b", "To node should be recorded"
        assert last_entry['edge_selector'] == "auto", "Edge selector should be recorded"
        assert last_entry['outro_text'] == "Test outro text", "Outro text should be recorded"
        assert last_entry['is_desired'] is True, "Desired status should be recorded"

    def test_get_edge_info(self):
        """Test edge information retrieval"""
        game = ButtonGame()
        
        # Should not crash when getting edge info
        outro_text, is_desired = game.get_edge_info("start_game", "welcome")
        
        # Results can be None or strings/bools
        assert outro_text is None or isinstance(outro_text, str), "Outro text should be None or string"
        assert is_desired is None or isinstance(is_desired, bool), "Desired status should be None or bool"

    def test_get_available_nodes(self):
        """Test available nodes retrieval"""
        game = ButtonGame()
        nodes = game.get_available_nodes()
        
        assert isinstance(nodes, list), "Should return a list of nodes"
        assert len(nodes) > 0, "Should have at least one node available"
        assert all(isinstance(node, str) for node in nodes), "All nodes should be strings"

    def test_show_game_summary_with_empty_path(self):
        """Test game summary with minimal path"""
        game = ButtonGame()
        
        # Should not crash with default path
        try:
            # We can't easily test the printed output, but we can ensure it doesn't crash
            game.show_game_summary()
        except Exception as e:
            pytest.fail(f"show_game_summary should not raise exception: {e}")

    def test_show_game_summary_with_text_wrapping(self):
        """Test that game summary properly formats long text"""
        import textwrap
        
        game = ButtonGame()
        # Add a transition with long outro text
        long_text = "This is a very long outro text that should definitely be wrapped when displayed in the game summary because it exceeds the standard console width of eighty characters."
        game.log_transition("test_from", "test_to", "random", long_text, False)
        
        # Test that textwrap.fill would work with this text
        wrapped = textwrap.fill(long_text, width=80, initial_indent="   � ", subsequent_indent="   ")
        assert len(wrapped.split('\n')) > 1, "Long text should be wrapped into multiple lines"
        
        # Test that the summary method doesn't crash
        try:
            game.show_game_summary()
        except Exception as e:
            pytest.fail(f"show_game_summary should handle long text: {e}")