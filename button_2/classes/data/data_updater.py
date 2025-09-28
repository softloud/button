from classes.data.gs_scraper import GsScraper

class DataUpdater:
    def __init__(self):
        self.edges = GsScraper('edges')
        self.nodes = GsScraper('nodes')
        self.text = GsScraper('text')
        self.employee = GsScraper('employee')
  
    def update_all(self):
        self.edges.df.to_csv('button_2/data/edges.csv', index=False)
        self.nodes.df.to_csv('button_2/data/nodes.csv', index=False)
        self.text.df.to_csv('button_2/data/text.csv', index=False)
        self.employee.df.to_csv('button_2/data/employee.csv', index=False)