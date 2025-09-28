import marimo

__generated_with = "0.16.2"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    return (mo,)


@app.cell
def _(mo):
    mo.md(r"""## employee text generator""")
    return


@app.cell
def _():
    from classes.entities.employee import Employee
    return (Employee,)


@app.cell
def _(Employee):
    employee = Employee()
    return (employee,)


@app.cell
def _(employee):
    employee.employee_id
    return


@app.cell
def _(employee):
    employee.job_title
    return


@app.cell
def _(employee):
    employee.department
    return


if __name__ == "__main__":
    app.run()
