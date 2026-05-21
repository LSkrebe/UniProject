# Coursework Report: Document Analyzer

## 1. Introduction

### Topic and goal

This coursework implements an **App Integration** application: a **Document Analyzer** that reads business documents from a **URL** or a **local text file**, sends the text to the **OpenAI API**, and returns a structured investor-focused analysis (summary, risks, opportunities, sentiment, event type).

The goal is to practice Object-Oriented Programming (OOP), design patterns, file persistence, unit testing, and external API integration in Python.

### What is the application?

The program is a command-line tool for students and analysts who want a quick structured view of a web article or text document without manual reading of long pages.

### How to run the program

```bash
cd Project
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Add your OpenAI API key to .env
python app.py
```

Run unit tests:

```bash
python -m unittest discover -s tests -v
```

### How to use the program

1. Choose **1** and enter a URL (`https://...`) or a file path (e.g. `sample.txt`).
2. Wait for analysis; results print in the terminal and save to `data/analysis_history.json`.
3. Choose **2** to view all saved analyses (loaded from file).
4. Choose **3** to export history to `data/analysis_history.csv`.
5. Choose **4** to exit.

---

## 2. Body / Analysis

### Functional requirements

| Requirement | Implementation |
|-------------|----------------|
| Read document | `UrlDocumentSource` (HTTP) or `FileDocumentSource` (TXT) |
| Analyze text | `OpenAITextAnalyzer` calls OpenAI API |
| Save results | `AnalysisStorage.append()` writes JSON |
| Load history | `AnalysisStorage.load_all()` reads JSON |
| Export data | `AnalysisStorage.export_csv()` writes CSV |

### Four OOP pillars

#### Encapsulation

Data is hidden inside classes and accessed through controlled interfaces.

`AnalysisResult` stores fields privately and exposes read-only properties:

```python
class AnalysisResult:
    def __init__(self, summary, risks, ...):
        self._summary = summary
        self._risks = list(risks)
```

`AppConfig` hides loading state in `_loaded` and exposes only `api_key` and paths via properties.

#### Abstraction

Abstract ideas are defined without implementation details:

- `DocumentSource` — any source must implement `fetch_text()`
- `TextAnalyzer` — any analyzer must implement `analyze()`

The main program depends on these interfaces, not on HTTP or OpenAI internals.

#### Inheritance

Concrete classes extend abstract bases:

- `UrlDocumentSource` and `FileDocumentSource` inherit from `DocumentSource`
- `OpenAITextAnalyzer` inherits from `TextAnalyzer`

Shared contracts live in the parent; each child provides its own behavior.

#### Polymorphism

The same method call works on different object types:

```python
source = DocumentSourceFactory.create(user_input)
text = source.fetch_text()  # URL or file — same call, different class
```

`DocumentAnalyzerApp` uses any `TextAnalyzer` implementation passed in (used in unit tests with `FakeAnalyzer`).

### Design patterns

#### Factory Method (`DocumentSourceFactory`)

When the user enters a URL or a file path, the program must create the correct source class. The **Factory Method** centralizes that decision:

```python
class DocumentSourceFactory:
    @staticmethod
    def create(user_input):
        if value.startswith(("http://", "https://")):
            return UrlDocumentSource(value)
        return FileDocumentSource(value)
```

**Why Factory Method?** We need different source types with different `fetch_text()` behavior. Factory Method is more flexible than hard-coding `if/else` in `app.py`. **Singleton** was not used here because we need many source instances, not one shared object.

#### Singleton (`AppConfig`)

API key and paths should be read once from the environment. **Singleton** ensures one shared `AppConfig` instance:

```python
class AppConfig:
    _instance = None
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        ...
```

**Why Singleton?** One central point for configuration avoids reloading `.env` in every module.

### Composition and aggregation

**Composition:** `DocumentAnalyzerApp` *has* a `TextAnalyzer` and `AnalysisStorage`. The app does not inherit their behavior; it *uses* them (`self._analyzer`, `self._storage`). The analyzer cannot exist meaningfully without the app workflow in this design.

**Aggregation:** `AnalysisStorage` holds a *collection* of `AnalysisResult` objects loaded from JSON. Results can be serialized and exist independently in a file; the storage object groups them but does not own their lifecycle exclusively.

### File read and write

| File | Format | Purpose |
|------|--------|---------|
| `data/analysis_history.json` | JSON | Save and load analysis history |
| `data/analysis_history.csv` | CSV | Export history for reports |
| User input path | TXT | Import document text via `FileDocumentSource` |

`AnalysisStorage.save_all()` and `load_all()` implement JSON persistence. `export_csv()` exports the same data for spreadsheets.

### Unit testing

Tests use the `unittest` framework in the `tests/` package:

- `test_models.py` — `AnalysisResult` serialization and encapsulation
- `test_factory.py` — Factory creates correct source type
- `test_sources.py` — file read and mocked URL fetch
- `test_storage.py` — JSON append and CSV export
- `test_application.py` — app workflow with fake analyzer
- `test_config.py` — Singleton behavior

Mocks (`unittest.mock`) avoid real HTTP and API calls during tests.

### Code style

The project follows **PEP 8**: clear names, small modules, one responsibility per file, and docstrings on main classes.

---

## 3. Results and Summary

### Results

- The application successfully integrates the **OpenAI API** and supports both **web URLs** and **local text files**.
- **OOP structure** keeps the code maintainable: new sources or analyzers can be added without rewriting the CLI.
- **JSON/CSV persistence** lets users review past analyses and submit exported data.
- **Unit tests** pass without requiring a live API key in CI or grading environments.
- The main challenge was balancing coursework requirements (OOP, patterns, files, tests) with a clear, usable CLI.

### Conclusions

This coursework produced a working **Document Analyzer** that meets the functional and technical requirements: four OOP pillars, Factory Method and Singleton patterns, composition/aggregation, file I/O, and automated tests.

The program demonstrates how external APIs fit into a structured Python application rather than a single script.

**Future extensions:** add a GUI (Tkinter or web), support PDF input, multiple API providers behind `TextAnalyzer`, user accounts, and encrypted storage for sensitive reports.

---

## 4. Resources

- [OpenAI API documentation](https://platform.openai.com/docs)
- [Python unittest](https://docs.python.org/3/library/unittest.html)
- [PEP 8](https://peps.python.org/pep-0008/)
- [Markdown Guide](https://www.markdownguide.org/)
- Course materials: Git, design patterns, OOP pillars (Moodle / `rules.txt`)
