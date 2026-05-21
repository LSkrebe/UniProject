"""Main application class (composition of analyzer + storage)."""

from analyzers import OpenAITextAnalyzer
from config import AppConfig
from factory import DocumentSourceFactory
from models import AnalysisResult
from storage import AnalysisStorage


class DocumentAnalyzerApp:
    """
    Composes a TextAnalyzer and AnalysisStorage.
    Uses Factory Method to build document sources.
    """

    def __init__(self, analyzer=None, storage=None):
        config = AppConfig()
        config.load()
        self._analyzer = analyzer or OpenAITextAnalyzer()
        self._storage = storage or AnalysisStorage(config.history_path)

    def analyze_input(self, user_input):
        source = DocumentSourceFactory.create(user_input)
        text = source.fetch_text()
        result = self._analyzer.analyze(text, source=user_input.strip())
        self._storage.append(result)
        return result

    def get_history(self):
        return self._storage.load_all()

    def export_history_csv(self, path="data/analysis_history.csv"):
        self._storage.export_csv(path)
        return path

    @staticmethod
    def format_result(result: AnalysisResult):
        lines = [
            "",
            "=" * 40,
            "DOCUMENT ANALYSIS",
            "=" * 40,
            f"\nSource:\n{result.source}",
            f"\nEvent Type:\n{result.event_type}",
            f"\nSentiment:\n{result.sentiment}",
            f"\nSummary:\n{result.summary}",
            "\nOpportunities:",
        ]
        for item in result.opportunities:
            lines.append(f"- {item}")
        lines.append("\nRisks:")
        for item in result.risks:
            lines.append(f"- {item}")
        lines.append("")
        return "\n".join(lines)
