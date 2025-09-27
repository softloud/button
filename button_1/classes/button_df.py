import pandas as pd
import os
from dotenv import load_dotenv
import pandas as pd


load_dotenv()  # Loads environment variables from .env

# format for reading a googlesheet into pandas
# https://docs.google.com/spreadsheets/d/[SHEET_ID]/export?format=csv&gid=[SHEET_GID]

class ButtonDf:
    def __init__(self, sheet_name):
        # internal sheet id and gid protected
        self._sheet_id = os.getenv("BUTTON_SHEET_ID")
        if sheet_name == 'edges':
            self._sheet_gid = os.getenv("BUTTON_SHEET_EDGES_GID")
        elif sheet_name == 'nodes':
            self._sheet_gid = os.getenv("BUTTON_SHEET_NODES_GID")
        elif sheet_name == 'text':
            self._sheet_gid = os.getenv("BUTTON_SHEET_TEXT_GID")
        elif sheet_name == 'titles':
            self._sheet_gid = os.getenv("BUTTON_SHEET_TITLES_GID")
        else:
            raise ValueError("Unknown sheet name")
        self.data_url = f"https://docs.google.com/spreadsheets/d/{self._sheet_id}/export?format=csv&gid={self._sheet_gid}"
        
        # set df as fundamental public attribute
        self.df = pd.read_csv(self.data_url)