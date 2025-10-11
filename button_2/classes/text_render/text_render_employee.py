from ..text_gen.textgen_employee import EmployeeTextGenerator

class EmployeeTextRenderer:
    def __init__(self, employee_text_gen: EmployeeTextGenerator):
        self.employee_text_gen = employee_text_gen
        self.rendered_text = self.render_text()

    def render_text(self) -> str:
        # We need to apply string wrapping in renderers.
        return self.employee_text_gen.employee_text
