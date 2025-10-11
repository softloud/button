import pandas as pd
import os
from pathlib import Path

class ButtonDat:
    def __init__(self):
        # Get the directory where this file is located
        current_dir = Path(__file__).parent
        # Navigate to the data directory
        data_dir = current_dir.parent.parent / 'data'
        
        self.edges_df = pd.read_csv(data_dir / 'edges.csv')
        self.nodes_df = pd.read_csv(data_dir / 'nodes.csv')
        self.text_df = pd.read_csv(data_dir / 'text.csv')
        self.employee_df = pd.read_csv(data_dir / 'employee.csv')