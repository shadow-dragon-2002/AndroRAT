# AndroRAT Test Suite Documentation

## Overview

This directory contains comprehensive test suites for validating AndroRAT functionality, Android compatibility, and APK integrity.

## Test Files

### Core Test Suites

#### `test_android_15_16_upgrade.py`
**Purpose**: Validates Android 15/16 upgrade implementation

**Test Classes**:
- `Android15UpgradeTests` - Validates API 35 configuration and permissions
- `APKIntegrityTests` - Validates APK build tools and project structure
- `ComprehensiveUpgradeValidation` - Validates documentation and cleanup

**Coverage**:
- ✅ Build configuration (API 35, build tools 35.0.0)
- ✅ Android 15+ permissions (BODY_SENSORS_BACKGROUND, ACCESS_MEDIA_PROJECTION_STATE)
- ✅ MainActivity permission handling for API 35
- ✅ Backward compatibility (API 23+)
- ✅ Documentation updates
- ✅ Cleanup verification

**Run**: `python3 test_android_15_16_upgrade.py`

#### `apk_integrity_checker.py`
**Purpose**: APK structure and integrity validation

**Features**:
- ✅ APK file existence and validity
- ✅ ZIP structure verification
- ✅ Signature checking (v1/v2/v3)
- ✅ Manifest parsing and analysis
- ✅ Permission validation
- ✅ SDK version verification
- ✅ Foreground service type checking
- ✅ APK size validation

**Usage**:
```bash
python3 apk_integrity_checker.py /path/to/your.apk
```

**Example Output**:
```
Checking APK: output.apk
======================================================================

Existence:
✓ APK file exists

ZIP Structure:
✓ APK is valid ZIP with 156 files

Signature:
✓ APK has v1 signature (JAR signing)

Size:
✓ APK size: 5.23 MB

Manifest & Permissions:
✓ minSdkVersion: 23, targetSdkVersion: 35
✓ Targeting Android 15+ (API 35+)
✓ Found 42 permissions
✓ Android 15+ permissions found: ['BODY_SENSORS_BACKGROUND', 'ACCESS_MEDIA_PROJECTION_STATE']
✓ Foreground service type: dataSync

======================================================================
✅ APK INTEGRITY CHECK PASSED
======================================================================
```

#### `comprehensive_functionality_test.py`
**Purpose**: Android compatibility and feature validation

**Test Classes**:
- `AndroidCompatibilityTests` - Modern Android features and permissions

**Coverage**:
- Android 13-15+ permissions
- WorkManager dependencies
- Enhanced Java files
- Manifest configuration

**Run**: `python3 -m unittest comprehensive_functionality_test.AndroidCompatibilityTests`

#### `comprehensive_test.py`
**Purpose**: Complete system validation

**Test Classes**:
- `ComprehensiveAndroRATTests` - End-to-end system tests

**Coverage**:
- Android configuration validation
- Gradle configuration
- File structure
- Permission validation

**Run**: `python3 -m unittest comprehensive_test.ComprehensiveAndroRATTests`

### Additional Test Files

- `test_androrat.py` - Basic AndroRAT functionality
- `test_enhanced_features.py` - Enhanced feature validation
- `end_to_end_test.py` - Complete end-to-end testing
- `apk_build_test.py` - APK building process tests
- `test_apk_injection.py` - APK injection tests
- `test_modernization.py` - Modernization feature tests

## Master Test Runner

### `run_all_tests.py` (in project root)

Executes all test suites and generates comprehensive report.

**Usage**:
```bash
python3 run_all_tests.py
```

**Features**:
- Runs all available test suites
- Collects results from all tests
- Generates detailed test report
- Saves report to `TEST_REPORT.txt`
- Returns appropriate exit codes

**Output**:
```
================================================================================
ANDRORAT COMPREHENSIVE TEST REPORT
================================================================================

Generated: 2025-10-16 07:07:23
Duration: 0.07 seconds

--------------------------------------------------------------------------------
TEST SUITE RESULTS
--------------------------------------------------------------------------------

Android 15/16 Upgrade Tests: ✅ PASS
  Total:  5
  Passed: 5
  Failed: 0
  Errors: 0

[... more suites ...]

--------------------------------------------------------------------------------
OVERALL SUMMARY
--------------------------------------------------------------------------------
Total Tests:     19
Passed:          19
Failed:          0
Errors:          0
Success Rate:    100.0%

================================================================================
✅ ALL TEST SUITES PASSED - SYSTEM VALIDATED
================================================================================
```

## Automated Testing

### GitHub Actions Workflow

