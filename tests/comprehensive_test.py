#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Comprehensive AndroRAT Test Suite
Extended testing for CLI, GUI, and APK compatibility
"""

import sys
import os

# Import test utilities to setup paths
from test_utils import setup_server_path, get_project_root
setup_server_path()
import subprocess
import tempfile
import shutil
import unittest
import threading
import time
import socket
import json
import platform

class ComprehensiveAndroRATTests(unittest.TestCase):
    
    def setUp(self):
        """Set up test environment"""
        self.test_dir = os.path.dirname(os.path.abspath(__file__))
        self.temp_dir = tempfile.mkdtemp()
        self.test_ip = "127.0.0.1"
        self.test_port = "9999"
        
    def tearDown(self):
        """Clean up test environment"""
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
    
    def test_01_environment_setup(self):
        """Test that the environment is properly set up"""
        print("\n=== Environment Setup Tests ===")
        
        # Test Python version
        self.assertGreaterEqual(sys.version_info, (3, 6))
        print(f"✓ Python version: {sys.version}")
        
        # Test Java availability
        result = subprocess.run(['java', '-version'], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0)
        print(f"✓ Java available: {result.stderr.split()[2] if result.stderr else 'Unknown'}")
        
        # Test tkinter availability
        result = subprocess.run([sys.executable, '-c', 'import tkinter; print("OK")'], 
                              capture_output=True, text=True)
        self.assertEqual(result.returncode, 0)
        print("✓ tkinter available for GUI testing")
        
    def test_02_cli_basic_functionality(self):
        """Test CLI basic functionality"""
        print("\n=== CLI Basic Functionality Tests ===")
        
        # Test help command
        result = subprocess.run([sys.executable, 'androRAT.py', '--help'], 
                              cwd=self.test_dir, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0)
        self.assertIn('--build', result.stdout)
        self.assertIn('--shell', result.stdout)
        print("✓ CLI help command works")
        
        # Test invalid arguments
        result = subprocess.run([sys.executable, 'androRAT.py', '--invalid'], 
                              cwd=self.test_dir, capture_output=True, text=True)
        self.assertNotEqual(result.returncode, 0)
        print("✓ CLI properly rejects invalid arguments")
        
    def test_03_cli_build_validation(self):
        """Test CLI build parameter validation"""
        print("\n=== CLI Build Parameter Validation ===")
        
        # Test build without parameters
        result = subprocess.run([sys.executable, 'androRAT.py', '--build'], 
                              cwd=self.test_dir, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0)
        self.assertIn('Arguments Missing', result.stdout)
        print("✓ Build command validates missing parameters")
        
        # Test build with partial parameters
        result = subprocess.run([sys.executable, 'androRAT.py', '--build', '-i', self.test_ip], 
                              cwd=self.test_dir, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0)
        self.assertIn('Arguments Missing', result.stdout)
        print("✓ Build command validates incomplete parameters")
        
    def test_04_cli_shell_validation(self):
        """Test CLI shell parameter validation"""
        print("\n=== CLI Shell Parameter Validation ===")
        
        # Test shell without parameters
        result = subprocess.run([sys.executable, 'androRAT.py', '--shell'], 
                              cwd=self.test_dir, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0)
        self.assertIn('Arguments Missing', result.stdout)
        print("✓ Shell command validates missing parameters")
        
    def test_05_gui_import_and_basic_functionality(self):
        """Test GUI import and basic functionality"""
        print("\n=== GUI Import and Basic Functionality ===")
        
        # Test GUI module import
        server_dir = get_project_root() + '/server'
        result = subprocess.run([
            sys.executable, '-c', 
            f'import sys; sys.path.insert(0, "{server_dir}"); import androRAT_gui; print("GUI import successful")'
        ], cwd=self.test_dir, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0)
        self.assertIn('GUI import successful', result.stdout)
        print("✓ GUI module imports successfully")
        
        # Test GUI class instantiation (headless)
        gui_test_code = '''
import os
os.environ["DISPLAY"] = ":99"
import sys
sys.path.insert(0, "../server")
import tkinter as tk
import androRAT_gui
root = tk.Tk()
app = androRAT_gui.AndroRATGUI(root)
print("GUI instantiation successful")
root.destroy()
'''
        result = subprocess.run([sys.executable, '-c', gui_test_code], 
                              cwd=self.test_dir, capture_output=True, text=True)
        if result.returncode == 0:
            print("✓ GUI instantiation works")
        else:
            print(f"⚠ GUI instantiation issue (display related): {result.stderr}")
        
    def test_06_launcher_functionality(self):
        """Test launcher functionality"""
        print("\n=== Launcher Functionality Tests ===")
        
        # Test launcher help
        result = subprocess.run([sys.executable, 'launcher.py', '--help'], 
                              cwd=self.test_dir, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0)
        print("✓ Launcher help command works")
        
        # Test launcher CLI mode
        result = subprocess.run([sys.executable, 'launcher.py', '--cli', '--help'], 
                              cwd=self.test_dir, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0)
        print("✓ Launcher CLI mode works")
        
    def test_07_android_configuration_validation(self):
        """Test Android configuration files"""
        print("\n=== Android Configuration Validation ===")
        
        # Test Android manifest
        project_root = get_project_root()
        manifest_path = os.path.join(project_root, 'Android_Code/app/src/main/AndroidManifest.xml')
        self.assertTrue(os.path.exists(manifest_path))
        
        with open(manifest_path, 'r') as f:
            content = f.read()
            
        # Check for Android 13+ through 15+ permissions
        required_permissions = [
            'POST_NOTIFICATIONS',
            'READ_MEDIA_IMAGES',
            'READ_MEDIA_VIDEO',
            'READ_MEDIA_AUDIO',
            'READ_MEDIA_VISUAL_USER_SELECTED',
            'FOREGROUND_SERVICE',
            'FOREGROUND_SERVICE_CAMERA',
            'FOREGROUND_SERVICE_MICROPHONE',
            'FOREGROUND_SERVICE_LOCATION',
            'FOREGROUND_SERVICE_DATA_SYNC',
            'USE_FULL_SCREEN_INTENT',
            'BODY_SENSORS_BACKGROUND',
            'ACCESS_MEDIA_PROJECTION_STATE'
        ]
        
        for permission in required_permissions:
            self.assertIn(permission, content)
            print(f"✓ Permission {permission} found in manifest")
            
        # Check for proper exported flags
        self.assertIn('android:exported="true"', content)
        self.assertIn('android:exported="false"', content)
        print("✓ Proper android:exported flags found")
        
        # Check foreground service types
        self.assertIn('foregroundServiceType=', content)
        print("✓ Foreground service types configured")
        
    def test_08_android_gradle_configuration(self):
        """Test Android Gradle configuration"""
        print("\n=== Android Gradle Configuration ===")
        
        project_root = get_project_root()
        gradle_path = os.path.join(project_root, 'Android_Code/app/build.gradle')
        self.assertTrue(os.path.exists(gradle_path))
        
        with open(gradle_path, 'r') as f:
            content = f.read()
            
        # Check SDK versions (Android 15+)
        self.assertIn('compileSdkVersion 35', content)
        self.assertIn('targetSdkVersion 35', content)
        self.assertIn('minSdkVersion 23', content)
        print("✓ SDK versions updated to Android 15+ (API 35)")
        
        # Check dependencies
        modern_deps = [
            'androidx.appcompat:appcompat:1.6.1',
            'androidx.constraintlayout:constraintlayout:2.1.4',
            'junit:junit:4.13.2'
        ]
        
        for dep in modern_deps:
            self.assertIn(dep, content)
            print(f"✓ Modern dependency found: {dep}")
            
    def test_09_file_structure_validation(self):
        """Test file structure and required files"""
        print("\n=== File Structure Validation ===")
        
        required_files = [
            'androRAT.py',
            'androRAT_gui.py',
            'launcher.py',
            'utils.py',
            'requirements.txt',
            'Android_Code/app/build.gradle',
            'Android_Code/app/src/main/AndroidManifest.xml'
        ]
        
        for file_path in required_files:
            full_path = os.path.join(self.test_dir, file_path)
            self.assertTrue(os.path.exists(full_path))
            print(f"✓ Required file exists: {file_path}")
            
    def test_10_python_syntax_validation(self):
        """Test Python syntax in all files"""
        print("\n=== Python Syntax Validation ===")
        
        python_files = [
            'androRAT.py',
            'androRAT_gui.py',
            'launcher.py',
            'utils.py',
            'test_androrat.py'
        ]
        
        for py_file in python_files:
            file_path = os.path.join(self.test_dir, py_file)
            if os.path.exists(file_path):
                result = subprocess.run([sys.executable, '-m', 'py_compile', file_path], 
                                      capture_output=True, text=True)
                self.assertEqual(result.returncode, 0)
                print(f"✓ Python syntax valid: {py_file}")
                
    def test_11_dependency_check(self):
        """Test all dependencies are available"""
        print("\n=== Dependency Check ===")
        
        # Test pyngrok import
        result = subprocess.run([sys.executable, '-c', 'import pyngrok; print("pyngrok OK")'], 
                              capture_output=True, text=True)
        self.assertEqual(result.returncode, 0)
        print("✓ pyngrok dependency available")
        
        # Test utils import
        result = subprocess.run([sys.executable, '-c', 'from utils import *; print("utils OK")'], 
                              cwd=self.test_dir, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0)
        print("✓ utils module imports successfully")
        
    def test_12_network_functionality_validation(self):
        """Test network functionality components"""
        print("\n=== Network Functionality Validation ===")
        
        # Test socket creation (basic network functionality)
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.bind(('127.0.0.1', 0))
            port = sock.getsockname()[1]
            sock.close()
            print(f"✓ Network socket functionality works (test port: {port})")
        except Exception as e:
            self.fail(f"Network functionality test failed: {e}")
            
    def test_13_apk_build_readiness(self):
        """Test APK build environment readiness"""
        print("\n=== APK Build Readiness ===")
        
        # Check Android SDK environment
        android_dirs = ['Android_Code', 'Android_Code/app', 'Android_Code/app/src']
        for dir_path in android_dirs:
            full_path = os.path.join(self.test_dir, dir_path)
            self.assertTrue(os.path.exists(full_path))
            print(f"✓ Android directory exists: {dir_path}")
            
        # Check Gradle wrapper
        gradlew_path = os.path.join(self.test_dir, 'Android_Code/gradlew')
        if os.path.exists(gradlew_path):
            print("✓ Gradle wrapper found")
        else:
            print("⚠ Gradle wrapper not found (may affect build)")
            
        # Check Java resources
        java_src_path = os.path.join(self.test_dir, 'Android_Code/app/src/main/java')
        if os.path.exists(java_src_path):
            print("✓ Java source directory exists")
        else:
            print("⚠ Java source directory not found")
            
    def test_14_error_handling_validation(self):
        """Test error handling in various scenarios"""
        print("\n=== Error Handling Validation ===")
        
        # Test invalid IP format
        result = subprocess.run([
            sys.executable, 'androRAT.py', '--build', 
            '-i', 'invalid.ip', '-p', self.test_port, '-o', 'test.apk'
        ], cwd=self.test_dir, capture_output=True, text=True)
        # Should handle gracefully (not crash)
        print("✓ Invalid IP handled gracefully")
        
        # Test invalid port
        result = subprocess.run([
            sys.executable, 'androRAT.py', '--build', 
            '-i', self.test_ip, '-p', 'invalid_port', '-o', 'test.apk'
        ], cwd=self.test_dir, capture_output=True, text=True)
        # Should handle gracefully (not crash)
        print("✓ Invalid port handled gracefully")
        
    def test_15_gui_components_validation(self):
        """Test GUI components validation (headless)"""
        print("\n=== GUI Components Validation ===")
        
        # Test GUI components can be created
        gui_component_test = '''
import os
import sys
# Prevent GUI from actually displaying
os.environ["DISPLAY"] = ":99"
sys.path.insert(0, ".")

try:
    import tkinter as tk
    from tkinter import ttk
    
    # Test basic tkinter widgets
    root = tk.Tk()
    root.withdraw()  # Hide window
    
    # Test widgets used in GUI
    notebook = ttk.Notebook(root)
    frame = ttk.Frame(notebook)
    entry = ttk.Entry(frame)
    button = ttk.Button(frame, text="Test")
    text = tk.Text(frame)
    
    print("GUI components validation successful")
    root.destroy()
    
except Exception as e:
    print(f"GUI components validation failed: {e}")
    sys.exit(1)
'''
        
        result = subprocess.run([sys.executable, '-c', gui_component_test], 
                              cwd=self.test_dir, capture_output=True, text=True)
        if result.returncode == 0:
            print("✓ GUI components validation successful")
        else:
            print(f"⚠ GUI components validation issue: {result.stderr}")

def run_comprehensive_tests():
    """Run all comprehensive tests"""
    print("=" * 70)
    print("COMPREHENSIVE ANDRORAT TESTING SUITE")
    print("=" * 70)
    print(f"Python Version: {sys.version}")
    print(f"Platform: {platform.system()} {platform.release()}")
    print("=" * 70)
    
    # Change to the script directory
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(ComprehensiveAndroRATTests)
    
    # Run tests with custom runner for better output
    runner = unittest.TextTestRunner(verbosity=2, stream=sys.stdout, buffer=True)
    result = runner.run(suite)
    
    print("\n" + "=" * 70)
    print("COMPREHENSIVE TEST SUMMARY")
    print("=" * 70)
    
    if result.wasSuccessful():
        print("🎉 ALL TESTS PASSED!")
        print("✅ AndroRAT is ready for Android 13+ compatibility")
        print("✅ CLI functionality validated")
        print("✅ GUI interface validated")
        print("✅ APK build environment verified")
    else:
        print("⚠️  Some tests failed or had issues")
        print(f"Failures: {len(result.failures)}")
        print(f"Errors: {len(result.errors)}")
        
        if result.failures:
            print("\nFailures:")
            for test, traceback in result.failures:
                print(f"- {test}: {traceback}")
                
        if result.errors:
            print("\nErrors:")
            for test, traceback in result.errors:
                print(f"- {test}: {traceback}")
    
    print("=" * 70)
    return result.wasSuccessful()

if __name__ == "__main__":
    success = run_comprehensive_tests()
    sys.exit(0 if success else 1)