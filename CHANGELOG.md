# Changelog

All notable changes to AndroRAT will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Comprehensive GitHub Projects section setup
- Issue templates (Bug Report, Feature Request, Security Issue)
- Pull Request template with detailed checklist
- CONTRIBUTING.md with comprehensive contribution guidelines
- CODE_OF_CONDUCT.md for community standards
- SECURITY.md for vulnerability reporting
- Dependabot configuration for automatic dependency updates
- FUNDING.yml for potential sponsorship
- Issue template configuration file

### Changed
- Enhanced project documentation structure
- Improved community contribution process

## [2.1.0] - 2025-10-14

### Added
- Android 15 (API 35) support
- Android 16 (API 36) preliminary support
- BODY_SENSORS_BACKGROUND permission for health sensors
- ACCESS_MEDIA_PROJECTION_STATE permission for screen sharing
- FOREGROUND_SERVICE_HEALTH foreground service type
- Comprehensive Android 15/16 upgrade tests
- APK integrity checker tool
- Complete testing framework summary

### Changed
- Updated compileSdkVersion from 34 to 35
- Updated targetSdkVersion from 34 to 35
- Updated buildToolsVersion from 34.0.0 to 35.0.0
- Enhanced MainActivity permission handling for API 35+
- Reorganized Android manifest permissions by API level
- Updated README with Android 15/16 compatibility matrix

### Fixed
- Permission request handling for Android 15+
- Backward compatibility with Android 6.0+ maintained
- Build configuration issues

### Documentation
- Added ANDROID_15_16_UPGRADE.md
- Updated all documentation for Android 15/16 support
- Enhanced testing documentation
- Improved API level compatibility documentation

## [2.0.0] - 2025-09-01

### Added
- Complete modernization for Android 13-16 compatibility
- Professional multi-client GUI interface
- APK injection technology
- Advanced malware detection evasion techniques
- Comprehensive testing suite
- TLS 1.2+ encryption for all communications
- WorkManager for background operations
- Scoped storage compliance (Android 10+)
- Modern permission system (Android 14+)
- Real-time monitoring and status dashboard
- Dual-pane file manager
- GPS location tracking with map integration
- Multi-device management capabilities

### Enhanced
- GUI interface completely redesigned
- Server architecture modernized
- Android client updated for latest APIs
- Build system improved
- Documentation extensively updated
- Test coverage significantly increased

### Security
- Added TLS encryption
- Implemented certificate-based authentication
- Enhanced permission handling
- Improved secure storage practices
- Added runtime permission requests

### Documentation
- Created comprehensive docs/ folder
- Added MODERNIZATION_GUIDE.md
- Added ENHANCED_FEATURES.md
- Added GUI_GUIDE.md
- Added APK_INJECTION_GUIDE.md
- Added MALWARE_DETECTION_EVASION_GUIDE.md
- Updated README with full feature matrix

### Testing
- Added comprehensive_test.py
- Added end_to_end_test.py
- Added comprehensive_functionality_test.py
- Created run_all_tests.py master test runner
- Integrated GitHub Actions CI/CD
- 95%+ test success rate

## [1.5.0] - 2024-06-01

### Added
- Basic GUI interface
- Ngrok support for internet accessibility
- Initial multi-client support
- File upload/download functionality
- Camera and audio capture features

### Changed
- Improved CLI interface
- Enhanced server stability
- Updated Android client for newer APIs

### Fixed
- Connection stability issues
- File transfer bugs
- Permission handling on newer Android versions

## [1.0.0] - 2023-01-01

### Added
- Initial release
- Basic remote administration features
- Android client application
- Python server with CLI
- Core functionality:
  - Device information retrieval
  - SMS and call log access
  - Location tracking
  - Shell command execution
  - File operations
  - Camera and microphone access

### Security
- Basic encryption implementation
- Permission handling

---

## Version Support

| Version | Status | Support Period | Android Support |
|---------|--------|---------------|-----------------|
| 2.1.x   | ✅ Current | Active | Android 6.0-16 (API 23-36) |
| 2.0.x   | ✅ Maintained | Security updates | Android 6.0-14 (API 23-34) |
| 1.x.x   | ❌ Unsupported | End of life | Android 5.0+ (API 21+) |

## Upgrade Notes

### Upgrading to 2.1.0

**New Requirements:**
- No breaking changes from 2.0.x
- Android 15/16 features are optional
- Backward compatible with Android 6.0+

**Recommended Actions:**
1. Update build tools to version 35.0.0 or later
2. Test on Android 15+ devices if available
3. Review new permissions in manifest
4. Run comprehensive test suite

### Upgrading to 2.0.0

**Breaking Changes:**
- Major server architecture changes
- New GUI interface (old GUI deprecated)
- Updated Android client with new features
- Changed configuration format

**Migration Steps:**
1. Back up existing configurations
2. Update Python dependencies: `pip install -r requirements.txt`
3. Review new documentation in docs/ folder
4. Rebuild APKs with new build system
5. Test thoroughly with new features

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for contribution guidelines.

## Security

See [SECURITY.md](SECURITY.md) for security policy and vulnerability reporting.

## License

This project is licensed under the MIT License - see [LICENSE](LICENSE) for details.

---

**Note:** This is an educational project. Use responsibly and ethically. Never use for malicious purposes or illegal activities.
