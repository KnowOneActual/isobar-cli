# Contributing to Isobar CLI

Thanks for your interest in contributing to Isobar CLI!

This project is intentionally small and opinionated. The goal is not to become a full-featured weather dashboard, but to answer one question well:

> “What does it feel like outside right now?”

Contributions are welcome as long as they respect that constraint.

## Core Principles

Before opening an issue or PR, align with these principles:

- **Single purpose** – Everything should serve the “what does it feel like outside?” question.
- **Essential over comprehensive** – Fewer, more meaningful data points beat large tables of stats.
- **Terminal-native** – Fast, readable, no GUI thinking sneaking in.
- **Zero friction** – Avoid config, setup steps, or requirements unless absolutely necessary.
- **Intentional features** – No feature “just because it’d be cool.”

If a change doesn’t clearly improve comfort-understanding or developer ergonomics, it probably doesn’t belong.

## What’s in scope

Good candidates for contributions:

- Improving clarity of the existing output (layout, wording, accessibility).
- Enhancing comfort-related metrics (e.g., AQI, sunrise/sunset, short forecast) in ways consistent with the roadmap.
- Performance improvements (faster responses, sensible caching) without complicating usage.
- Robustness (better error handling, edge cases, tests).
- Developer experience improvements that don’t leak complexity onto the user.

## What’s out of scope (for now)

Changes that are usually not a fit:

- Heavy customization systems (themes, arbitrary layouts, fonts).
- Turning Isobar into a general-purpose weather dashboard.
- Features unrelated to the “feels like outside right now” mission.
- Large dependency trees or complex configuration for marginal benefit.

If you’re unsure, open a small issue first and describe the problem and why it matters.

## How to contribute

1. **Open an Issue (recommended)**
   - Describe the problem you’re solving, not just the solution you want.
   - Explain how it helps answer “what does it feel like outside?”

2. **Fork & Branch**
   - Fork the repo.
   - Create a branch from `main`:
     ```bash
     git checkout -b feature/short-description
     ```
   - If you use `start-work.sh`, you can let it handle the branch naming for you.

3. **Make focused changes**
   - Keep PRs small and single-purpose.
   - If you find unrelated cleanups, either keep them minimal or send them as a separate PR.

4. **Run tests & checks**
   - Ensure the CLI still runs:
     ```bash
     pip install -e ".[test]"
     isobar "Chicago"
     ```
   - Run the test suite:
     ```bash
     pytest
     ```
   - For detailed instructions on writing and running tests, see [docs/TESTING.md](docs/TESTING.md).

5. **Open a Pull Request**
   - Clearly state:
     - The problem.
     - The proposed change.
     - How it supports the project philosophy and roadmap.
   - If your change touches user-facing behavior, include before/after screenshots or terminal output.

## Design discussion

For bigger ideas or direction shifts, please:

- Reference the sections in `README.md` (“Philosophy”, “Project Direction”, “What This Project Is Not”).
- Reference specific roadmap items in `ROADMAP.md` where your idea fits or propose a new item.

The maintainer may ask “How does this help someone understand what it feels like outside?” more than once. That’s by design.

## Code style

- Favor readability and simplicity over cleverness.
- Keep modules focused (`api`, `ui`, CLI entrypoint).
- Avoid introducing heavy dependencies without a strong, user-facing reason.

Thanks for helping keep Isobar CLI small, sharp, and intentional.
