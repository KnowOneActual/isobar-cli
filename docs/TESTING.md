# Testing Procedure

This document outlines how to run and write tests for Isobar CLI. We use [pytest](https://docs.pytest.org/) for testing and [requests-mock](https://requests-mock.readthedocs.io/) to simulate API responses.

## 🛠 Setup

Before running tests, install the project with the `test` extra:

```bash
pip install -e ".[test]"
```

This installs `pytest`, `requests-mock`, and all other necessary development dependencies.

## 🚀 Running Tests

### Standard Run
Run all tests from the project root:
```bash
pytest
```

### With Coverage
To see which parts of the code are covered (requires `pytest-cov`):
```bash
pytest --cov=isobar_cli
```

### Specific Files
Run tests in a single file:
```bash
pytest tests/test_api.py
```

## 🧪 Writing New Tests

All tests should be placed in the `tests/` directory and follow the `test_*.py` naming convention.

### Mocking API Calls
Isobar CLI depends on external APIs (Open-Meteo, ip-api.com). **Never make real network requests in tests.**

Use the `requests_mock` fixture to intercept calls:

```python
def test_my_feature(requests_mock):
    # Intercept the Geocoding API
    requests_mock.get(
        "https://geocoding-api.open-meteo.com/v1/search?name=London&count=1&format=json",
        json={"results": [{"name": "London", "latitude": 51.5, "longitude": -0.1}]}
    )
    
    # Now call your function
    ...
```

### Key Areas to Test
1. **API parsing**: Ensure new weather fields from Open-Meteo are handled correctly in `isobar_cli/api.py`.
2. **UI formatting**: Verify that temperature colors and condition icons map correctly in `isobar_cli/ui.py`.
3. **Location logic**: Test auto-detection fallbacks in `isobar_cli/location.py`.

## 🧹 Linting & Style
We use [Ruff](https://docs.astral.sh/ruff/) for linting and formatting. Ensure your code passes linting before submitting a PR:

```bash
ruff check .
ruff format .
```
