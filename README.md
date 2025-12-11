# StudyStats

StudyStats is a small command‑line tool that helps you track and summarize your study sessions.

It focuses on **simple numeric inputs** (minutes, pages, focus rating) and produces quick statistics like
pages per hour, effective study time (after breaks), and aggregate metrics across multiple sessions.

## Features

- Analyze a **single study session**
- Analyze **multiple sessions** and see aggregate statistics
- Compute:
  - Effective study time (subtracting breaks)
  - Pages per hour
  - Simple adjusted focus score
  - Mean and median session duration

## Installation

1. Ensure you have **Python 3.9+** installed.
2. Clone or download this project.
3. (Optional but recommended) create and activate a virtual environment.
4. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

There are no heavy external dependencies; only the standard library is required for core functionality.

## Usage

Run the main entry point from the project directory:

```bash
python main.py
```

You will be prompted to either:

- Analyze a single study session, or
- Analyze multiple sessions.

Follow the on‑screen prompts; validation will guide you if an input is invalid.

## Project Structure

- `main.py` – CLI entry point and user interaction flow
- `calculator.py` – pure calculation utilities (time, pages/hour, statistics)
- `report.py` – utilities for building formatted reports (currently used for programmatic summaries)
- `input_helpers.py` – reusable helpers for safe and user‑friendly console input

## Extending StudyStats

Some ideas for extensions:

- Persist sessions to a local file (CSV or JSON)
- Add subjects or tags to sessions
- Export nicely formatted reports using `ReportGenerator`
- Build a simple GUI or web interface reusing the same calculator and report logic

## License

This project is provided as‑is for learning and personal use.
