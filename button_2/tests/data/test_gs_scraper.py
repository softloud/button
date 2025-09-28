from button_2.classes.data.gs_scraper import GsScraper

def test_gs_scraper_edges_non_empty():
    gs_scraper = GsScraper('edges')
    assert gs_scraper.df is not None, "GsScraper.df should not be None after initialization, sheet name likely misspecified or env vars missing"
    assert not gs_scraper.df.empty, "GsScraper.df should not be empty after initialization, sheet name likely misspecified or env vars missing"

def test_gs_scraper_nodes_non_empty():
    gs_scraper = GsScraper('nodes')
    assert gs_scraper.df is not None, "GsScraper.df should not be None after initialization, sheet name likely misspecified or env vars missing"
    assert not gs_scraper.df.empty, "GsScraper.df should not be empty after initialization, sheet name likely misspecified or env vars missing"
