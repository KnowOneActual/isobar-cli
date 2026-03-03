# Testing Procedure

This document outlines the procedures for executing and developing tests for Isobar CLI. The project utilizes [pytest](https://docs.pytest.org/) for test execution and [requests-mock](https://requests-mock.readthedocs.io/) for API simulation.

## 🛠 Setup

Prior to executing tests, install the project with the `test` extra:

```bash
pip install -e ".[test]"
```

This ensures `pytest`, `requests-mock`, and all other development dependencies are available.

## 🚀 Running Tests

### Standard Execution
Execute all tests from the project root:
```bash
pytest
```

### Coverage Analysis
To analyze code coverage (requires `pytest-cov`):
```bash
pytest --cov=isobar_cli
```

### Codecov Integration
Upon pushing code to GitHub or opening a Pull Request, the CI pipeline automatically executes the test suite and uploads the coverage report to [Codecov.io](https://codecov.io). A summary of coverage impacts is automatically provided on Pull Requests.

### Targeted Execution
Execute tests in a specific file:
```bash
pytest tests/test_api.py
```

## 🧪 Developing New Tests

All tests should be located in the `tests/` directory and adhere to the `test_*.py` naming convention.

### Cache Isolation
Tests utilize a temporary directory for caching, managed by a `pytest` fixture in `tests/test_api.py`. This ensures that local user caches remain unaffected and tests are reproducible.

### CLI Integration Testing
`typer.testing.CliRunner` is used in `tests/test_main.py` to verify the command-line interface. New flags or arguments should include corresponding test cases in this module.

### API Simulation
Isobar CLI interacts with external APIs (Open-Meteo, ip-api.com). **Network requests are prohibited during test execution.**

Utilize the `requests_mock` fixture to simulate API responses:

```python
def test_feature_implementation(requests_mock):
    # Simulate the Geocoding API response
    requests_mock.get(
        "https://geocoding-api.open-meteo.com/v1/search?name=London&count=1&format=json",
        json={"results": [{"name": "London", "latitude": 51.5, "longitude": -0.1}]}
    )
    
    # Execute and verify the function
    ...
```

### Key Testing Areas
1. **API Parsing**: Verify that weather fields from Open-Meteo are correctly processed in `isobar_cli/api.py`.
2. **UI Rendering**: Ensure temperature color mapping and condition icons are correctly handled in `isobar_cli/ui.py`.
3. **Location Resolution**: Verify auto-detection and fallback logic in `isobar_cli/location.py`.

## 🧹 Linting & Style Standards
The project employs [Ruff](https://docs.astral.sh/ruff/) for linting and formatting. Code must pass all style checks prior to pull request submission:

```bash
ruff check .
ruff format .
```
