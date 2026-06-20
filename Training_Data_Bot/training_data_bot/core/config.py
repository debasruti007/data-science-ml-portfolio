import os
from typing import Any, Dict

class Settings:
    """The rule book for the factory"""
    def __init__(self):
        self.PROJECT_NAME: str = "Training Data Curation Bot"
        self.VERSION: str = "0.1.0"
        self.MAX_WORKERS: int = int(os.getenv("MAX_WORKERS", "4"))
        # Add API keys and other environment variables here

settings = Settings()