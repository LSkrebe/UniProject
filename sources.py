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

    def _request_headers(self):
        user_agent = self._config.user_agent
        if "sec.gov" in self._url.lower():
            if not user_agent or "@" not in user_agent:
                raise ValueError(
                    "SEC.gov blocks requests without contact info. "
                    "Add to .env: HTTP_USER_AGENT=Your Name UniProject/1.0 "
                    "(your.email@university.edu)"
                )
        elif not user_agent:
            user_agent = "DocumentAnalyzer/1.0"
        return {
            "User-Agent": user_agent,
            "Accept-Encoding": "gzip, deflate",
        }

    def fetch_text(self):
        response = requests.get(
            self._url, headers=self._request_headers(), timeout=30
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
