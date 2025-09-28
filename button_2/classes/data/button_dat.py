import pandas as pd

class ButtonDat:
    def __init__(self):
        self.edges_df = pd.read_csv('button_2/data/edges.csv')
        self.nodes_df = pd.read_csv('button_2/data/nodes.csv')
        self.text_df = pd.read_csv('button_2/data/text.csv')
        self.employee_df = pd.read_csv('button_2/data/employee.csv')
