# ApiPlaygroundPy

ApiPlaygroundPy is a small, focused **Python playground for working with web APIs and basic data processing**.

It is designed as a clean, minimal template you can:

- Use to **try out APIs quickly** in a notebook or script
- Extend into a more complete **data-ingestion micro-project**
- Reuse as a **starter structure** for API-centric experiments

---

## Features

- Simple **API client wrapper** around `requests`
- Basic **data processing helpers** for JSON and tabular data
- Centralized, configurable **logging utility**
- Example **Jupyter notebook** to demonstrate usage
- Lightweight dependencies and **clear environment setup** docs

---

## Project Structure

```text
ApiPlaygroundPy/
├── README.md
├── requirements.txt
├── setup_environment.md
├── data_api_playground.ipynb
├── src/
│   ├── __init__.py
│   ├── api_playground.py
│   ├── data_processing.py
│   └── utils/
│       ├── __init__.py
│       └── logger.py
├── notebooks/
│   └── README.md
├── env_checklist/
│   ├── README.md
│   ├── terminal_commands.txt
│   └── tool_versions.txt
└── .gitignore
```

---

## Installation

1. **Clone** or copy this repository structure into a folder named `ApiPlaygroundPy`.
2. Create and activate a virtual environment (see `setup_environment.md` or `env_checklist/terminal_commands.txt`).
3. Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Quick Start

### 1. Using the API playground module

```python
from src.api_playground import ApiPlayground

# Initialize client with a base URL (can be any public API)
client = ApiPlayground(
    base_url="https://jsonplaceholder.typicode.com",
    default_timeout=10,
)

# Simple GET request
posts = client.get("/posts", params={"userId": 1})
print(len(posts))
```

### 2. Processing the data

```python
from src.data_processing import to_dataframe, select_columns, filter_rows

# Convert JSON list to DataFrame
import pandas as pd

posts_df = to_dataframe(posts)

# Select and filter
posts_small = select_columns(posts_df, ["id", "userId", "title"])
filtered = filter_rows(posts_small, lambda df: df["userId"] == 1)

print(filtered.head())
```

---

## Jupyter Notebook

The file **`data_api_playground.ipynb`** is an example notebook showing:

- How to import from `src/`
- How to call external APIs
- How to convert and explore data with `pandas`

Open it with:

```bash
jupyter notebook data_api_playground.ipynb
```

or using VS Code / another Jupyter-compatible editor.

---

## Configuration & Logging

- Logging behavior is configured in `src/utils/logger.py`.
- By default, the logger:
  - Logs to **stdout**
  - Uses a **simple, readable format**
  - Is namespaced under `api_playground`.

You can customize the logger by importing `get_logger` and adding handlers or changing levels.

```python
from src.utils.logger import get_logger

logger = get_logger(__name__)
logger.info("Hello from ApiPlaygroundPy!")
```

---

## Testing Ideas (not included by default)

This skeleton does not include a `tests/` folder or test runner configuration, but it is structured to make that easy to add later. Suggested additions:

- `tests/test_api_playground.py`
- Use `pytest` for test discovery and execution

Example `pytest` command:

```bash
pytest -q
```

---

## Extending This Template

Some ideas for extending `ApiPlaygroundPy`:

- Add **authentication** support (API keys, OAuth, etc.)
- Add **rate limiting** or retry logic to the client
- Add **caching** of responses (e.g., on disk or in memory)
- Add **CLI entry points** to trigger API calls from the command line
- Add a **configuration file** (YAML/TOML) for base URLs and secrets (never commit secrets)

---

## License

This template is provided as-is with no license specified by default. Add your own `LICENSE` file and update this section before publishing or sharing the project.
