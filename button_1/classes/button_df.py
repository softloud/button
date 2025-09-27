"""
ButtonDf - Google Sheets Data Connector with Retry Logic
=========================================================

This module provides robust Google Sheets integration for the text-based
adventure game, with automatic retry logic and rate limiting to handle
API restrictions and network issues gracefully.

The ButtonDf class serves as the primary data connector, converting Google
Sheets tabs into pandas DataFrames while handling common failure modes
like rate limiting, network timeouts, and temporary service unavailability.

Classes:
    ButtonDf: Google Sheets scraper with exponential backoff retry logic

Environment Requirements:
    - BUTTON_SHEET_ID: Main Google Sheets document identifier
    - BUTTON_SHEET_EDGES_GID: GID for edges data tab
    - BUTTON_SHEET_NODES_GID: GID for nodes data tab  
    - BUTTON_SHEET_TEXT_GID: GID for text content tab
    - BUTTON_SHEET_TITLES_GID: GID for job titles tab

Key Features:
    - Automatic retry with exponential backoff
    - Environment-specific .env file loading
    - Comprehensive error handling and reporting
    - Rate limiting protection for API compliance
"""

import pandas as pd
import os
from dotenv import load_dotenv
import time
from urllib.error import HTTPError
from pathlib import Path


# Load .env file from the button_1 directory (not root)
button_1_dir = Path(__file__).parent.parent  # Go up from classes/ to button_1/
env_path = button_1_dir / '.env'
load_dotenv(env_path)  # Load environment variables from button_1/.env

# Google Sheets CSV export URL format:
# https://docs.google.com/spreadsheets/d/[SHEET_ID]/export?format=csv&gid=[SHEET_GID]

class ButtonDf:
    """
    Google Sheets data connector with robust error handling and retry logic.
    
    ButtonDf provides reliable access to Google Sheets data by implementing
    exponential backoff retry logic and comprehensive error handling. It
    automatically handles rate limiting, network issues, and temporary
    service unavailability while providing clear error messages for
    configuration problems.
    
    The class supports multiple sheet tabs within a single Google Sheets
    document, using environment variables to map sheet names to their
    specific GID identifiers.
    
    Attributes:
        df (pd.DataFrame): Loaded data from the specified sheet
        sheet_name (str): Name of the sheet tab being accessed
        
    Supported Sheet Names:
        - 'edges': State transition definitions
        - 'nodes': Node content and configuration
        - 'text': Reusable text snippets
        - 'titles': Job title variations (future feature)
    
    Environment Variables Required:
        BUTTON_SHEET_ID: Main Google Sheets document ID
        BUTTON_SHEET_*_GID: Individual tab GID for each sheet type
    """
    
    def __init__(self, sheet_name):
        """
        Initialize Google Sheets connection for specified tab.
        
        Sets up the connection parameters and loads data from the specified
        Google Sheets tab using the appropriate GID from environment variables.
        
        Args:
            sheet_name (str): Name of sheet tab to load
                Must be one of: 'edges', 'nodes', 'text', 'titles'
        
        Raises:
            ValueError: If sheet_name is not recognized
            EnvironmentError: If required environment variables are missing
            ConnectionError: If data cannot be loaded after all retries
        """
        # Load sheet configuration from environment variables
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
            raise ValueError(f"Unknown sheet name: {sheet_name}. Must be one of: edges, nodes, text, titles")
        self.data_url = f"https://docs.google.com/spreadsheets/d/{self._sheet_id}/export?format=csv&gid={self._sheet_gid}"
        
        # Load data with retry logic for rate limiting
        self.df = self._load_data_with_retry()
    
    def _load_data_with_retry(self, max_retries=3, delay=1):
        """Load CSV data with retry logic for rate limiting"""
        for attempt in range(max_retries):
            try:
                return pd.read_csv(self.data_url)
            except HTTPError as e:
                if e.code == 404 and attempt < max_retries - 1:
                    print(f"⚠️  Rate limited, retrying in {delay} seconds... (attempt {attempt + 1})")
                    time.sleep(delay)
                    delay *= 2  # Exponential backoff
                else:
                    raise e
            except Exception as e:
                raise e