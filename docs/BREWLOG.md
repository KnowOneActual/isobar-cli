# Homebrew Journey: From zero to Tap

Getting `isobar` onto Homebrew was a milestone for the project, but it came with its own set of challenges. This log documents the "rough road" and what we learned along the way.

## Initial Setup
- **Tool used:** `homebrew-pypi-poet` (to generate the formula).
- **Strategy:** Build a "tap" (a separate GitHub repository) at `KnowOneActual/homebrew-tap` to host the formula.

## Challenges & Solutions

### 1. The `NameError` (Virtualenvs)
Initially, we faced a `NameError` related to `virtualenv_install_with_resources`.
- **Cause:** Homebrew formulas that use Python virtualenvs require the `include Language::Python::Virtualenv` module. We also needed to ensure it was used correctly in the `install` block.
- **Solution:** Switched to the robust `virtualenv_install_with_resources` method which handles isolation and symlinking automatically.

### 2. The `command not found` Error
Even after a "successful" looking install, the `isobar` command wasn't working.
- **Cause:** We tried letting `pip` handle the dependencies inside the virtualenv (which is fast because it uses wheels), but Homebrew's sandbox often blocks network requests during the build phase. This led to a broken, empty installation.
- **Solution:** Reverted to the "standard" Homebrew way: explicitly listing every dependency as a `resource` in the formula. This ensures Homebrew downloads everything *before* the sandbox is closed.

### 3. Missing Resources (`flatbuffers`)
The build stalled because of a missing dependency for `timezonefinder`.
- **Cause:** `poet` missed the `flatbuffers` resource because its URL wasn't easily discoverable on PyPI.
- **Solution:** Manually researched the correct PyPI source URL and SHA256 for `flatbuffers` and added it to the formula.

### 4. The "Stall" (Compilation)
Installation seemed to hang on `h3` or `numpy`.
- **Cause:** Homebrew builds from source distributions (`.tar.gz`). Heavy libraries like `numpy` and `h3` (C/C++ extensions) require compilation, which can take several minutes.
- **Learning:** `pipx` is faster because it uses wheels, but `brew` is more robust and isolated. We added a note to the README to warn users about the build time.

## Key Learnings
- **Homebrew is strict.** It values isolation and "building from source" over speed.
- **Resources are everything.** For a Python CLI to work on Homebrew, you *must* explicitly define every single transitive dependency.
- **Testing is hard.** You can't truly test a tap until it's pushed and `brew update` is run.

## Final Result
A working, isolated installation of `isobar` that lives in `/usr/local/Cellar/isobar/` and is symlinked to `/usr/local/bin/isobar`.

```bash
brew install KnowOneActual/tap/isobar
```

It was a tough road, but now `isobar` is part of the Homebrew ecosystem! 🍻
