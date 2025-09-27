import networkx as nx
import matplotlib.pyplot as plt
from classes.button_dat import ButtonDat
from classes.story_graph import StoryGraph

# Load and display the game data
game_data = ButtonDat()
print("Edges data:")
print(game_data.edges_df.head())
print("\nNodes data:")
print(game_data.nodes_df.head())
print("\nText data:")
print(game_data.text_df.head())
# print("\nTitles data:")
# print(game_data.titles_df.head())

# Create and save the story graph
story_graph = StoryGraph()
story_graph.create_and_save_graph()

# Example of using the new ButtonDat methods
print(f"\nAll nodes in game: {game_data.get_all_nodes()}")
print(f"Connections from 'start_game': {game_data.get_connections('start_game')}")

# Validate the data
issues = game_data.validate_data()
if issues:
    print(f"\nData validation issues: {issues}")
else:
    print("\nData validation: All good!")