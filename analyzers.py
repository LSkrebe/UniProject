"""Text analyzers: abstraction + OpenAI implementation."""

import json

from openai import OpenAI

from config import AppConfig
from models import AnalysisResult


class TextAnalyzer:
    """Abstract analyzer interface."""

    def analyze(self, text, source=""):
        raise NotImplementedError


class OpenAITextAnalyzer(TextAnalyzer):
    """Calls OpenAI API and returns a structured AnalysisResult."""

    def __init__(self):
        self._config = AppConfig()

    def analyze(self, text, source=""):
        api_key = self._config.api_key
        if not api_key or api_key == "your_api_key_here":
            raise ValueError("Set OPENAI_API_KEY in .env")

        client = OpenAI(api_key=api_key)
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            response_format={"type": "json_object"},
            messages=[
                {
                    "role": "user",
                    "content": (
                        "Analyze this document for investors. Return JSON with "
                        "keys: summary (string), risks (array of strings), "
                        "opportunities (array of strings), sentiment (string), "
                        f"event_type (string). Each array must have 3-5 items.\n\n{text}"
                    ),
                }
            ],
        )
        data = json.loads(response.choices[0].message.content)
        return AnalysisResult(
            summary=data.get("summary", ""),
            risks=data.get("risks", []),
            opportunities=data.get("opportunities", []),
            sentiment=data.get("sentiment", ""),
            event_type=data.get("event_type", ""),
            source=source,
        )
