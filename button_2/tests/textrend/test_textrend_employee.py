from button_2.classes.entities.employee import Employee
from button_2.classes.data.button_dat import ButtonDat
from button_2.classes.text_gen.textgen_employee import EmployeeTextGenerator
from button_2.classes.text_render.text_render_employee import EmployeeTextRenderer

button_dat = ButtonDat()
employee = Employee(button_dat)
employee_text = EmployeeTextGenerator(employee)

def test_employee_text_renderer():
    employee_text_renderer = EmployeeTextRenderer(employee_text)
    
    # More comprehensive assertions
    assert employee_text_renderer.rendered_text is not None
    assert isinstance(employee_text_renderer.rendered_text, str)
    assert len(employee_text_renderer.rendered_text) > 0

def test_employee_text_renderer_type():
    employee_text_renderer = EmployeeTextRenderer(employee_text)
    assert hasattr(employee_text_renderer, 'rendered_text')

def test_employee_text_renderer_consistency():
    employee_text_renderer = EmployeeTextRenderer(employee_text)
    
    # Should return same result on multiple calls
    first_render = employee_text_renderer.rendered_text
    second_render = employee_text_renderer.rendered_text
    assert first_render == second_render