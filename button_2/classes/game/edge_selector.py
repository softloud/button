from ..data.button_dat import ButtonDat
from ..entities.employee import Employee

class EdgeSelector:
    def __init__(self, button_dat: ButtonDat, employee: Employee, current_node=None):
        self.button_dat = button_dat
        self.employee = employee
        self.current_node = current_node
        self.next_edge = None

    def set_current_node(self, node):
        self.current_node = node
        self.next_edge = None

    def select_next_edge(self):
        if self.current_node is None:
            raise ValueError("Current node is not set.")
        
        # Logic to select the next edge
        connections = self.button_dat.edges_df[
            self.button_dat.edges_df['source'] == self.current_node
        ]

        # perhaps I need an edge id to refer to here
        if not connections.empty:
            self.next_edge = connections.target.iloc[0]
        else:
            self.next_edge = None
