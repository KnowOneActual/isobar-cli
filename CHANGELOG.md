# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.2] - 2026-03-30

### Fixed
- **CLI Structure Regression** — Restored hourly (`-H`) and weekly forecast (`-f`) functionality that was broken when adding the `home` command.
- **Typer Integration** — Fixed CLI structure to use `invoke_without_command=True` for default weather behavior while maintaining `home` as a subcommand.
- **Test Updates** — Updated tests to reflect new CLI structure and fix `WeatherData` constructor calls.

## [1.1.1] - 2026-03-30

### Fixed
- **PyPI Publishing** — Version bump to resolve conflict with existing 1.1.0 release on PyPI.
- **Test Structure** — Fixed test invocations for new CLI structure with `home` command.
- **Linting** — Removed unused imports to pass ruff checks.

## [1.1.0] - 2026-03-30

### Added
- **Phase 7: Intuition & Analysis** — Complete implementation of higher-level context and automated insights:
  - **Preparation Guidance** — Clothing and gear suggestions based on outdoor conditions (e.g., "🧥 Light jacket", "🧴 Sunscreen recommended").
  - **Temporal Context** — Comparative analysis with previous day conditions (e.g., "↑ 5°F warmer than yesterday").
  - **UV Index Monitoring** — Sun protection guidance with color-coded intensity levels (Low to Extreme).
  - **Wind Gust Alerts** — Specific highlighting of significant gust events (alerts when gusts >1.5x sustained wind and >20 mph).
  - **Home City Persistence** — Support for a configured "Home City" to bypass IP lookups (`isobar home "Your City"`).
- **Enhanced Weather Data** — Added UV index and wind gust data to API responses and caching.
- **Configuration System** — New `config.py` module with persistent settings in `~/.config/isobar/`.
- **Comprehensive Testing** — 7 new test functions covering all Phase 7 features with maintained high coverage.

### Changed
- **UI Enhancements** — Weather table now includes UV index and wind gust information.
- **Auto-Location Logic** — Checks for home city configuration before falling back to IP detection.
- **API Integration** — Expanded Open-Meteo API calls to include `wind_gusts_10m` and `uv_index` fields.

## [1.0.1] - 2026-03-03

### Added
- **Comprehensive Security Scanning** — Integrated Trivy, Bandit, Semgrep, and ShellCheck into a new GitHub Actions workflow, outputting to the GitHub Security tab.
- **Automated Dependency Updates** — Configured Dependabot for `pip` and `github-actions` ecosystems.
- **Release Drafter** — Added a workflow to automatically generate structured release notes based on PR labels (`feature`, `fix`, `chore`).
- **Codecov Integration** — Integrated Codecov into the CI pipeline to track test coverage visually on every PR.

### Fixed
- **Insecure Transport (HTTPS)** — Resolved a security finding by switching from `ip-api.com` (HTTP) to `ipwho.is` (HTTPS) for automated location detection.
- **Project Tone** — Standardized documentation and source code to use a professional, objective tone while preserving the project's intuitive personality.

## [1.0.0] - 2026-03-02

### Added
- **PyPI Release** — `isobar-cli` is now available on PyPI. Install via `pip install isobar-cli`.
- **Homebrew Tap** — Now available via a custom tap. Install with `brew install KnowOneActual/tap/isobar`.

### Changed
- **Simplified CLI Usage** — Removed the redundant `--city` flag. Multi-word cities are now handled with standard quotes (e.g., `"New York"`) instead of underscores.

## [0.6.3] - 2026-02-28

### Added
- **Major Test Coverage Boost** — Increased project test coverage from 77% to 98% by adding a comprehensive new test suite (`tests/test_isobar_extra.py`).
  - **API Edge Cases** — Added tests for cache invalidation, API failures, and hourly data index errors.
  - **Main Logic** — Verified multi-city support and all CLI flags (`--hourly`, `--forecast`, `--city`).
  - **UI Conditions** — New unit tests for Wind Chill, Heat Index, and various precipitation intensities (Moderate/Light rain and snow).

## [0.6.2] - 2026-02-28

### Added
- **PyPI Preparation** — Added rich metadata, classifiers, and project URLs to `pyproject.toml`.
- **Automated Publishing** — New GitHub Action to automatically publish to PyPI on version tags.

### Changed
- Updated `.gitignore` to prevent accidental log commits.
- Expanded the project roadmap to include Homebrew, AUR, and Windows package managers.

## [0.6.1] - 2026-02-28

### Added
- **Shell Completion** — Added support for tab-completing city names from search history. Run `isobar --install-completion` to enable.

## [0.6.0] - 2026-02-28

