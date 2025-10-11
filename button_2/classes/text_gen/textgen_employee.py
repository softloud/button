from ..entities.employee import Employee

class EmployeeTextGenerator():

    def __init__(self, employee: Employee):
        employee.set_current_titles()

        self.job_title = employee.job_title
        self.department = employee.department
        self.employee_text = self.generate_employee_text()

    def generate_employee_text(self) -> str:
        return f"Your day begins as a {self.job_title} in the {self.department} department."
