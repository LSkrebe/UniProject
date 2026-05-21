import unittest

from factory import DocumentSourceFactory
from sources import FileDocumentSource, UrlDocumentSource


class TestDocumentSourceFactory(unittest.TestCase):
    def test_create_url_source(self):
        source = DocumentSourceFactory.create("https://example.com/page")
        self.assertIsInstance(source, UrlDocumentSource)

    def test_create_file_source(self):
        source = DocumentSourceFactory.create("sample.txt")
        self.assertIsInstance(source, FileDocumentSource)
