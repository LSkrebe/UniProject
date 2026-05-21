import os
import tempfile
import unittest
from unittest.mock import MagicMock, patch

from application import DocumentAnalyzerApp
from models import AnalysisResult
from storage import AnalysisStorage


class FakeAnalyzer:
    def analyze(self, text, source=""):
        return AnalysisResult(
            summary="Done",
            risks=["risk"],
            opportunities=["opp"],
            sentiment="Neutral",
            event_type="Report",
            source=source,
        )


class TestDocumentAnalyzerApp(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.json_path = os.path.join(self.temp_dir, "history.json")

    @patch("application.DocumentSourceFactory")
    def test_analyze_input_saves_history(self, mock_factory):
        mock_source = MagicMock()
        mock_source.fetch_text.return_value = "Sample text"
        mock_factory.create.return_value = mock_source

        app = DocumentAnalyzerApp(
            analyzer=FakeAnalyzer(),
            storage=AnalysisStorage(self.json_path),
        )
        result = app.analyze_input("sample.txt")

        self.assertEqual(result.summary, "Done")
        history = app.get_history()
        self.assertEqual(len(history), 1)
