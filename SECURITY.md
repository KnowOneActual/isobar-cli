# Security Policy

## Supported Versions

The following versions of Isobar CLI are currently supported with security updates:

| Version | Supported |
| ------- | --------- |
| 1.0.x   | ✅ Yes    |
| < 1.0.0 | ❌ No     |

## Reporting a Vulnerability

Security is a fundamental priority for the Isobar CLI project. If a potential security vulnerability is discovered, please do not report it via public issues. Instead, utilize the following method:

**GitHub Private Vulnerability Reporting:** Use the "Report a vulnerability" button under the **Security** tab of the repository. This is the most secure way to disclose findings directly to the maintainers.

A response can typically be expected within 48 hours.

## Automated Security Measures

The project employs multiple layers of automated scanning to maintain a high security standard:
- **Static Analysis (SAST):** Bandit and Semgrep scan the codebase for insecure patterns.
- **Vulnerability Scanning:** Trivy monitors the filesystem and dependencies for known CVEs.
- **Dependency Auditing:** pip-audit and Dependabot ensure third-party packages remain updated.
- **Script Linting:** ShellCheck enforces security best practices for all included scripts.

Results from these automated tools are monitored via the GitHub Security tab.
