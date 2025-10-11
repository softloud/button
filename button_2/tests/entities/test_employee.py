from button_2.classes.entities.employee import Employee
import pandas as pd
from button_2.classes.data.button_dat import ButtonDat

button_dat = ButtonDat()
employee = Employee(
    job_title=button_dat.employee_df.iloc[0]['job_title'] if not button_dat.employee_df.empty else None,
    department=button_dat.employee_df.iloc[0]['department'] if not button_dat.employee_df.empty else None
)

def test_employee_init():
    assert employee is not None
    assert hasattr(employee, 'employee_id') 
    assert hasattr(employee, 'job_title')
    assert hasattr(employee, 'department')

def test_employee_methods():
    assert callable(employee.reorg), (
        "Employee should have a callable reorg method"
    )

def test_texgen_employee_attributes():
    assert employee.employee_id is not None
    assert employee.job_title is not None
    assert employee.department is not None

def helper_test_reorg_method():
    # this helper is a single trial that:
    # instantiates employee
    # stores initial state
    # calls reorg
    # checks if state changed
    # low probability of change expected, 
    # so will run multiple times in main test

    initial_state = (employee.job_title, employee.department)
    employee.set_current_titles(
        job_titles=button_dat.employee_df['job_title'].dropna().values,
        departments=button_dat.employee_df['department'].dropna().values
    )
    new_state = (employee.job_title, employee.department)
    return {"state_change": initial_state != new_state, 
            "job_title": employee.job_title,
            "department": employee.department}

def test_employee_reorg_method_changes_state():
    # run the helper multiple times to statistically verify change
    
    trials = 1000

    # we don't want the reorg to happen too often, say 0.1 true probability
    probability_threshold = 0.20

    simulation = [helper_test_reorg_method() for _ in range(trials)]

    sim_df = pd.DataFrame(simulation)

    changes = sum(sim_df['state_change'])


    assert changes > 0, (
        "reorg method should change employee state occasionally"
        )
    assert changes / trials < probability_threshold, (
        "reorg method should not change employee state too frequently"
        ) 
    # check generated job titles are expected values from employee df
    assert set(sim_df["job_title"].unique()).issubset(
        set(button_dat.employee_df["job_title"].unique())
        ), "Unexpected job titles generated"

    # check generated departments are expected values from employee df
    assert set(sim_df["department"].unique()).issubset(
        set(button_dat.employee_df["department"].unique())
        ), "Unexpected departments generated"

