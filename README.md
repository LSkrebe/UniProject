# Document Analyzer (OOP Coursework)

CLI app that analyzes business documents from a **URL** or **text file** using the OpenAI API. Results are saved to JSON and can be exported to CSV.

## Requirements covered

- 4 OOP pillars (see `REPORT.md`)
- Factory Method + Singleton design patterns
- Composition / aggregation
- JSON + CSV file read/write
- Unit tests (`unittest`)

## Setup

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env — set OPENAI_API_KEY
```

## Run

```bash
python app.py
```

Try `sample.txt` without internet, or any `https://` URL with a connection.

## Tests

```bash
python -m unittest discover -s tests -v
```

## Project layout

| File | Role |
|------|------|
| `app.py` | CLI menu |
| `application.py` | Main app (composition) |
| `sources.py` | URL / file sources (inheritance) |
| `factory.py` | Factory Method |
| `analyzers.py` | OpenAI analyzer |
| `storage.py` | JSON + CSV persistence |
| `config.py` | Singleton settings |
| `models.py` | `AnalysisResult` model |
| `REPORT.md` | Coursework report |
| `tests/` | Unit tests |

## Submit zip (no venv)

```bash
git archive -o ../Project-submit.zip HEAD
```

Do not include `venv/`, `__pycache__/`, or `.env` in submissions.