### Added
- **Air Quality Index (AQI)** — Integrated US AQI data with color-coded health classifications (Good, Moderate, Unhealthy, etc.).
- **Side-by-Side Multi-City View** — Multiple cities are now displayed in columns when requested together (without detailed forecast flags), significantly improving information density.
- **Smart City Suggestions** — Added "Did you mean?" suggestions using the geocoding API when a city name is misspelled or not found.
- **Extreme Temperature Labels** — The "Real Feel" label now dynamically changes to "Wind Chill" or "Heat Index" when conditions are extreme.

### Changed
- Refactored UI and API modules to clearly separate data processing from rendering.
- Cache metadata is now passed directly from the API layer to the UI.

## [0.5.2] - 2026-02-28

### Added
- **Multiple Cities Support** — Fetch and display weather for multiple cities in a single command (e.g., `isobar London Tokyo Paris`).
- **Visual Separators** — Clean dashed separators between city cards when viewing multiple locations.

### Changed
- The `city` argument is now `cities` (a list), allowing for one or more positional arguments.

## [0.5.1] - 2026-02-28

### Added
- **Hourly Outlook** — Pass `--hourly` or `-H` to see a compact 12-hour forecast including temperature, weather icons, and rain probability.
- **Improved Test Suite** — Updated mocks and tests to cover hourly data parsing and UI rendering.

### Fixed
- **CI Stability** — Resolved CI and coverage failures related to project layout and ANSI color escape codes in test output.
- **Test Isolation** — Aggressively disabled color output in CLI tests to ensure reliable help output matching across different environments.

### Changed
- **API Cache** — Hourly data is now cached alongside daily data. Older caches (v0.5.0) will automatically refresh when hourly data is requested.

## [0.5.0] - 2026-02-28

### Added
- **Metric Unit Support** — Pass `--metric` or `-m` to display weather in Celsius, km/h, and mm.
- **Unit-Aware Color Coding** — Temperature color-coding thresholds automatically adjust for Celsius (e.g., 0°C is cyan, 20°C is green).
- **Comprehensive Test Suite** — Expanded `pytest` coverage to 73%:
  - **`test_main.py`** — New CLI integration tests using `typer.testing.CliRunner`.
  - **Metric Tests** — Unit tests for metric unit API requests and UI rendering.
  - **Cache Isolation** — Added a `pytest` fixture to mock `CACHE_DIR`, preventing tests from being affected by or polluting the local user cache.

### Changed
- **API Results** — Added a `units` metadata dictionary to the weather data structure to track display units.
- **Cache Strategy** — Cache files now include a unit suffix (`_metric.json` or `_imperial.json`) to allow toggling between unit systems without waiting for the cache to expire.

### Fixed
- **Test Reliability** — Fixed a bug where `test_get_weather_data_success` would fail if a local cache file existed for Chicago.
- **UI Logic** — Standardized internal keys for rainfall and snowfall (`rainfall_inch` → `rainfall`) to support both unit systems.

## [0.4.4] - 2026-02-26

### Added
- **GitHub Actions CI** - Automated workflow (`.github/workflows/ci.yml`) runs on every push and pull request to `main` with three parallel jobs:
  - **Ruff Lint** — `ruff check .` enforces code style, catches unused variables, import order, and bugbear rules.
  - **Security Audit** — `pip-audit` scans all dependencies for known CVEs.
  - **Run Tests** — `pytest` runs the full test suite on every commit.
- **Initial Test Suite** — Comprehensive unit tests for `api.py`, `location.py`, and `ui.py` (formatting, icons, precip headlines) in the `tests/` directory.
- **Testing Procedure Document** — New `docs/TESTING.md` guide for running tests, mocking APIs, and checking coverage.
- **README Badges** — CI status, Coverage, Version, Ruff, Python 3.8+, and MIT license badges added.

### Changed
- **Src Layout Refactor** — Moved source files from `src/` to `src/isobar_cli/` and updated `pyproject.toml` to follow modern Python packaging standards.
- **Dependency Management** — Added `[project.optional-dependencies]` for testing (`pip install ".[test]"`), including `pytest-cov`.
- **Contribution Guide** — Updated `CONTRIBUTING.md` with instructions for running the test suite.

### Fixed
- **Repository Cleanup** — Removed legacy build artifacts (`build/`, `*.egg-info/`, `.ruff_cache/`) and unified the project structure.
- **Ruff Config** — Corrected `pyproject.toml` configuration to fix parsing errors and linting issues in tests.

## [0.4.3] - 2026-02-26

### Added
- **7-Day Forecast** - Pass `--forecast` or `-f` to display a full week outlook below the current conditions card. Each day shows the weekday, a WMO condition icon, plain-English description, color-coded high/low temps, and daily rain probability. Rain% is color-coded: cyan (≥60%), yellow (≥30%), dim (dry).
- **`--forecast` / `-f` flag** - New CLI option; composable with `--city` (e.g., `isobar --city Paris -f`).

