# Isobar CLI Roadmap

This roadmap describes the **intentional, phased development** of Isobar CLI.

## Mission Statement

> Help people quickly understand what it feels like outside, right from the terminal.

Features are evaluated based on their ability to improve the clarity and speed of weather-related preparation decisions.

---

## Phase 1: Performance & Flow ✅ COMPLETE

**Goal:** Enhance core usability and convenience.

- [x] **Local Caching (15 minutes)** — Persistent cache per city in `~/.cache/isobar/` to reduce API latency.
- [x] **Auto-Location** — Automated city detection via IP.
- [x] **Fuzzy City Suggestions** — Correction suggestions for misspelled city names.
- [x] **Shell Completion** — Tab-completion for city names from search history.

---

## Phase 2: Contextual Comfort ✅ COMPLETE

**Goal:** Integrate metrics that directly inform preparation decisions.

- [x] **Precipitation Probability** — 6-hour precipitation forecasts with plain-English summaries.
- [x] **Precipitation Totals** — Expected rainfall and snowfall amounts.
- [x] **Solar Events** — Sunrise and sunset times in the local city timezone.
- [x] **Air Quality Index (AQI)** — US AQI data with color-coded health classifications.
- [x] **Metric Support** — Comprehensive support for Celsius and metric units.

---

## Phase 3: Visualization & Forecasting ✅ COMPLETE

**Goal:** Optimize information density and communication.

- [x] **Condition Icons** — WMO condition mappings to visual emoji and descriptions.
- [x] **7-Day Forecast** — Week-at-a-glance outlook with highs, lows, and precipitation trends.
- [x] **Hourly Outlook** — Short-term temperature and precipitation trends.
- [x] **Multi-City Comparison** — Side-by-side weather comparisons in a single view.
- [x] **CLI Refinement** — Streamlined positional arguments for intuitive usage.

---

## Phase 4: Quality & Trust ✅ COMPLETE

**Goal:** Ensure security, reliability, and maintainability.

- [x] **GitHub Actions CI** — Automated linting and security scanning on all pushes.
- [x] **Comprehensive Security Scans** — Integration of Trivy, Bandit, Semgrep, and ShellCheck.
- [x] **Dependabot** — Automated dependency management for security and stability.
- [x] **Release Drafter** — Categorized release notes automated from PR metadata.
- [x] **Status Badges** — Real-time monitoring of project health in the repository.
- [x] **Changelog Maintenance** — Detailed documentation of every release and notable change.

---

## Phase 5: Testing & Reliability ✅ COMPLETE

**Goal:** Verify functional correctness and prevent regressions.

- [x] **pytest Suite** — Unit tests for core formatting and logic modules.
- [x] **API Mocking** — Offline test execution using simulated API responses.
- [x] **Automated Verification** — CI-integrated test runs on every pull request.
- [x] **Code Coverage Tracking** — Integrated reporting to maintain high test coverage standards.

---

## Phase 6: Distribution ✅ IN PROGRESS

**Goal:** Improve accessibility across different platforms and environments.

- [x] **PyPI Release** — Official package distribution via `pip`.
- [x] **Homebrew Formula** — Native installation support for macOS and Linux via `brew`.
- [ ] **Standalone Binaries** — Executable builds for macOS, Linux, and Windows to eliminate local Python dependencies.
- [ ] **AUR Package** — Distribution via the Arch User Repository.
- [ ] **Windows Package Managers** — Support for Winget and Scoop.

---

## Phase 7: Intuition & Analysis ✅ COMPLETE

**Goal:** Provide higher-level context and automated insights.

- [x] **Preparation Guidance** — Clothing and gear suggestions based on outdoor conditions.
- [x] **Temporal Context** — Comparative analysis with previous day conditions.
- [x] **UV Index Monitoring** — Sun protection guidance based on UV intensity.
- [x] **Wind Gust Alerts** — Specific highlighting of significant gust events.
- [x] **Persistence** — Support for a "Home City" to bypass IP lookups.

---

## Phase 8: Security & Configuration ✅ COMPLETE (v1.2.0)

**Goal:** Enhance security, reliability, and configurability for advanced use cases.

- [x] **Configurable API Endpoints** — Environment variable support for custom weather providers.
- [x] **Enhanced Error Handling** — Specific exception catching with timeout protection.
- [x] **Timezone Support** — Optional `pytz` dependency for accurate local time display.
- [x] **Improved Logging** — Debug information to stderr while maintaining clean UI.
- [x] **Security Hardening** — Replace hardcoded endpoints with configurable alternatives.

---

## Phase 9: Industrial Aesthetic ✅ COMPLETE (v1.3.0)

**Goal:** Transform the terminal interface into a distinctive, memorable experience with production-grade frontend design principles.

- [x] **Industrial Color Palette** — Concrete gray, steel blue, warning yellow, bright cyan accents
- [x] **Visual Gauges** — Temperature and humidity gauge visualizations using █ and ░ characters
- [x] **Severity Indicators** — Weather condition severity icons (⚡, ▲, ●, ○, ◇)
- [x] **Wind Categories** — Descriptive wind speed classifications (CALM, LIGHT, GENTLE, etc.)
- [x] **Industrial Styling** — Heavy borders, uppercase labels, METRIC/READING/STATUS columns
- [x] **Enhanced Preparation Guidance** — Priority-based suggestions with HIGH PRIORITY/RECOMMENDED/ADVISORY sections
- [x] **Forecast Panel Redesign** — 7-day forecast with industrial panel styling
- [x] **Hourly Tracker Enhancement** — Next 12 hours with temperature gauges and condition severity

---

## Future Considerations

Proposed features are evaluated against the core project philosophy. Complexity is added only when it provides significant value for situational awareness.

---

## Contribution Guidelines

New feature proposals should specify:
- The target roadmap phase.
- The specific value provided for situational weather awareness.

> The roadmap is a **guardrail against scope creep**, not a promise that everything listed will ship. It keeps the project sharp and focused on its core purpose.
