"""Domain models with encapsulation."""


def _as_string_list(value):
    """Ensure risks/opportunities are lists, not split strings."""
    if not value:
        return []
    if isinstance(value, str):
        return [value.strip()] if value.strip() else []
    return [str(item).strip() for item in value if str(item).strip()]


class AnalysisResult:
    """Stores one document analysis (private fields, public accessors)."""

    def __init__(
        self,
        summary,
        risks,
        opportunities,
        sentiment,
        event_type,
        source="",
    ):
        self._summary = summary
        self._risks = _as_string_list(risks)
        self._opportunities = _as_string_list(opportunities)
        self._sentiment = sentiment
        self._event_type = event_type
        self._source = source

    @property
    def summary(self):
        return self._summary

    @property
    def risks(self):
        return list(self._risks)

    @property
    def opportunities(self):
        return list(self._opportunities)

    @property
    def sentiment(self):
        return self._sentiment

    @property
    def event_type(self):
        return self._event_type

    @property
    def source(self):
        return self._source

    def to_dict(self):
        return {
            "summary": self._summary,
            "risks": self._risks,
            "opportunities": self._opportunities,
            "sentiment": self._sentiment,
            "event_type": self._event_type,
            "source": self._source,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            summary=data.get("summary", ""),
            risks=_as_string_list(data.get("risks", [])),
            opportunities=_as_string_list(data.get("opportunities", [])),
            sentiment=data.get("sentiment", ""),
            event_type=data.get("event_type", ""),
            source=data.get("source", ""),
        )