### Changed
- API now fetches 7 days of daily data (`forecast_days=7`) including `temperature_2m_max`, `temperature_2m_min`, `weather_code`, and `precipitation_probability_max`.
- Stale city caches from before `0.4.3` will show `No forecast data available` until cleared (`rm ~/.cache/isobar/<city>.json`).

## [0.4.2] - 2026-02-26

### Added
- **Weather Condition Icons** - A new `Conditions` row appears at the top of the weather card showing a WMO weather code mapped to an emoji and plain-English description (e.g., `☀️ Clear sky`, `🌧️ Moderate rain`, `⛈️ Thunderstorm`). Covers all 23 standard WMO codes.

## [0.4.1] - 2026-02-26

### Added
- **Dynamic Timezone Detection** - Timezone is now resolved from city coordinates using `timezonefinder` (no API key required). Sunrise/sunset times are always accurate in the city's local time, not the host machine's timezone.
- **`--city` / `-c` flag** - City can now be passed as a named option (`isobar --city Tokyo`) in addition to the existing positional argument (`isobar Tokyo`). Both styles work interchangeably.

### Fixed
- Format sunrise/sunset using 12-hour time (e.g., `6:29 AM`, `5:37 PM`) instead of 24-hour `HH:MM`.
- Fix Ruff `F841` warnings by removing unused `sunrise_iso` / `sunset_iso` variables.

## [0.4.0] - 2026-02-24

### Added
- **Auto-Location Detection** - Run `isobar` without arguments to auto-detect location via IP
  - Uses ip-api.com (1,000 req/day free tier)
  - Browser-like User-Agent to avoid blocking
  - Graceful fallback to Chicago if detection fails
  - **Phase 1 of ROADMAP complete** ✅

### Fixed
- **requests DNS resolution** - Robust handling of DNS/SSL edge cases
- **Ruff linting** - Fixed W293, E501 line length violations

### Changed
- City argument now optional in CLI
- Updated help text/examples to show `isobar` (no args) usage

## [0.3.1] - 2026-02-22

### Added
- **Rain forecast**: 6-hour rainfall totals in inches (`rainfall_inch`) [PR #1]
- **Snow forecast**: 6-hour snowfall totals in inches (converted from cm) [PR #1]
- **Precipitation headline**: Instant comfort summary under Precip Chance row
  - "Dry conditions expected", "Light rain likely", "Snowy conditions likely", etc.
  - Helps answer "what should I wear?" at a glance [PR #1]

### Changed
- Snow display now uses inches consistently with rain (was cm) [PR #1]
- Precip headline moved under "Precip Chance" row for better flow [PR #1]

## [0.3.0] - 2026-02-22

### Added
- **Precipitation Probability** - Next 6h rain chance (%) [Phase 2]
- **Snow Detection** - Expected snowfall warning (>1mm)
- **Underscore Support** - `isobar New_York` → "New York" [no quotes!]
- **Smart Defaults** - `isobar` → Chicago weather

### Fixed
- Graceful "city not found" messaging with examples

## [0.2.0] - 2026-02-22

### Added
- **Local Caching** - 15-minute cache per-city in `~/.cache/isobar/` (~78% faster repeat requests) [#1]
- **Cache Timestamp** - Subtle "Updated X min ago" indicator on cache hits
- **Phase 1 Complete** - Core performance improvements from ROADMAP.md

### Fixed
- Cache filename consistency (handles city names with commas cleanly)

## [0.1.0] - 2026-02-21

### Added
- Core command-line interface to request weather by city name.
- Open-Meteo API integration for free geocoding and forecast data.
- Terminal UI built with Rich featuring a colored, borderless card layout.
- Display for Temperature, Real Feel, and Wind Speed.
- Basic error handling for failed API connections and unrecognized city names.

## [Unreleased]

## [1.0.2] - 2026-03-09

### Fixed
- **Hourly Forecast Start Time**: Resolved a bug where the hourly forecast would incorrectly reset to midnight (12 AM) if the current time from the API included minutes (e.g., 12:32 PM). The logic now correctly identifies the current hour or finds the next available slot.

### Changed
- **Ruthless Refactor**: Decomposed `api.py` into specialized clients (`GeocodingClient`, `WeatherClient`, `AirQualityClient`).
- **Logic Extraction**: Moved business logic (Real Feel, comfort thresholds, precipitation headlines) from `ui.py` to `isobar_cli/logic.py`.
- **Model Introduction**: Implemented `dataclasses` in `isobar_cli/models.py` for structured weather data and unit contracts.
- **AI Slop Removal**: Replaced manual 12-hour clock logic with standard library `strftime` and eliminated redundant "god" functions.
- **Improved Reliability**: Replaced silent failures in API calls with explicit error handling and logging.


### Added
- Initial project setup.
