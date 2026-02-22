# Isobar CLI Roadmap

This roadmap describes **intentional, phased changes** to Isobar CLI.

The mission stays the same:

> Help you quickly understand what it feels like outside, from your terminal.

Everything here is optional until it proves it actually improves that mission.

---

## Phase 1: Speed & Flow (Near-Term)

**Goal:** Make the existing experience faster and more convenient, without changing what Isobar is.

- [X] **Local Caching (≈ 15 minutes)**  
       Cache the last successful response per location to: - Avoid hammering the API on repeated checks. - Make repeated calls feel instant when conditions haven’t changed much.  
       This will only ship if it delivers noticeable UX gains over the current Open-Meteo latency.

- [ ] **Auto-Location (optional flag or default)**  
       Allow running `isobar` with no city to use current IP-based location.  
       Must: - Fail gracefully with a clear message. - Never require config files or accounts.

---

## Phase 2: Deeper Comfort Context

**Goal:** Add _a bit more_ information that directly informs comfort, without turning into a dashboard.

- [ ] **Rain / Snow / Cloud Coverage**  
       Show a simple percentage of rain, snow (expanded currently), and cloud coverage for the current location.

- [ ] **Air Quality Index (AQI)**  
       Show a simple AQI metric and qualitative label (e.g., “Good”, “Moderate”) for the current location.

- [ ] **Sunrise / Sunset Times**  
       Add sunrise and sunset to the readout so users can quickly gauge remaining daylight.

Any new metric added here must answer:  
**“Would I make a different decision about going outside because of this?”**

---

## Phase 3: Visual Communication & Forecasting

**Goal:** Improve how information is communicated, not how much information there is.

- [ ] **ASCII / Text Weather Icons**  
       Small text-based icons that reinforce current conditions (sun, rain, snow, clouds).  
       Must: - Be legible in typical terminal setups. - Add clarity, not visual noise.

- [ ] **Mini Forecast (opt-in flag)**  
       A short, optional forecast (next few hours or days) exposed via a flag like:
      `bash
    isobar "Chicago" --mini-forecast
    `
      The default command should remain focused on “right now”.

- [ ] **Subtle Visual Enhancements**  
       Small tweaks (spacing, emphasis, color choices) that make the card clearer without adding busy-ness.

---

## Nice to Have (Carefully Considered)

Ideas that could be fun but are not core to the mission. These will only be implemented if they **don’t compromise simplicity** and there is real demand.

- [ ] **Animated Weather Icons**  
       Lightweight ASCII animations that run only when explicitly requested.

- [ ] **Colorful Weather Icons**  
       Tasteful use of color that remains readable on common background themes.

---

## Future Roadmap (Highly Skeptical)

These are **not planned** features. They’re noted here primarily to say:  
“Not unless there’s a very strong reason.”

- [ ] **Customizable Units**  
       Might ship if enough non-Fahrenheit users adopt Isobar.

- [ ] **Multi-Language Support**  
       Might ship if enough non-English speakers adopt Isobar. It’s not a priority.

- [ ] **Multiple Cities in One Run**  
       	It might be shipped if enough users are interested in checking multiple locations at once. However, I'm unsure whether this feature would be useful enough for many people to spend time on.

- [ ] **Customization Surface (colors, layout, icons, fonts, backgrounds, themes, etc.)**

If any of these are ever considered, they must:

1. Not require config files for basic use.
2. Keep `isobar <city>` simple and uncluttered.
3. Justify themselves in terms of comfort-understanding, not aesthetics alone.

---

## How to Use This Roadmap 

If you’re proposing a change:

- Point to where it fits (Phase 1/2/3, Nice to Have, or Future).
- Explain why it deserves to move from “Future” to a real phase.
- Be explicit about what you’d remove, not just what you’d add.

> The roadmap is a **guardrail against scope creep**, not a promise that everything listed here will ship.
