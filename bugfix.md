# Bug Fixes

## Resume Upload API

### 1. `llm_analysis` import error

**Error:**

```text
ModuleNotFoundError: No module named 'llm_analysis'
```

**Cause:** `API/Resum_API.py` imported the sibling module as a top-level module. This failed when the API was imported as `API.Resum_API`.

**Fix:** Added an import that supports both package execution and direct execution from the `API` directory:

```python
try:
	from .llm_analysis import analyze_resume
except ImportError:
	from llm_analysis import analyze_resume
```

### 2. Mistral API key startup error

**Error:**

```text
ValueError: Mistral API key not found
```

**Cause:** `API/llm_analysis.py` checked for the Mistral API key while the module was imported. The current analyzer returns placeholder data and does not use the key yet.

**Fix:** Removed the unused import-time API key check so the FastAPI application can start without a Mistral key. The key should be validated when real Mistral analysis is enabled.

### 3. Upload format mismatch

**Problem:** The API allowed `.pdf`, `.docx`, `.doc`, `.txt`, and `.rtf`, but `mainCode/docs_loader.py` only implemented loaders for PDF, TXT, and CSV files.

**Fix:** Updated the API allowlist to match the implemented loaders:

```text
.pdf, .txt, .csv
```

Unsupported formats now return HTTP `400` with a clear error message instead of reaching document processing.

## Validation

The modified Python files were checked with:

```bash
env/bin/python -m py_compile API/Resum_API.py API/llm_analysis.py mainCode/docs_loader.py
```

A DOCX upload was also tested and returned the expected response:

```text
400
File type not allowed. Allowed: .txt, .pdf, .csv
```
