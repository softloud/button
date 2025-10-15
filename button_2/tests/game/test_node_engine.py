from classes.data.button_dat import ButtonDat
from classes.entities.employee import Employee

button_dat = ButtonDat()
employee = Employee(button_dat)

def test_node_engine_attributes(node_engine):
    assert hasattr(node_engine, 'button_dat')
    assert hasattr(node_engine, 'employee')
    assert hasattr(node_engine, 'current_node')
    assert hasattr(node_engine, 'next_edge')

def test_node_engine_methods(node_engine):
    assert callable(node_engine.select_next_edge)
    # assert that next edge attribute is unset at init
    assert node_engine.next_edge is None
    # assert that select_next_edge sets next_edge
    node_engine.select_next_edge()
    assert node_engine.next_edge is not None
    # assert that next_edge is in button_dat.nodes_df.nodes
    assert node_engine.next_edge in button_dat.nodes_df.nodes
