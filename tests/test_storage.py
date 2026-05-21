import os
import tempfile
import unittest

from models import AnalysisResult
from storage import AnalysisStorage


class TestAnalysisStorage(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.json_path = os.path.join(self.temp_dir, "history.json")
        self.csv_path = os.path.join(self.temp_dir, "history.csv")
        self.storage = AnalysisStorage(self.json_path)

    def test_append_and_load(self):
        result = AnalysisResult(
            "Summary", ["r1"], ["o1"], "Neutral", "Report", "file.txt"
        )
        self.storage.append(result)
        loaded = self.storage.load_all()
        self.assertEqual(len(loaded), 1)
        self.assertEqual(loaded[0].summary, "Summary")

    def test_export_csv(self):
        result = AnalysisResult(
            "Summary", ["risk"], ["opp"], "Bullish", "Earnings", "a.txt"
        )
        self.storage.append(result)
        self.storage.export_csv(self.csv_path)
        with open(self.csv_path, encoding="utf-8") as handle:
            content = handle.read()
        self.assertIn("Summary", content)
        self.assertIn("Bullish", content)
