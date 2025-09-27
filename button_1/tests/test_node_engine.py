import pytest
from button_1.classes.button_dat import ButtonDat
from button_1.classes.node_engine import NodeEngine


class TestNodeEngine:
    """Test suite for NodeEngine class"""
    
    def test_node_engine_initialization(self):
        """Test that NodeEngine initializes correctly"""
        game_data = ButtonDat()
        engine = NodeEngine(game_data, starting_node="start_game")
        
        assert engine.current_node == "start_game", "Should initialize with correct starting node"
        assert engine.button_dat is not None, "Should have game data reference"
        assert engine.game_running is True, "Game should be running initially"
    
    def test_get_edge_selector(self):
        """Test edge selector retrieval"""
        game_data = ButtonDat()
        engine = NodeEngine(game_data)
        
        # Should return a string (either from data or default 'auto')
        selector = engine.get_edge_selector("start_game")
        assert isinstance(selector, str), "Edge selector should be a string"
    
    def test_determine_next_node(self):
        """Test next node determination logic"""
        game_data = ButtonDat()
        engine = NodeEngine(game_data)
        
        # Should return None or a string (node name)
        next_node = engine.determine_next_node("start_game")
        assert next_node is None or isinstance(next_node, str), "Next node should be None or string"
    
    def test_get_node_column_text(self):
        """Test text retrieval for nodes from DataFrame columns"""
        game_data = ButtonDat()
        engine = NodeEngine(game_data)
        
        # Should not crash when looking for text
        text = engine.get_node_column_text("start_game", "intro_text")
        assert text is None or isinstance(text, str), "Text should be None or string"
    
    def test_run_single_node(self):
        """Test single node execution"""
        game_data = ButtonDat()
        engine = NodeEngine(game_data)
        
        # This test is tricky because it requires input
        # For now, just test that the method exists and can be called
        assert hasattr(engine, 'run_single_node'), "Should have run_single_node method"
        
        # Test with a mock or skip actual execution for automated testing
        # We'll expand this test later when we add input mocking

    def test_get_edge_outro_text(self):
        """Test outro text retrieval from edges"""
        game_data = ButtonDat()
        engine = NodeEngine(game_data)
        
        # Should return None or string
        outro = engine.get_edge_outro_text("start_game", "welcome")
        assert outro is None or isinstance(outro, str), "Outro text should be None or string"

    def test_get_combined_outro_text(self):
        """Test combined outro text with edge feedback"""
        game_data = ButtonDat()
        engine = NodeEngine(game_data)
        
        # Should return None or string
        combined = engine.get_combined_outro_text("start_game", "welcome")
        assert combined is None or isinstance(combined, str), "Combined outro should be None or string"

    def test_get_edge_desired_status(self):
        """Test edge desired status retrieval"""
        game_data = ButtonDat()
        engine = NodeEngine(game_data)
        
        # Should return None or boolean
        desired = engine.get_edge_desired_status("start_game", "welcome")
        assert desired is None or isinstance(desired, bool), "Desired status should be None or bool"

    def test_display_methods_exist(self):
        """Test that all display methods exist and are callable"""
        game_data = ButtonDat()
        engine = NodeEngine(game_data)
        
        display_methods = ['display_title', 'display_intro', 'display_event', 'display_outro']
        
        for method_name in display_methods:
            assert hasattr(engine, method_name), f"Should have {method_name} method"
            method = getattr(engine, method_name)
            assert callable(method), f"{method_name} should be callable"

    def test_developer_mode_flag(self):
        """Test developer mode initialization and behavior"""
        game_data = ButtonDat()
        
        # Test production mode
        prod_engine = NodeEngine(game_data, developer_mode=False)
        assert prod_engine.developer_mode is False, "Production mode should be disabled"
        
        # Test developer mode
        dev_engine = NodeEngine(game_data, developer_mode=True)
        assert dev_engine.developer_mode is True, "Developer mode should be enabled"