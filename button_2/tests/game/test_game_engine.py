import pytest
from button_2.classes.game.game_engine import GameEngine

# this tests that the game engine has the required attributes & methods

# instantiate the game engine
# nb this is where I will pass hyper parameters to tweak probabilities

@pytest.fixture
def button_game():
    button_game = GameEngine()
    return button_game

# test the game engine is a thing
def test_game_engine(button_game: GameEngine):
    assert button_game is not None

# required attributes
def test_game_engine_attributes(button_game: GameEngine):
    assert hasattr(button_game, 'button_dat')
    assert hasattr(button_game, 'employee')
    assert hasattr(button_game, 'current_node')
    assert hasattr(button_game, 'narrative_path')
    assert hasattr(button_game, 'nodes_visited')

# required methods
