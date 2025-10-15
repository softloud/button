from ..data.button_dat import ButtonDat
from ..entities.employee import Employee
from ..game.edge_selector import EdgeSelector

class NodeEngine:
    def __init__(
        self, button_dat: ButtonDat, employee: Employee
    ):
        self.button_dat = button_dat
        self.employee = employee
        self.current_node = button_dat.nodes_df.node.iloc[0]
        self.next_edge = None
        self.edge_selector = EdgeSelector(
            button_dat, employee, self.current_node
            )

    def select_next_edge(self):
        self.edge_selector.set_current_node(self.current_node)
        self.edge_selector.select_next_edge()
        self.next_edge = self.edge_selector.next_edge
