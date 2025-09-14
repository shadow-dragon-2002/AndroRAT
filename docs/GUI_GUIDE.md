# AndroRAT GUI User Guide

## Overview
The AndroRAT GUI provides a user-friendly interface for building Android APKs and managing device connections. It offers the same functionality as the CLI version but with an intuitive graphical interface.

## Getting Started

### Launch the GUI
```bash
python3 androRAT_gui.py
```
or
```bash
python3 launcher.py --gui
```

### Prerequisites
- Python 3.6 or higher
- tkinter (usually included with Python)
- Java (for APK building)
- All dependencies from requirements.txt

### Installation
```bash
sudo apt-get install python3-tk  # On Ubuntu/Debian
pip install -r requirements.txt
```

## Features

### 1. APK Building Tab
- **Connection Settings**: Configure IP, port, and ngrok options
- **Output Settings**: Set APK filename and icon visibility
- **Build Progress**: Real-time progress indication
- **Validation**: Automatic input validation

#### Building an APK
1. Open the "Build APK" tab
2. Choose connection method:
   - **Manual**: Enter IP address and port
   - **Ngrok**: Check "Use Ngrok tunnel" for automatic configuration
3. Set output filename (default: karma.apk)
4. Choose icon visibility option
5. Click "Build APK"
6. Monitor progress in the progress bar and logs

### 2. Shell Connection Tab
- **Listener Configuration**: Set IP and port for incoming connections
- **Connection Management**: Start/stop listeners
- **Future Enhancement**: Full shell interface (currently redirects to CLI)

#### Starting a Listener
1. Open the "Shell Connection" tab
2. Enter listen IP (default: 0.0.0.0)
3. Enter port (default: 8000)
4. Click "Start Listener" for connection instructions

### 3. Logs Tab
- **Activity Monitoring**: Real-time activity logs
- **Status Tracking**: Build progress and errors
- **Log Management**: Clear and save log functionality

#### Managing Logs
- **View**: All activities are automatically logged
- **Clear**: Use "Clear Logs" button to reset
- **Save**: Export logs to text file

## CLI Integration
The GUI is designed to work alongside the existing CLI:
- All CLI functionality remains available
- GUI uses the same underlying functions
- Seamless switching between modes

## Advanced Usage

### Configuration Files
- GUI settings are preserved during the session
- APK building uses the same configuration as CLI
- Build output compatible with CLI-generated APKs

### Error Handling
- Input validation prevents common mistakes
- Clear error messages for troubleshooting
- Automatic recovery from temporary failures

### Batch Operations
- Queue multiple APK builds
- Monitor all operations in logs tab
- Export logs for analysis

## Troubleshooting

### Common Issues

#### "tkinter not found"
```bash
sudo apt-get install python3-tk
```

#### "Java not found"
```bash
sudo apt-get install openjdk-11-jdk
```

#### GUI doesn't start
- Check Python version (3.6+ required)
- Ensure DISPLAY variable is set (Linux)
- Try running from terminal for error messages

#### Build failures
- Verify Java installation
- Check IP/port format
- Ensure write permissions in directory

### Getting Help
- Check the Logs tab for detailed error messages
- Use the CLI version for debugging: `python3 androRAT.py --help`
- Run the test suite: `python3 test_androrat.py`

## Security Notes
- Use ngrok for remote testing only
- Never expose listeners to public internet
- Test APKs in isolated environments
- Follow responsible disclosure practices

## Future Enhancements
- Integrated shell interface
- Device management dashboard
- Batch operations
- Configuration profiles
- Advanced logging and analytics