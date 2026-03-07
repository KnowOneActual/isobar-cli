# Refactor Plan: Ruthless Isobar Cleanup

## Phase 1: Foundation (Models & Units)
*   Create `isobar_cli/models.py`.
*   Define `WeatherUnits`, `ForecastDay`, `HourlyForecast`, and `WeatherData` (Pydantic).
*   Add a `UnitSystem` enum (METRIC, IMPERIAL).
*   Add unit conversion helper methods directly to the models.

## Phase 2: API & Logic Separation
*   Split `api.get_weather_data` into:
    *   `api.GeocodingClient`
    *   `api.WeatherClient`
    *   `api.AirQualityClient`
*   Move comfort logic (Real Feel thresholds, precip headlines) from `ui.py` to `isobar_cli/logic.py`.
*   Move threshold definitions to constants.

## Phase 3: AI Slop & Defensive Bloat Removal
*   Replace `api.format_time` with standard `strftime`.
*   Replace `try...except Exception: pass` with explicit error handling and logging.
*   Remove redundant comments.

## Phase 4: Integration & UI Update
*   Refactor `ui.py` to accept `WeatherData` objects instead of raw dicts.
*   Simplify `ui.py` by removing all logic checks.
*   Update `main.py` to use the new service objects and models.

## Phase 5: Verification & Cleanup
*   Run `pytest tests/`.
*   Add specific tests for new model logic.
*   Update `CHANGELOG.md` with the refactor details.
