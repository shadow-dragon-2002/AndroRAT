# Contributing to AndroRAT

Thank you for your interest in contributing to AndroRAT! This document provides guidelines and instructions for contributing to the project.

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [How to Contribute](#how-to-contribute)
- [Development Setup](#development-setup)
- [Coding Standards](#coding-standards)
- [Testing Guidelines](#testing-guidelines)
- [Submitting Changes](#submitting-changes)
- [Security Guidelines](#security-guidelines)

## 🤝 Code of Conduct

This project adheres to a Code of Conduct that all contributors are expected to follow. Please read [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) before contributing.

**Key Principles:**
- Be respectful and inclusive
- Educational and research purposes only
- No malicious use or illegal activities
- Responsible disclosure of security issues

## 🚀 Getting Started

### Prerequisites

Before contributing, ensure you have:

- **Python 3.6+** (Recommended: Python 3.8+)
- **Java Development Kit (JDK)** or **Android Studio**
- **Git** for version control
- Basic understanding of Android development (for Android client contributions)
- Familiarity with Python (for server-side contributions)

### Understanding the Project

1. **Read the Documentation:**
   - [README.md](README.md) - Project overview and features
   - [docs/MODERNIZATION_GUIDE.md](docs/MODERNIZATION_GUIDE.md) - Technical implementation guide
   - [docs/ENHANCED_FEATURES.md](docs/ENHANCED_FEATURES.md) - Feature documentation
   - [ANDROID_15_16_UPGRADE.md](ANDROID_15_16_UPGRADE.md) - Latest Android support

2. **Explore the Codebase:**
   ```
   AndroRAT/
   ├── Android_Code/        # Android client (Java)
   ├── server/             # Python server components
   ├── tests/              # Test suite
   ├── docs/               # Documentation
   └── tools/              # Utility tools
   ```

3. **Run the Tests:**
   ```bash
   python3 run_all_tests.py
   ```

## 💡 How to Contribute

### Types of Contributions

We welcome various types of contributions:

1. **🐛 Bug Fixes**
   - Fix reported bugs
   - Improve error handling
   - Resolve compatibility issues

2. **✨ New Features**
   - Implement roadmap items
   - Add requested features
   - Enhance existing functionality

3. **📚 Documentation**
   - Improve existing docs
   - Add code comments
   - Create tutorials or guides

4. **🧪 Testing**
   - Write new tests
   - Improve test coverage
   - Add edge case testing

5. **🔒 Security Enhancements**
   - Improve security measures
   - Fix vulnerabilities
   - Enhance encryption

6. **⚡ Performance Improvements**
   - Optimize code
   - Reduce resource usage
   - Improve efficiency

### Before You Start

1. **Check Existing Issues:** Search for existing issues or feature requests
2. **Discuss Major Changes:** Open an issue to discuss significant changes before implementing
3. **Review Roadmap:** Check the roadmap in README.md to align with project goals
4. **Avoid Duplicates:** Ensure your contribution isn't already in progress

## 🛠️ Development Setup

### 1. Fork and Clone

```bash
# Fork the repository on GitHub, then clone your fork
git clone https://github.com/YOUR_USERNAME/AndroRAT.git
cd AndroRAT

# Add upstream remote
git remote add upstream https://github.com/shadow-dragon-2002/AndroRAT.git
```

### 2. Install Dependencies

```bash
# Install Python dependencies
pip install -r requirements.txt

# For Android development, import Android_Code into Android Studio
```

### 3. Create a Branch

```bash
# Create a new branch for your changes
git checkout -b feature/your-feature-name
# or
git checkout -b fix/bug-description
```

### 4. Set Up Development Environment

**For Server Development:**
```bash
# Test the CLI
python3 server/androRAT.py --help

# Test the GUI
python3 server/androRAT_advanced_gui.py
```

**For Android Development:**
1. Open `Android_Code` in Android Studio
2. Sync Gradle files
3. Build the project
4. Run on emulator or device

## 📝 Coding Standards

### Python Code Style

- Follow [PEP 8](https://pep8.org/) style guide
- Use meaningful variable and function names
- Add docstrings to functions and classes
- Keep functions focused and modular
- Use type hints where appropriate

**Example:**
```python
def build_apk(ip_address: str, port: int, output_file: str) -> bool:
    """
    Build an APK with specified configuration.
    
    Args:
        ip_address: Server IP address
        port: Server port number
        output_file: Output APK file path
        
    Returns:
        bool: True if build succeeded, False otherwise
    """
    # Implementation
    pass
```

### Java Code Style

- Follow Android coding conventions
- Use meaningful class and method names
- Add comments for complex logic
- Handle Android API level differences properly
- Use appropriate Android lifecycle methods

**Example:**
```java
/**
 * Request necessary permissions for Android 15+
 */
@TargetApi(Build.VERSION_CODES.VANILLA_ICE_CREAM)
private void requestAndroid15Permissions() {
    // Implementation
}
```

### General Guidelines

- **Keep changes minimal and focused** - One PR per feature/fix
- **Write clear commit messages** - Use descriptive messages
- **Add comments for complex code** - Help others understand
- **Handle errors gracefully** - Don't let exceptions crash the app
- **Test edge cases** - Consider unusual scenarios
- **Maintain backward compatibility** - Unless breaking changes are necessary

## 🧪 Testing Guidelines

### Running Tests

**All Tests:**
```bash
python3 run_all_tests.py
```

**Specific Test Suites:**
```bash
# Android 15/16 compatibility
cd tests
python3 test_android_15_16_upgrade.py

# APK integrity
python3 apk_integrity_checker.py /path/to/test.apk

# Comprehensive tests
python3 -m unittest comprehensive_test.ComprehensiveAndroRATTests
```

### Writing Tests

1. **Unit Tests:** Test individual functions and methods
2. **Integration Tests:** Test component interactions
3. **End-to-End Tests:** Test complete workflows
4. **Compatibility Tests:** Test across Android versions

**Test Structure:**
```python
import unittest

class MyFeatureTests(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures"""
        pass
    
    def test_specific_functionality(self):
        """Test specific feature"""
        # Arrange
        # Act
        # Assert
        pass
    
    def tearDown(self):
        """Clean up after tests"""
        pass
```

### Test Requirements

- All new features must include tests
- Bug fixes should include regression tests
- Tests must pass before PR submission
- Maintain or improve test coverage

## 📤 Submitting Changes

### 1. Commit Your Changes

```bash
# Stage your changes
git add .

# Commit with a clear message
git commit -m "Add feature: [brief description]"
# or
git commit -m "Fix: [bug description]"
```

**Commit Message Format:**
```
<type>: <subject>

<body>

<footer>
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

**Example:**
```
feat: Add Android 16 support for new permissions

- Updated compileSdkVersion to 36
- Added BODY_SENSORS_BACKGROUND permission
- Updated MainActivity permission handling
- Added compatibility checks

Closes #123
```

### 2. Push to Your Fork

```bash
git push origin feature/your-feature-name
```

### 3. Create a Pull Request

1. Go to your fork on GitHub
2. Click "Pull Request"
3. Select your branch
4. Fill out the PR template completely
5. Provide clear description of changes
6. Reference related issues
7. Add screenshots if applicable

### 4. PR Review Process

- **Automated Checks:** GitHub Actions will run tests automatically
- **Code Review:** Maintainers will review your code
- **Feedback:** Address any requested changes
- **Approval:** Once approved, your PR will be merged

### PR Best Practices

- ✅ Keep PRs focused and small
- ✅ Write clear PR descriptions
- ✅ Include tests for new code
- ✅ Update documentation
- ✅ Respond to review comments
- ✅ Ensure CI tests pass
- ❌ Don't include unrelated changes
- ❌ Don't mix multiple features in one PR

## 🔒 Security Guidelines

### Responsible Disclosure

**For Security Vulnerabilities:**

1. **DO NOT** create a public issue
2. **USE** GitHub's Security Advisory feature:
   - Go to Security tab
   - Click "Report a vulnerability"
   - Provide details privately

3. **READ** [SECURITY.md](SECURITY.md) for full guidelines

### Security Considerations

When contributing:

- Never hardcode credentials or secrets
- Use secure communication protocols (TLS)
- Follow Android security best practices
- Validate and sanitize all inputs
- Handle permissions appropriately
- Consider privacy implications
- Document security features

### Educational Purpose Notice

**Important:** This project is for educational and research purposes only. Contributors must:

- Not use for illegal activities
- Not assist in malicious deployments
- Respect privacy and legal boundaries
- Focus on security research and education
- Follow responsible disclosure practices

## 🎯 Areas Looking for Contributors

### High Priority

- [ ] Enhanced screenshot capabilities
- [ ] Real-time screen sharing improvements
- [ ] Advanced notification monitoring
- [ ] Plugin architecture development
- [ ] Android 16 feature support
- [ ] Performance optimizations

### Documentation

- [ ] Video tutorials
- [ ] More code examples
- [ ] API documentation
- [ ] Translation to other languages

### Testing

- [ ] Increased test coverage
- [ ] More Android device testing
- [ ] Automated UI testing
- [ ] Performance benchmarking

## 📞 Getting Help

### Resources

- **Documentation:** [docs/](docs/) folder
- **Issues:** [GitHub Issues](https://github.com/shadow-dragon-2002/AndroRAT/issues)
- **Discussions:** [GitHub Discussions](https://github.com/shadow-dragon-2002/AndroRAT/discussions)
- **Twitter:** [@karma9874](https://twitter.com/karma9874)

### Questions?

- Check existing documentation first
- Search closed issues
- Ask in GitHub Discussions
- Open a new issue with the "question" label

## 🏆 Recognition

Contributors will be recognized:

- In the project README
- In release notes
- As GitHub contributors
- In the commit history

Thank you for contributing to AndroRAT! Your efforts help make this educational tool better for the entire community.

---

**Remember:** This is an educational project. Always use responsibly and ethically. Never use for malicious purposes or illegal activities.
