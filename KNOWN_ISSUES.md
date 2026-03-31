# Known Issues & Limitations

This document tracks known issues, limitations, and technical debt in the Isobar CLI project.

## Current Issues

### 1. `home` Subcommand Conflict with `invoke_without_command=True`

**Status**: Known Limitation  
**Priority**: Medium  
**Affects**: CLI usability  
**Created**: 2026-03-30  
**Last Updated**: 2026-03-30  

**Description**:  
When using Typer's `invoke_without_command=True` to make weather display the default behavior, the `home` subcommand doesn't work correctly. The command `isobar home "Chicago"` shows weather for "Home, Kansas" instead of invoking the `home` subcommand to set the home city.

**Root Cause**:  
Typer with `invoke_without_command=True` tries to parse all arguments through the callback first, before checking if they match a subcommand. When it sees `["home", "Chicago"]`, it treats "home" as a city name argument rather than recognizing it as a subcommand.

**Impact**:  
- Users cannot use `isobar home "City"` to set their home city
- The `home` subcommand is effectively unusable in its current form
- Workaround: Users must manually edit `~/.config/isobar/config.json`

**Potential Solutions**:  
1. Rename the subcommand to something that doesn't conflict with city names (e.g., `set-home`, `config-home`)
2. Implement custom argument parsing to detect "home" and invoke the subcommand manually
3. Remove `invoke_without_command=True` and require `isobar weather Chicago` for weather display
4. Use a different CLI framework that handles this case better

**Related Files**:  
- `src/isobar_cli/main.py` - CLI structure with `invoke_without_command=True`
- `src/isobar_cli/config.py` - Home city configuration logic

### 2. Flag Ordering Requirement

**Status**: Known Limitation  
**Priority**: Low  
**Affects**: CLI usability  
**Created**: 2026-03-30  
**Last Updated**: 2026-03-30  

**Description**:  
Flags (`-H`, `-f`, `-m`) must come before city arguments. `isobar Chicago -H` doesn't work; users must use `isobar -H Chicago`.

**Root Cause**:  
Typer's argument parsing treats everything after city arguments as additional cities, not flags.

**Impact**:  
- Non-intuitive for users accustomed to other CLI tools
- Requires documentation and user education

**Workaround**:  
Document that flags must come before city names.

**Related Files**:  
- `src/isobar_cli/main.py` - Argument parsing logic

## Recently Fixed Issues

### 3. Hourly (`-H`) and Weekly Forecast (`-f`) Regression

**Status**: Fixed in v1.1.2  
**Priority**: High (was blocking)  
**Affected**: All users  
**Created**: 2026-03-30  
**Fixed**: 2026-03-30  

**Description**:  
The hourly (`-H`) and weekly forecast (`-f`) functionality was broken when the `home` command was added in v1.1.0.

**Root Cause**:  
CLI structure change made `main` a subcommand, requiring `isobar main Chicago -H` instead of `isobar Chicago -H`.

**Solution**:  
Restored `invoke_without_command=True` to make weather display the default behavior.

**Related Files**:  
- `src/isobar_cli/main.py` - Fixed CLI structure
- `tests/test_main.py` - Updated tests
- `tests/test_isobar_extra.py` - Updated tests

## Technical Debt

### 4. Test Mock Complexity

**Status**: Technical Debt  
**Priority**: Low  
**Affects**: Test maintenance  

**Description**:  
Tests require complex mocking of `WeatherData` constructors with many parameters. Changes to the `WeatherData` model require updating many test files.

**Impact**:  
- High maintenance cost for model changes
- Tests are brittle

**Potential Solution**:  
Create test fixture factories or builder pattern for `WeatherData` creation.

**Related Files**:  
- `tests/test_main.py` - Multiple `WeatherData` constructor calls
- `tests/test_isobar_extra.py` - Multiple `WeatherData` constructor calls
- `src/isobar_cli/models.py` - `WeatherData` model definition

### 5. API Client Separation Could Be Cleaner

**Status**: Technical Debt  
**Priority**: Low  
**Affects**: Code organization  

**Description**:  
While `api.py` was decomposed into logical clients (`GeocodingClient`, `WeatherClient`, `AirQualityClient`), they still share some common functionality that could be better abstracted.

**Impact**:  
- Some code duplication
- Could be more DRY

**Potential Solution**:  
Extract common HTTP client logic into a base class.

**Related Files**:  
- `src/isobar_cli/api.py` - API client implementations

## Issue Tracking

| Issue | Status | Priority | Created | Last Updated |
|-------|--------|----------|---------|--------------|
| `home` subcommand conflict | Known Limitation | Medium | 2026-03-30 | 2026-03-30 |
| Flag ordering requirement | Known Limitation | Low | 2026-03-30 | 2026-03-30 |
| Hourly/forecast regression | Fixed | High | 2026-03-30 | 2026-03-30 |
| Test mock complexity | Technical Debt | Low | 2026-03-30 | 2026-03-30 |
| API client organization | Technical Debt | Low | 2026-03-30 | 2026-03-30 |

## Resolution Priority

1. **High Priority**: Issues blocking core functionality (e.g., hourly/forecast regression - FIXED)
2. **Medium Priority**: Issues affecting usability but with workarounds (e.g., `home` subcommand)
3. **Low Priority**: Technical debt and minor usability issues

## Contributing Fixes

When fixing any of these issues:
1. Update this document with the fix details
2. Add appropriate tests
3. Update CHANGELOG.md
4. Consider backward compatibility
5. Document any breaking changes