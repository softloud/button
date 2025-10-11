from ..entities.employee import Employee

class NodeContext:
    def __init__(
            self, 
            employee: Employee#, 
            # node_name: str, 
            # game_path: str, 
            # button_dat: str, 
            # choices: list = None, 
            # text_type: str = None
            ):
        self.employee = employee
        # self.node_name = node_name
        # self.game_path = game_path
        # self.button_dat = button_dat
        # self.choices = choices or []
        # self.text_type = text_type