import random 
from classes.data.button_dat import ButtonDat

class Employee:
    def __init__(self, button_dat: ButtonDat):
        self.employee_id = "#eilaslv426ekaceht", 
        self.job_title = button_dat.employee_df.job_title[0]
        self.department = button_dat.employee_df.department[0]
        self.button_dat = button_dat

    def reorg(self):
        self.job_title = random.choice(self.button_dat.employee_df.job_title)
        self.department = random.choice(self.button_dat.employee_df.department)

    def set_current_titles(self):
        reorg_now = random.choices([True, False], weights=[0.1, 0.9])[0]
        if reorg_now:
            self.reorg()