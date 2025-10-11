from button_2.classes.text_gen.textgen_employee import EmployeeTextGenerator
from button_2.classes.entities.employee import Employee
from button_2.classes.data.button_dat import ButtonDat

button_dat = ButtonDat()
employee = Employee(button_dat)

# assert that the text generator works
def test_employee_text_generator():

    text_generator = EmployeeTextGenerator(employee)
    assert text_generator is not None

# assert that the text generator has attributes:
# job_title
# department

def test_employee_text_generator_attributes():
    text_generator = EmployeeTextGenerator(employee)
    assert hasattr(text_generator, "job_title")
    assert hasattr(text_generator, "department")