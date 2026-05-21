"""Domain models with encapsulation."""


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
        self._risks = list(risks)
        self._opportunities = list(opportunities)
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
            risks=data.get("risks", []),
            opportunities=data.get("opportunities", []),
            sentiment=data.get("sentiment", ""),
            event_type=data.get("event_type", ""),
            source=data.get("source", ""),
        )
