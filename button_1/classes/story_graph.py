import networkx as nx
import matplotlib.pyplot as plt 
from .button_dat import ButtonDat

class StoryGraph(ButtonDat):
    def __init__(self):
        super().__init__()
        # Create directed graph from edges DataFrame
        self.graph = nx.from_pandas_edgelist(
            self.edges_df,
            source='source',
            target='target',
            create_using=nx.DiGraph
        )

    def _get_node_colors(self):
        """Generate node colors based on edge_selector attribute"""
        # Murky chic color mapping - sophisticated earth tones
        color_map = {
            'auto': '#2F4F4F',        # Dark slate gray - automatic progression
            'choice': '#556B2F',      # Dark olive green - player choice points
            'condition': '#CD853F',   # Peru/burnt ochre - conditional branches
            'random': '#8B4513',      # Saddle brown - random outcomes
            'input': '#B8860B',       # Dark goldenrod - user input required
            'end': '#800000',         # Maroon - end points
            'start': '#483D8B',       # Dark slate blue - start points
        }
        default_color = '#696969'     # Dim gray - unknown/other
        
        node_colors = []
        for node in self.graph.nodes():
            # Look up the edge_selector for this node in nodes_df
            if 'node' in self.nodes_df.columns and 'edge_selector' in self.nodes_df.columns:
                node_data = self.nodes_df[self.nodes_df['node'] == node]
                if not node_data.empty:
                    edge_selector = node_data.iloc[0]['edge_selector']
                    color = color_map.get(edge_selector, default_color)
                    node_colors.append(color)
                else:
                    node_colors.append(default_color)
            else:
                node_colors.append(default_color)
        
        return node_colors

    def _create_multiline_labels(self):
        """Create multiline labels by splitting on underscores"""
        labels = {}
        for node in self.graph.nodes():
            # Split on underscore and join with newline
            label_parts = node.split('_')
            labels[node] = '\n'.join(label_parts)
        return labels

    def plot_graph(self):
        # Set up the figure with appropriate size
        plt.figure(figsize=(18, 10))

        # Create left-to-right layout with improved spacing
        pos = nx.nx_agraph.graphviz_layout(
            self.graph, 
            prog="dot", 
            args='-Grankdir=LR -Gnodesep=2.0 -Granksep=3.0 -Gdpi=150 -Gsplines=true'
        )

        # Get node colors based on edge_selector
        node_colors = self._get_node_colors()
        
        # Create multiline labels
        labels = self._create_multiline_labels()

        # Draw the graph without labels first
        nx.draw(
            self.graph, pos,
            with_labels=False,        # We'll add custom labels separately
            node_color=node_colors,
            edge_color='#4A4A4A',     # Darker gray for edges
            node_size=2500,           # Slightly larger to accommodate multi-line text
            arrows=True,
            arrowsize=30,
            arrowstyle='->',
            edgecolors='#2F2F2F',     # Dark gray node borders
            linewidths=2,             # Thicker borders for definition
            alpha=0.7                 # Make nodes semi-transparent for text readability
        )
        
        # Add custom multiline labels with better positioning
        for node, (x, y) in pos.items():
            plt.text(x, y, labels[node], 
                    horizontalalignment='center',
                    verticalalignment='center',
                    fontsize=8,
                    fontweight='bold',
                    color='white',
                    bbox=dict(boxstyle="round,pad=0.1", 
                             facecolor='black', 
                             alpha=0.3,
                             edgecolor='none'))
        
        # Add a legend for the color coding
        self._add_color_legend()

    def _add_color_legend(self):
        """Add a legend showing what each color represents"""
        from matplotlib.patches import Patch
        
        legend_elements = [
            Patch(facecolor='#2F4F4F', label='Auto progression', edgecolor='#2F2F2F'),
            Patch(facecolor='#556B2F', label='Player choice', edgecolor='#2F2F2F'),
            Patch(facecolor='#CD853F', label='Conditional branch', edgecolor='#2F2F2F'),
            Patch(facecolor='#8B4513', label='Random outcome', edgecolor='#2F2F2F'),
            Patch(facecolor='#B8860B', label='User input', edgecolor='#2F2F2F'),
            Patch(facecolor='#800000', label='End point', edgecolor='#2F2F2F'),
            Patch(facecolor='#483D8B', label='Start point', edgecolor='#2F2F2F'),
            Patch(facecolor='#696969', label='Unknown/Other', edgecolor='#2F2F2F')
        ]
        
        plt.legend(handles=legend_elements, loc='upper left', bbox_to_anchor=(1, 1), 
                  fancybox=True, shadow=True, facecolor='#F5F5DC', edgecolor='#8B7355')

    def get_node_type_stats(self):
        """Get statistics about different node types in the game"""
        if 'node' not in self.nodes_df.columns or 'edge_selector' not in self.nodes_df.columns:
            return "Node type statistics not available - missing required columns"
        
        stats = self.nodes_df['edge_selector'].value_counts().to_dict()
        
        print("\n=== Game Structure Statistics ===")
        for selector_type, count in stats.items():
            print(f"{selector_type}: {count} nodes")
        
        total_nodes = len(self.get_all_nodes())
        print(f"\nTotal nodes in game: {total_nodes}")
        print(f"Nodes with metadata: {len(self.nodes_df)}")
        
        return stats

    def save_graph(self):
        # Save with tight bounding box to ensure everything fits
        plt.savefig("button_1/vis/graph.png", bbox_inches="tight", dpi=300)

    def create_and_save_graph(self):
        """Convenience method to plot and save graph in one call"""
        print("=== Creating Story Graph Visualization ===")
        self.get_node_type_stats()  # Show development statistics
        self.plot_graph()
        self.save_graph()
        print(f"Graph saved to button_1/vis/graph.png")
