"""Application settings (Singleton pattern)."""

import os

from dotenv import load_dotenv


class AppConfig:
    """Single shared config instance for API key and limits."""

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._loaded = False
        return cls._instance

    def load(self):
        if not self._loaded:
            load_dotenv()
            self._loaded = True

    @property
    def api_key(self):
        self.load()
        return os.getenv("OPENAI_API_KEY", "")

    @property
    def max_chars(self):
        return 12000

    @property
    def history_path(self):
        return os.path.join("data", "analysis_history.json")
