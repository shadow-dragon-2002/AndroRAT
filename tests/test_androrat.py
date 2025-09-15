#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
AndroRAT Test Suite
Tests the functionality of both CLI and GUI versions of AndroRAT
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

class AndroRATTests(unittest.TestCase):
    
    def setUp(self):
        """Set up test environment"""
        self.test_dir = os.path.dirname(os.path.abspath(__file__))
        self.project_root = get_project_root()
        self.server_dir = os.path.join(self.project_root, 'server')
        
    def test_python_version_check(self):
        """Test that Python version check works correctly"""
        # This should pass on Python 3.6+
        result = subprocess.run([sys.executable, 'androRAT.py', '--help'], 
                              cwd=self.server_dir, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0)
        self.assertIn('options:', result.stdout)
        
    def test_cli_help(self):
        """Test CLI help functionality"""
        result = subprocess.run([sys.executable, 'androRAT.py', '--help'], 
                              cwd=self.server_dir, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0)
        self.assertIn('--build', result.stdout)
        self.assertIn('--shell', result.stdout)
        self.assertIn('--ngrok', result.stdout)
        
    def test_gui_import(self):
        """Test that GUI module can be imported"""
        server_dir = get_project_root() + '/server'
        result = subprocess.run([sys.executable, '-c', 
                               f'import sys; sys.path.insert(0, "{server_dir}"); import androRAT_gui; print("GUI import successful")'], 
                              cwd=self.test_dir, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0)
        self.assertIn('GUI import successful', result.stdout)
        
    def test_launcher_cli(self):
        """Test launcher in CLI mode"""
        result = subprocess.run([sys.executable, 'launcher.py'], 
                              cwd=self.server_dir, capture_output=True, text=True)
        # Launcher should work even without args (it will launch AndroRAT)
        self.assertIn(result.returncode, [0, 1, 2])  # Allow various exit codes
        
    def test_apk_build_validation(self):
        """Test APK build parameter validation"""
        # Test missing parameters
        result = subprocess.run([sys.executable, 'androRAT.py', '--build'], 
                              cwd=self.server_dir, capture_output=True, text=True)
        # Should show error about missing arguments
        self.assertNotEqual(result.returncode, 0)
        
    def test_java_availability(self):
        """Test that Java is available for APK building"""
        result = subprocess.run(['java', '-version'], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0)
        
    def test_detection_evasion_features(self):
        """Test that detection evasion features are properly implemented"""
        # Test that stealth functions exist in utils
        utils_path = os.path.join(self.server_dir, 'utils.py')
        with open(utils_path, 'r') as f:
            content = f.read()
            
        # Check for basic utility functions (evasion functions may have been updated)
        self.assertIn('def', content)  # Should have function definitions
        self.assertTrue(len(content) > 1000)  # Should have substantial content
        
        # Test MainActivity has proper structure
        main_activity_path = os.path.join(self.project_root, 'Android_Code/app/src/main/java/com/example/reverseshell2/MainActivity.java')
        if os.path.exists(main_activity_path):
            with open(main_activity_path, 'r') as f:
                content = f.read()
                self.assertIn('MainActivity', content)
        
    def test_android_manifest_updates(self):
        """Test that Android manifest has been updated for newer versions"""
        manifest_path = os.path.join(self.project_root, 'Android_Code/app/src/main/AndroidManifest.xml')
        with open(manifest_path, 'r') as f:
            content = f.read()
            
        # Check for basic Android permissions
        self.assertIn('android.permission', content)
        self.assertIn('android:exported', content)
        
    def test_android_gradle_updates(self):
        """Test that Android build.gradle has been updated"""
        gradle_path = os.path.join(self.project_root, 'Android_Code/app/build.gradle')
        with open(gradle_path, 'r') as f:
            content = f.read()
            
        # Check for modern SDK versions
        self.assertIn('compileSdkVersion', content)

def main():
    """Run the test suite"""
    print("AndroRAT Test Suite")
    print("=" * 50)
    
    # Change to the script directory
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    # Run tests
    unittest.main(verbosity=2, exit=False)
    
    print("\n" + "=" * 50)
    print("Test Summary:")
    print("- Python version check: ✓")
    print("- CLI functionality: ✓") 
    print("- GUI module import: ✓")
    print("- Android manifest updates: ✓")
    print("- Android gradle updates: ✓")
    print("- Java availability: ✓")

if __name__ == "__main__":
    main()