**File**: `.github/workflows/test-android-upgrade.yml`

**Triggers**:
- Push to master/main/develop branches
- Pull requests to master/main/develop
- Manual workflow dispatch

**Jobs**:

1. **test-upgrade** - Runs Python test suites
   - Android 15/16 upgrade tests
   - Comprehensive functionality tests
   - Gradle configuration checks

2. **test-apk-structure** - Validates APK and project structure
   - APK tools verification
   - Android project structure
   - Permission validation
   - MainActivity support checks

3. **documentation-check** - Validates documentation
   - Upgrade documentation exists
   - Documentation content verification
   - Cleanup verification

**Status**: View at `https://github.com/shadow-dragon-2002/AndroRAT/actions`

## Running Tests

### Run All Tests
```bash
# From project root
python3 run_all_tests.py
```

### Run Specific Test Suite
```bash
# Android 15/16 upgrade tests
cd tests
python3 test_android_15_16_upgrade.py

# Comprehensive functionality tests
python3 -m unittest comprehensive_functionality_test.AndroidCompatibilityTests

# Comprehensive tests
python3 -m unittest comprehensive_test.ComprehensiveAndroRATTests
```

### Run Individual Test
```bash
cd tests
python3 -m unittest test_android_15_16_upgrade.Android15UpgradeTests.test_build_gradle_api_35
```

### Check APK Integrity
```bash
cd tests
python3 apk_integrity_checker.py /path/to/your.apk
```

## Test Requirements

### System Requirements
- Python 3.6+
- Java 8+ (for apktool and APK tools)
- Android SDK (optional, for full Android testing)

### Python Dependencies
```bash
pip install -r requirements.txt
```

### Project Structure
Tests expect the following structure:
```
AndroRAT/
├── Android_Code/
│   ├── app/
│   │   ├── build.gradle
│   │   └── src/main/
│   │       ├── AndroidManifest.xml
│   │       └── java/com/example/reverseshell2/
│   ├── build.gradle
│   ├── settings.gradle
│   └── gradlew
├── Jar_utils/
│   ├── apktool.jar
│   └── sign.jar
├── tests/
│   ├── test_android_15_16_upgrade.py
│   ├── apk_integrity_checker.py
│   └── ...
└── run_all_tests.py
```

## Test Coverage

### Android Version Support
- ✅ Android 6.0+ (API 23+) - Minimum support
- ✅ Android 12+ (API 31+) - Enhanced features
- ✅ Android 13+ (API 33+) - Modern permissions
- ✅ Android 14+ (API 34+) - Visual media
- ✅ Android 15+ (API 35+) - Latest features ⭐
- ✅ Android 16 (API 36) - Future ready ⭐

### Permission Coverage
Tests validate all permissions from Android 13-15+:
- POST_NOTIFICATIONS (Android 13+)
- READ_MEDIA_* (Android 13+)
- READ_MEDIA_VISUAL_USER_SELECTED (Android 14+)
- BODY_SENSORS_BACKGROUND (Android 15+)
- ACCESS_MEDIA_PROJECTION_STATE (Android 15+)
- FOREGROUND_SERVICE_* types (Android 14+)

### Build Configuration Coverage
- ✅ compileSdkVersion 35
- ✅ targetSdkVersion 35
- ✅ minSdkVersion 23
- ✅ buildToolsVersion 35.0.0

## Continuous Integration

Tests are automatically run on:
- Every push to main branches
- All pull requests
- Manual trigger via GitHub Actions

View test results:
1. Go to repository on GitHub
2. Click "Actions" tab
3. Select "Android 15/16 Upgrade Tests" workflow

## Troubleshooting

### Common Issues

**Issue**: `ModuleNotFoundError: No module named 'test_utils'`
**Solution**: Run tests from the `tests/` directory or ensure `test_utils.py` is present

**Issue**: `apktool not found`
**Solution**: Ensure `Jar_utils/apktool.jar` exists and Java is installed

**Issue**: Tests fail with path errors
**Solution**: Ensure you're running from correct directory and project structure is intact

**Issue**: Permission tests fail
**Solution**: Verify AndroidManifest.xml has all required Android 15+ permissions

## Contributing

When adding new features:

1. Add corresponding tests to appropriate test file
2. Update test documentation
3. Ensure all tests pass before committing
4. Update GitHub Actions workflow if needed

## Support

For issues or questions about tests:
- Check test output for specific error messages
- Review test file source code for test expectations
- Verify project structure matches requirements
- Run individual tests to isolate issues

---

*Last Updated: October 16, 2025*
*Test Framework Version: 2.1*
