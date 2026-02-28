# Isobar CLI Roadmap

This roadmap describes **intentional, phased changes** to Isobar CLI.

The mission stays the same:

> Help you quickly understand what it feels like outside, from your terminal.

Everything here is optional until it proves it actually improves that mission.

---

## Phase 1: Speed & Flow ✅ COMPLETE

**Goal:** Make the existing experience faster and more convenient, without changing what Isobar is.

- [x] **Local Caching (15 minutes)** — Cache per city in `~/.cache/isobar/`. Avoids hammering the API; repeat calls feel instant.
- [x] **Auto-Location** — Run `isobar` with no arguments to detect city via IP. Fails gracefully with a clear message; no config files required.

---

## Phase 2: Deeper Comfort Context ✅ COMPLETE

**Goal:** Add information that directly informs comfort decisions, without turning into a dashboard.

- [x] **Precipitation Probability** — Next 6h rain chance (%) with a plain-English comfort headline ("Dry conditions expected", "Heavy rain likely", etc.).
- [x] **Rain & Snow Totals** — Next 6h rainfall/snowfall in inches.
- [x] **Sunrise & Sunset Times** — Shown in the city's local timezone (not the host machine's). Uses `timezonefinder` offline — no API key needed.

---

## Phase 3: Visual Communication & Forecasting ✅ COMPLETE

**Goal:** Improve how information is communicated, not how much.

- [x] **Weather Condition Icons** — WMO weather code mapped to emoji + plain-English description (e.g., `☀️ Clear sky`, `🌨️ Moderate snow`, `⛈️ Thunderstorm`). Covers all 23 standard WMO codes. Appears at the top of the card.
- [x] **7-Day Forecast (`--forecast` / `-f`)** — Full week outlook with per-day condition icon, high/low temps (color-coded), and rain %. Default command stays focused on "right now".
- [x] **`--city` / `-c` flag** — City can be passed as a named option or positional argument interchangeably.
- [x] **Dynamic Timezone Detection** — Timezone resolved from coordinates; sunrise/sunset always accurate for the queried city.

---

## Phase 4: Quality & Trust ✅ COMPLETE

**Goal:** Make the project safe to contribute to and easy to trust.

- [x] **GitHub Actions CI** — Automated `ruff check` (lint) + `pip-audit` (security scan) on every push and pull request to `main`.
- [x] **README Badges** — Live CI status, version, ruff, Python 3.8+, and MIT license badges.
- [x] **Ruff Linting** — Full rule set enforced (pycodestyle, pyflakes, isort, bugbear, comprehensions, pyupgrade).
- [x] **Keep a Changelog** — Every release documented with dated version entries.

---

## Phase 5: Tests & Reliability ✅ COMPLETE

**Goal:** Ensure correctness survives future changes.

- [x] **pytest test suite** — Unit tests for `format_time()`, `get_weather_icon()`, `get_precip_headline()`, `get_temp_color()`, and the WMO code mapper.
- [x] **API response mocking** — Test `get_weather_data()` against fixture JSON without hitting the live API.
- [x] **CI test job** — Add a `test` job to `ci.yml` that runs `pytest` on every push alongside lint and security.
- [x] **Code coverage badge** — Add `codecov` or `coverage.py` report to README.

---

## Phase 6: Distribution & Accessibility 🚀 NEXT

**Goal:** Make Isobar easy to install and run on any machine, even without a Python environment.

- [ ] **PyPI Release** — Publish `isobar-cli` to PyPI for easy `pip install` or `pipx install`.
- [ ] **Homebrew Formula** — Create a formula for `brew install isobar`.
- [ ] **AUR Package** — Publish to the Arch User Repository for Arch Linux users.
- [ ] **Winget / Scoop** — Windows package manager support.
- [ ] **Standalone Binaries** — Generate executable binaries for macOS, Linux, and Windows using PyInstaller or similar.
- [ ] **Global Install UX** — Ensure `isobar` command works globally after install without manual PATH configuration.

---

## Nice to Have (Carefully Considered)

Ideas that could be useful but are not core to the current mission. Will only ship if they don't compromise simplicity.

- [x] **Celsius / metric units flag** — `--metric` for non-Fahrenheit users.
- [x] **Hourly outlook** — Next 12h temperature curve, opt-in via `--hourly`.
- [x] **Multiple cities** — `isobar Chicago London Tokyo` side-by-side comparison.
- [x] **Air Quality Index (AQI)** — Integrated health classification.
- [x] **Fuzzy City Suggestions** — "Did you mean?" suggestions for typos.
- [x] **Shell completion** — Tab-complete city names from cache history.

---

## Future (Highly Skeptical)

Not planned. Noted here to say: *"Not unless there's a very strong reason."*

- [ ] **Multi-language support**
- [ ] **Customization surface** (colors, themes, layouts)
- [ ] **Animated icons**
- [ ] **Push notifications / alerts**

If any of these are ever considered, they must:
1. Not require config files for basic use.
2. Keep `isobar` simple and uncluttered.
3. Justify themselves in terms of comfort-understanding, not aesthetics alone.

---

## How to Use This Roadmap

If you're proposing a change:
- Point to where it fits (Phase 1–5, Nice to Have, or Future).
- Explain why it deserves to move from "Future" to a real phase.
- Be explicit about what you'd **remove**, not just what you'd add.

> The roadmap is a **guardrail against scope creep**, not a promise that everything listed will ship.
