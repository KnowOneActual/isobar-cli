# Release Protocol

This document outlines the standard operating procedure for releasing a new version of Isobar CLI to PyPI and Homebrew. Following these steps ensures consistent, reliable distribution.

## 1. Preparation

Before initiating a release, verify the following:
- All tests pass (`pytest`).
- Code coverage is maintained (`pytest --cov=isobar_cli`).
- Security scans and linting are passing (`ruff check .`, `pip-audit`).
- Local changes are committed and the working directory is clean.

## 2. Version Bump

1. **Update `pyproject.toml`:**
   Modify the `version` field to the new semantic version (e.g., `1.0.2`).
   ```toml
   [project]
   name = "isobar-cli"
   version = "1.0.2"
   ```

2. **Update `CHANGELOG.md`:**
   Move the contents of the `## [Unreleased]` section to a new section titled with the new version and today's date.
   ```markdown
   ## [1.0.2] - YYYY-MM-DD
   ### Added
   ...
   ```

3. **Commit Changes:**
   Commit the version bump using the standard commit message format.
   ```bash
   git add pyproject.toml CHANGELOG.md
   git commit -m "release: v1.0.2"
   git push
   ```

## 3. PyPI Release (Automated)

The release to PyPI is automated via GitHub Actions (`.github/workflows/publish.yml`) and is triggered by pushing a version tag.

1. **Tag the Release:**
   ```bash
   git tag v1.0.2
   git push origin v1.0.2
   ```

2. **Verify:**
   Check the GitHub Actions tab to confirm the "Publish to PyPI" workflow completed successfully. Verify the new version is live on PyPI at `https://pypi.org/project/isobar-cli/`.

## 4. Homebrew Release (Manual)

Homebrew distribution is managed via a separate tap repository (`KnowOneActual/homebrew-tap`). It must be updated *after* the PyPI release is live.

1. **Fetch New PyPI Details:**
   Retrieve the `tar.gz` URL and its SHA256 hash from the new PyPI release.
   ```bash
   curl -s https://pypi.org/pypi/isobar-cli/json | jq -r '.releases["1.0.2"][] | select(.packagetype=="sdist") | .url, .digests.sha256'
   ```

2. **Update the Formula (`Formula/isobar.rb`):**
   Update the local `Formula/isobar.rb` in this repository for historical tracking:
   - Update `url` to the new `tar.gz` URL.
   - Update `sha256` to the new hash.
   - If there are new dependencies, update the `resource` blocks.

   Commit the update:
   ```bash
   git add Formula/isobar.rb
   git commit -m "docs: Update local Homebrew formula to v1.0.2"
   git push
   ```

3. **Push to the Tap:**
   Copy the updated `Formula/isobar.rb` into your local `homebrew-tap` repository, commit, and push.
   ```bash
   # In the homebrew-tap directory
   cp ../isobar-cli/Formula/isobar.rb ./Formula/isobar.rb
   git add Formula/isobar.rb
   git commit -m "isobar: update to v1.0.2"
   git push
   ```

4. **Verify Installation:**
   ```bash
   brew update
   brew upgrade isobar
   ```
