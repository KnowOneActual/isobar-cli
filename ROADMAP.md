# Isobar CLI Roadmap

This roadmap describes **intentional, phased changes** to Isobar CLI.

The mission stays the same:

> Help you quickly understand what it feels like outside, from your terminal.

Everything here is optional until it proves it actually improves that mission.

---

## Phase 1: Speed & Flow ✅ COMPLETE

**Goal:** Make the existing experience faster and more convenient.

- [x] **Local Caching (15 minutes)** — Cache per city in `~/.cache/isobar/`. Avoids hammering the API; repeat calls feel instant.
- [x] **Auto-Location** — Run `isobar` with no arguments to detect city via IP. Fails gracefully with a clear message.
- [x] **Fuzzy City Suggestions** — "Did you mean?" suggestions for typos using geocoding metadata.
- [x] **Shell Completion** — Tab-complete city names from your search history (`isobar --install-completion`).

---

## Phase 2: Deeper Comfort Context ✅ COMPLETE

**Goal:** Add information that directly informs comfort decisions, without turning into a dashboard.

- [x] **Precipitation Probability** — Next 6h rain chance (%) with a plain-English comfort headline.
- [x] **Rain & Snow Totals** — Next 6h rainfall/snowfall in inches (or mm).
- [x] **Sunrise & Sunset Times** — Shown in the city's local timezone (not yours).
- [x] **Air Quality Index (AQI)** — Integrated US AQI data with color-coded health classifications (Good, Moderate, etc.).
- [x] **Celsius / Metric Units** — Full support for `--metric` / `-m` across all displays and caches.

---

## Phase 3: Visual Communication & Forecasting ✅ COMPLETE

**Goal:** Improve how information is communicated, not how much.

- [x] **Weather Condition Icons** — WMO weather code mapped to emoji + plain-English description.
- [x] **7-Day Forecast (`--forecast` / `-f`)** — Full week outlook with daily icons, color-coded highs/lows, and rain probability.
- [x] **Hourly Outlook (`--hourly` / `-H`)** — Next 12h temperature curve and rain probability.
- [x] **Side-by-Side Comparison** — Compare multiple cities in columns (e.g., `isobar London Tokyo Paris`).
- [x] **Simplified Positional CLI** — Removed redundant `--city` flags in favor of direct, intuitive arguments (`isobar "New York"`).

---

## Phase 4: Quality & Trust ✅ COMPLETE

**Goal:** Make the project safe to contribute to and easy to trust.

- [x] **GitHub Actions CI** — Automated `ruff check` (lint) + `pip-audit` (security scan) on every push.
- [x] **Comprehensive Security Scans** — Trivy (filesystem), Bandit/Semgrep (SAST), and ShellCheck integration via SARIF to the Security tab.
- [x] **Dependabot** — Automated PRs for keeping Python dependencies and GitHub Actions up to date.
- [x] **Release Drafter** — Automated generation of categorized release notes from PR labels.
- [x] **README Badges** — Live CI status, security scan, version, ruff, Python 3.8+, and MIT license badges.
- [x] **Keep a Changelog** — Every release documented with dated version entries.

---

## Phase 5: Tests & Reliability ✅ COMPLETE

**Goal:** Ensure correctness survives future changes.

- [x] **pytest test suite** — Unit tests for formatting, icons, and WMO mappings.
- [x] **API Response Mocking** — Test logic against fixture JSON without hitting live APIs.
- [x] **CI Test Job** — Automated `pytest` runs on every push alongside lint and security.
- [x] **Codecov Integration** — Automated test coverage reporting directly on Pull Requests, maintaining ~98% coverage.

---

## Phase 6: Distribution & Accessibility 🚀 IN PROGRESS

**Goal:** Make Isobar easy to install and run on any machine.

- [x] **PyPI Release** — `pip install isobar-cli`.
- [x] **Homebrew Formula** — `brew install KnowOneActual/tap/isobar`.
- [ ] **Standalone Binaries** — Generate executable binaries for macOS, Linux, and Windows (no Python required).
- [ ] **AUR Package** — Publish to the Arch User Repository.
- [ ] **Winget / Scoop** — Windows package manager support.

---

## Phase 7: Human Context & Intuition 💡 NEXT

**Goal:** Move beyond raw data to provide human-centered context.

- [ ] **Clothing Recommendations** — Simple "Preparation" line: *"Heavy jacket & gloves"* or *"T-shirt weather"*.
- [ ] **Yesterday Comparison** — *"It's 10°F colder than yesterday at this time"* for relative context.
- [ ] **UV Index & Sun Protection** — *"UV is High: Wear sunscreen if outside for >20 mins."*
- [ ] **Wind Gust Alert** — Specifically highlight if gusts significantly exceed average wind speed.
- [ ] **"Home City" Persistence** — `isobar --set-home "City"` to skip IP lookups and get instant local results.

---

## Future (Highly Skeptical)

Not planned. Noted here to say: *"Not unless there's a very strong reason."*

- [ ] **Multi-language support**
- [ ] **Customization surface** (colors, themes, layouts)
- [ ] **Animated icons**
- [ ] **Push notifications / alerts**

---

## How to Use This Roadmap

If you're proposing a change:
- Point to where it fits (Phase 1–7 or Future).
- Be explicit about what you'd **remove**, not just what you'd add.

> The roadmap is a **guardrail against scope creep**, not a promise that everything listed will ship.
