from button_1.classes.button_df import ButtonDf

def test_button_df_edges_non_empty():
    button_df = ButtonDf('edges')
    assert button_df.df is not None, "ButtonDf.df should not be None after initialization, sheet name likely misspecified or env vars missing"
    assert not button_df.df.empty, "ButtonDf.df should not be empty after initialization, sheet name likely misspecified or env vars missing"

def test_button_df_nodes_non_empty():
    button_df = ButtonDf('nodes')
    assert button_df.df is not None, "ButtonDf.df should not be None after initialization, sheet name likely misspecified or env vars missing"
    assert not button_df.df.empty, "ButtonDf.df should not be empty after initialization, sheet name likely misspecified or env vars missing"
