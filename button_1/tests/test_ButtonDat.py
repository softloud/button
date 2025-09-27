from button_1.classes.button_dat import ButtonDat

def test_button_data_non_empty():
    button_data = ButtonDat('edges')
    assert button_data.df is not None, "ButtonDat.df should not be None after initialization, sheet name likely misspecified or env vars missing"
    assert not button_data.df.empty, "ButtonDat.df should not be empty after initialization, sheet name likely misspecified or env vars missing"
