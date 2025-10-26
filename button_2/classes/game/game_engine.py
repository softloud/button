from ..data.button_dat import ButtonDat
from ..entities.employee import Employee
from .node_engine import NodeEngine
from ..text_gen.textgen_employee import EmployeeTextGenerator
from ..text_render.text_render_employee import EmployeeTextRenderer

class GameEngine:
    def __init__(self):
        self.button_dat = ButtonDat()
        self.employee = Employee(self.button_dat)
        self.current_node = self.button_dat.nodes_df.node.iloc[0]
        self.narrative_path = [self.current_node]
        self.nodes_visited = {self.current_node: 1}
        self.node = NodeEngine(self.button_dat, self.employee)
    
    def start_game(self):
        employee_text = EmployeeTextGenerator(self.employee)
        employee_text_rendered = EmployeeTextRenderer(employee_text)
        print(f"{employee_text_rendered.rendered_text}")
        

