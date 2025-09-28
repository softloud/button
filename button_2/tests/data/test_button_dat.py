from button_2.classes.data.button_dat import ButtonDat

def test_button_dat_initialisation():
    """Test that ButtonDat initializes correctly with both datasets"""
    game_data = ButtonDat()
    
    # Test that both DataFrames exist
    assert hasattr(game_data, 'edges_df'), "ButtonDat should have edges_df attribute"
    assert hasattr(game_data, 'nodes_df'), "ButtonDat should have nodes_df attribute"
    assert hasattr(game_data, 'text_df'), "ButtonDat should have text_df attribute"
    assert hasattr(game_data, 'employee_df'), "ButtonDat should have employee_df attribute"

    # Test DataFrames are not empty
    assert not game_data.edges_df.empty, "Edges DataFrame should not be empty"
    assert not game_data.nodes_df.empty, "Nodes DataFrame should not be empty"
    assert not game_data.text_df.empty, "Text DataFrame should not be empty"
    assert not game_data.employee_df.empty, "Employee DataFrame should not be empty"