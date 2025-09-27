import pytest
import textwrap
from button_1.classes.node_engine import NodeEngine
from button_1.classes.button_dat import ButtonDat


class TestTextWrapping:
    """Test suite for text wrapping functionality across the game"""

    def test_node_engine_wrap_text(self):
        """Test NodeEngine text wrapping method"""
        game_data = ButtonDat()
        engine = NodeEngine(game_data)
        
        # Test with short text (should remain unchanged)
        short_text = "Short text"
        wrapped_short = engine.wrap_text(short_text)
        assert wrapped_short == short_text, "Short text should remain unchanged"
        
        # Test with long text (should be wrapped)
        long_text = "This is a very long text that should definitely be wrapped when processed through the wrap_text method because it exceeds the standard console width."
        wrapped_long = engine.wrap_text(long_text)
        lines = wrapped_long.split('\n')
        assert len(lines) > 1, "Long text should be wrapped into multiple lines"
        assert all(len(line) <= 80 for line in lines), "All lines should be 80 characters or less"

    def test_wrap_text_with_custom_width(self):
        """Test text wrapping with custom width"""
        game_data = ButtonDat()
        engine = NodeEngine(game_data)
        
        long_text = "This is a long text that will be wrapped at different widths for testing purposes."
        
        # Test with width 40
        wrapped_40 = engine.wrap_text(long_text, width=40)
        lines_40 = wrapped_40.split('\n')
        assert all(len(line) <= 40 for line in lines_40), "All lines should be 40 characters or less"
        
        # Test with width 60  
        wrapped_60 = engine.wrap_text(long_text, width=60)
        lines_60 = wrapped_60.split('\n')
        assert all(len(line) <= 60 for line in lines_60), "All lines should be 60 characters or less"
        
        # Shorter width should create more lines
        assert len(lines_40) >= len(lines_60), "Shorter width should create more or equal lines"

    def test_wrap_text_with_none_or_empty(self):
        """Test text wrapping with edge cases"""
        game_data = ButtonDat()
        engine = NodeEngine(game_data)
        
        # Test with None
        assert engine.wrap_text(None) is None, "None input should return None"
        
        # Test with empty string
        assert engine.wrap_text("") == "", "Empty string should return empty string"
        
        # Test with whitespace only
        whitespace_text = "   \n  \t  "
        wrapped = engine.wrap_text(whitespace_text)
        assert isinstance(wrapped, str), "Should return a string even for whitespace"

    def test_textwrap_integration(self):
        """Test that our wrapping integrates properly with Python's textwrap module"""
        # Test the exact pattern used in ButtonGame.show_game_summary()
        test_text = "Oh, no! Something isn't quite right. During your presentation one of the stakeholders points out there's no integration of a data source that was never mentioned until now."
        
        wrapped = textwrap.fill(test_text, width=80, 
                               initial_indent="   � ", subsequent_indent="   ")
        
        lines = wrapped.split('\n')
        assert lines[0].startswith("   � "), "First line should have bullet point"
        assert all(line.startswith("   ") for line in lines[1:]), "Continuation lines should be indented"
        assert all(len(line) <= 80 for line in lines), "All lines should be within width limit"

    def test_console_display_formatting(self):
        """Test that display methods would produce properly formatted output"""
        game_data = ButtonDat()
        engine = NodeEngine(game_data)
        
        # Test various text lengths that might appear in the game
        texts = [
            "Short intro.",
            "Medium length introduction text that provides context for the current game state and situation.",
            "Very long introduction text that describes the complex situation the player finds themselves in, with multiple clauses and detailed explanations that would definitely exceed normal console width limits and require proper text wrapping to maintain readability in the terminal environment."
        ]
        
        for text in texts:
            wrapped = engine.wrap_text(text)
            lines = wrapped.split('\n')
            
            # All lines should be reasonable length
            assert all(len(line) <= 80 for line in lines), f"Text should be wrapped properly: {text[:50]}..."
            
            # Content should be preserved (ignoring whitespace changes)
            original_words = text.split()
            wrapped_words = wrapped.replace('\n', ' ').split()
            assert original_words == wrapped_words, "Text content should be preserved during wrapping"