import unittest

from models import AnalysisResult


class TestAnalysisResult(unittest.TestCase):
    def test_to_dict_and_from_dict(self):
        original = AnalysisResult(
            summary="Test summary",
            risks=["risk1"],
            opportunities=["opp1"],
            sentiment="Neutral",
            event_type="Report",
            source="http://example.com",
        )
        restored = AnalysisResult.from_dict(original.to_dict())
        self.assertEqual(restored.summary, "Test summary")
        self.assertEqual(restored.risks, ["risk1"])
        self.assertEqual(restored.source, "http://example.com")

    def test_encapsulation_returns_copy(self):
        result = AnalysisResult("s", ["r"], ["o"], "Bullish", "Earnings")
        risks = result.risks
        risks.append("extra")
        self.assertEqual(result.risks, ["r"])
