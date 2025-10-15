from ..data.button_dat import ButtonDat
from ..entities.employee import Employee
from .node_engine import NodeEngine

class GameEngine:
    def __init__(self):
        self.button_dat = ButtonDat()
        self.employee = Employee(self.button_dat)
        self.current_node = self.button_dat.nodes_df.node.iloc[0]
        self.narrative_path = [self.current_node]
        self.nodes_visited = {self.current_node: 1}
        self.node = NodeEngine(self.button_dat, self.employee)

