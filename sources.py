"""Document sources: abstraction, inheritance, polymorphism."""

import os
import re

import requests

from config import AppConfig


class DocumentSource:
    """Abstract base for reading document text."""

    def fetch_text(self):
        raise NotImplementedError


class UrlDocumentSource(DocumentSource):
    """Fetch and strip text from a web page."""

    def __init__(self, url):
        self._url = url
        self._config = AppConfig()

    def fetch_text(self):
        response = requests.get(
            self._url,
            headers={"User-Agent": "DocumentAnalyzer/1.0"},
            timeout=30,
        )
        response.raise_for_status()
        text = re.sub(r"<[^>]+>", " ", response.text)
        text = re.sub(r"\s+", " ", text).strip()
        if not text:
            raise ValueError("No text found on page.")
        return text[: self._config.max_chars]


class FileDocumentSource(DocumentSource):
    """Read plain text from a local file."""

    def __init__(self, path):
        self._path = path
        self._config = AppConfig()

    def fetch_text(self):
        if not os.path.isfile(self._path):
            raise FileNotFoundError(f"File not found: {self._path}")
        with open(self._path, encoding="utf-8") as handle:
            text = handle.read().strip()
        if not text:
            raise ValueError("File is empty.")
        return text[: self._config.max_chars]
