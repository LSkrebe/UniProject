"""JSON file import/export for analysis history."""

import json
import os

from models import AnalysisResult


class AnalysisStorage:
    """Reads and writes analysis results to a JSON file."""

    def __init__(self, file_path):
        self._file_path = file_path

    def _ensure_folder(self):
        folder = os.path.dirname(self._file_path)
        if folder:
            os.makedirs(folder, exist_ok=True)

    def load_all(self):
        if not os.path.isfile(self._file_path):
            return []
        with open(self._file_path, encoding="utf-8") as handle:
            raw = json.load(handle)
        return [AnalysisResult.from_dict(item) for item in raw]

    def save_all(self, results):
        self._ensure_folder()
        data = [result.to_dict() for result in results]
        with open(self._file_path, "w", encoding="utf-8") as handle:
            json.dump(data, handle, indent=2)

    def append(self, result):
        history = self.load_all()
        history.append(result)
        self.save_all(history)

    def export_csv(self, csv_path):
        """Export history to CSV for sharing or spreadsheets."""
        results = self.load_all()
        lines = [
            "source,event_type,sentiment,summary,risks,opportunities",
        ]
        for item in results:
            risks = "; ".join(item.risks)
            opportunities = "; ".join(item.opportunities)
            summary = item.summary.replace('"', '""')
            lines.append(
                f'"{item.source}","{item.event_type}","{item.sentiment}",'
                f'"{summary}","{risks}","{opportunities}"'
            )
        folder = os.path.dirname(csv_path)
        if folder:
            os.makedirs(folder, exist_ok=True)
        with open(csv_path, "w", encoding="utf-8") as handle:
            handle.write("\n".join(lines))
