# Environment Setup for ApiPlaygroundPy

This guide walks you through creating an isolated Python environment and installing the dependencies for **ApiPlaygroundPy**.

---

## 1. Prerequisites

- **Python**: 3.9 or newer is recommended.
- **pip**: Ensure it is up to date:

```bash
python -m pip install --upgrade pip
```

Optional but recommended tools:

- **virtualenv** or the built-in `venv` module
- **git** for version control

---

## 2. Create a Virtual Environment

From the project root (`ApiPlaygroundPy/`), run one of the following options.

### Using `python -m venv` (built-in)

```bash
python -m venv .venv
```

Activate it:

- On **Windows (PowerShell)**:

  ```bash
  .venv\Scripts\Activate.ps1
  ```

- On **Windows (cmd.exe)**:

  ```bash
  .venv\Scripts\activate.bat
  ```

- On **macOS / Linux**:

  ```bash
  source .venv/bin/activate
  ```

When activated, your shell prompt will typically be prefixed with `(.venv)`.

---

## 3. Install Project Dependencies

With the virtual environment active:

```bash
pip install -r requirements.txt
```

This installs all libraries needed by the modules in `src/` and the example notebook.

---

## 4. Verify the Setup

From the project root, open a Python REPL:

```bash
python
```

Then run:

```python
from src.api_playground import ApiPlayground
from src.data_processing import to_dataframe
from src.utils.logger import get_logger

logger = get_logger(__name__)
logger.info("Environment is set up correctly.")

client = ApiPlayground("https://jsonplaceholder.typicode.com")
posts = client.get("/posts")
print(f"Fetched {len(posts)} posts")
```

If this runs without errors and prints a message, your environment is ready.

---

## 5. Jupyter Notebook Setup

With the virtual environment activated:

```bash
python -m ipykernel install --user --name api-playground-py --display-name "Python (ApiPlaygroundPy)"
```

Then you can start Jupyter:

```bash
jupyter notebook
```

Open `data_api_playground.ipynb` and choose the **"Python (ApiPlaygroundPy)"** kernel.

---

## 6. Deactivating the Environment

When you are done working:

```bash
deactivate
```

You can later re-activate it using the same commands shown in section 2.
