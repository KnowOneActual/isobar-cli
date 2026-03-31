# Contributing to Isobar CLI

Thank you for your interest in contributing to Isobar CLI.

This project is intentionally focused and opinionated. The mission is not to provide a comprehensive weather dashboard, but to answer one question well:

> “What does it feel like outside right now?”

Contributions are welcome as long as they align with this objective and the project's design principles.

## Core Principles

Proposed changes should align with the following principles:

- **Single purpose** – Everything should serve the “what does it feel like outside?” mission.
- **Essential over comprehensive** – Prioritize meaningful data points over exhaustive statistics.
- **Terminal-native** – Fast, readable, and focused on the command-line experience.
- **Zero friction** – Avoid introducing complex configuration or setup requirements.
- **Intentional features** – Features are added based on their utility for situational awareness, not "just because."

Changes that do not clearly enhance comfort-understanding or developer ergonomics are likely outside the project's scope.

## Project Scope

### In Scope
- Enhancing output clarity (layout, wording, accessibility).
- Improving comfort-related metrics (e.g., AQI, solar events, short-term forecasts) consistent with the roadmap.
- Performance optimizations (faster responses, efficient caching) that maintain simplicity.
- Increasing robustness (better error handling, edge case management, tests).
- Developer experience improvements that do not increase end-user complexity.

### Out of Scope
- Heavy customization systems (themes, arbitrary layouts, font management).
- Turning Isobar into a general-purpose weather dashboard.
- Features unrelated to the "feels like outside right now" mission.
- Significant increases in dependency complexity for marginal benefit.

For ambiguous cases, please open an issue to describe the problem and the proposed value.

## Contribution Process

1. **Open an Issue**
   - Define the problem being addressed.
   - Explain how the proposed change supports the project's core mission.

2. **Fork and Branch**
   - Fork the repository.
   - Create a branch from `main`:
     ```bash
     git checkout -b feature/short-description
     ```
   - The `start-work.sh` script may be used to assist with branch management.

3. **Implement Focused Changes**
   - Maintain small, single-purpose Pull Requests.
   - Address unrelated cleanups in separate PRs where possible.

4. **Verify Changes**
   - Ensure the CLI still runs:
     ```bash
     pip install -e ".[test]"
     isobar "Chicago"
     ```
   - Execute the test suite:
     ```bash
     pytest
     ```
   - Refer to [docs/TESTING.md](docs/TESTING.md) for detailed testing instructions.

5. **Submit a Pull Request**
   - Provide a clear description of:
     - The problem addressed.
     - The implementation details.
     - Alignment with the project philosophy and roadmap.
   - For user-facing changes, include example output or screenshots.

## Design Alignment

For significant structural or directional changes:
- Reference the "Philosophy" and "Design Principles" sections in the `README.md`.
- Identify the relevant roadmap items in `ROADMAP.md` or propose new strategic additions.

Expect the following question during code review: **"How does this help someone understand what it feels like outside?"** This focus ensures Isobar stays true to its mission.

## Code Standards

- Prioritize readability and simplicity over cleverness.
- Maintain modular separation (e.g., `api`, `ui`, CLI entrypoint).
- Avoid introducing heavy dependencies without a strong, user-facing reason.

## Known Issues & Technical Debt

For contributors looking to help improve the project, here are some known issues and areas for improvement:

### Current Limitations
1. **`home` subcommand conflict**: Due to Typer's `invoke_without_command=True` behavior, `isobar home "City"` doesn't work as expected (shows weather for Home, Kansas instead of setting home city).
2. **Flag ordering requirement**: Flags (`-H`, `-f`, `-m`) must come before city arguments.

### Technical Debt
1. **Test mock complexity**: Tests require verbose `WeatherData` constructor calls that are brittle to model changes.
2. **API client organization**: Could benefit from better abstraction of common HTTP client logic.

For detailed information on these issues, see [KNOWN_ISSUES.md](KNOWN_ISSUES.md).

Thank you for contributing to the continued development of a focused and intentional Isobar CLI.
