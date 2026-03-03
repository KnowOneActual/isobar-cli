# Homebrew Integration: Challenges and Implementation

This document logs the challenges and solutions encountered during the integration of `isobar` into the Homebrew ecosystem.

## Initial Strategy
- **Tooling:** `homebrew-pypi-poet` was used to generate the initial formula.
- **Distribution:** A custom tap repository (`KnowOneActual/homebrew-tap`) was created to host the formula.

## Key Technical Challenges

### 1. Virtual Environment Installation
Formulas using Python virtualenvs required the `include Language::Python::Virtualenv` module and correct implementation within the `install` block.
- **Resolution:** The `virtualenv_install_with_resources` method was implemented to handle isolation and symlinking within the Homebrew environment.

### 2. Dependency Management and Sandboxing
Relying on `pip` to manage dependencies within the virtualenv resulted in broken installations because Homebrew's sandbox blocks network requests during the build phase.
- **Resolution:** Every dependency was explicitly listed as a `resource` in the formula. This ensures Homebrew downloads all necessary components before entering the build sandbox.

### 3. Discovered Resource Requirements
Certain transitive dependencies, such as `flatbuffers` (required by `timezonefinder`), were omitted by automated tools because their URLs were not easily discoverable.
- **Resolution:** Manual research identified the correct PyPI source URLs and SHA256 hashes, which were then manually added to the formula.

### 4. Compilation and Build Prerequisites
Installations for libraries such as `numpy` and `h3` (C/C++ extensions) require local compilation from source. `h3` specifically requires `cmake` for its C core.
- **Resolution:** `depends_on "cmake" => :build` was added to the formula to provide the necessary build environment for C extensions. A note was added to the documentation to advise users on potential build times.

## Core Lessons
- **Isolation Standards:** Homebrew prioritizes environment isolation and building from source distribution over installation speed.
- **Resource Definition:** Successful Homebrew integration for a Python CLI requires explicit definition of all transitive dependencies.
- **Testing Requirements:** True tap verification is only possible after deployment and execution of `brew update`.

## Implementation Details
The final implementation provides a working, isolated installation of `isobar` in `/usr/local/Cellar/isobar/`, with a symlink provided at `/usr/local/bin/isobar`.

```bash
brew install KnowOneActual/tap/isobar
```
