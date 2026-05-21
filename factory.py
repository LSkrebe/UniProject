"""Factory Method: create the right document source from user input."""

from sources import FileDocumentSource, UrlDocumentSource


class DocumentSourceFactory:
    """Builds UrlDocumentSource or FileDocumentSource from a string."""

    @staticmethod
    def create(user_input):
        value = user_input.strip()
        if value.lower().startswith(("http://", "https://")):
            return UrlDocumentSource(value)
        return FileDocumentSource(value)
