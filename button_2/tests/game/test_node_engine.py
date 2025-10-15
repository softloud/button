import pytest
from button_2.classes.data.button_dat import ButtonDat
from button_2.classes.entities.employee import Employee
from button_2.classes.game.node_engine import NodeEngine

@pytest.fixture
def node_engine():
    button_dat = ButtonDat()
    employee = Employee(button_dat)
    return NodeEngine(button_dat, employee)

def test_node_engine_attributes(node_engine):
    assert hasattr(node_engine, 'button_dat')
    assert hasattr(node_engine, 'employee')
    assert hasattr(node_engine, 'current_node')
    assert hasattr(node_engine, 'next_edge')

def test_node_engine_methods(node_engine):
    assert callable(node_engine.select_next_edge)
    assert node_engine.next_edge is None
    node_engine.select_next_edge()
    assert node_engine.next_edge is not None
    assert node_engine.next_edge in (
        node_engine.button_dat.nodes_df.node.tolist()
    )