import os
import tempfile
import unittest
from unittest.mock import MagicMock, patch

from sources import FileDocumentSource, UrlDocumentSource


class TestFileDocumentSource(unittest.TestCase):
    def test_reads_text_file(self):
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".txt", delete=False, encoding="utf-8"
        ) as handle:
            handle.write("Hello from file.")
            path = handle.name

        try:
            source = FileDocumentSource(path)
            text = source.fetch_text()
            self.assertEqual(text, "Hello from file.")
        finally:
            os.remove(path)

    def test_missing_file_raises(self):
        source = FileDocumentSource("missing-file-xyz.txt")
        with self.assertRaises(FileNotFoundError):
            source.fetch_text()


class TestUrlDocumentSource(unittest.TestCase):
    def test_sec_url_requires_user_agent(self):
        source = UrlDocumentSource(
            "https://www.sec.gov/Archives/edgar/data/320193/aapl.htm"
        )
        source._config = MagicMock()
        source._config.user_agent = ""
        source._config.max_chars = 12000
        with self.assertRaises(ValueError) as ctx:
            source.fetch_text()
        self.assertIn("HTTP_USER_AGENT", str(ctx.exception))

    @patch("sources.requests.get")
    def test_fetch_strips_html(self, mock_get):
        mock_response = MagicMock()
        mock_response.text = "<html><body><p>Hello web</p></body></html>"
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response

        source = UrlDocumentSource("https://example.com")
        text = source.fetch_text()
        self.assertIn("Hello web", text)
        self.assertNotIn("<p>", text)
