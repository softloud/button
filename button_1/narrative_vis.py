import pandas as pd
import os

# format for reading a googlesheet into pandas
# https://docs.google.com/spreadsheets/d/[SHEET_ID]/export?format=csv&gid=[SHEET_GID]


def get_data_url(sheet_name):
    sheet_id = os.getenv("BUTTON_SHEET_ID")
    if sheet_name == 'edges':
        sheet_gid = os.getenv("BUTTON_SHEET_EDGES_GID")
    elif sheet_name == 'nodes':
        sheet_gid = os.getenv("BUTTON_SHEET_NODES_GID")
    else:
        raise ValueError("Unknown sheet name")
    return f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid={sheet_gid}"

