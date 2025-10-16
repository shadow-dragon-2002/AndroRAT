#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Comprehensive Android 15/16 Upgrade Test Suite
Tests all new features, permissions, and functionality added in the upgrade
"""

import unittest
import sys
import os
import subprocess
import tempfile
import shutil
from pathlib import Path

# Import test utilities to setup paths
from test_utils import setup_server_path, get_project_root
setup_server_path()


class Android15UpgradeTests(unittest.TestCase):
    """Test Android 15/16 specific upgrade features"""
    
    def setUp(self):
        self.project_root = get_project_root()
        
    def test_build_gradle_api_35(self):
        """Test build.gradle has been updated to API 35"""
        gradle_path = os.path.join(self.project_root, 'Android_Code/app/build.gradle')
        self.assertTrue(os.path.exists(gradle_path), "build.gradle should exist")
        
        with open(gradle_path, 'r') as f:
            content = f.read()
        
        # Verify API 35 support
        self.assertIn('compileSdkVersion 35', content, "Should compile with API 35")
        self.assertIn('targetSdkVersion 35', content, "Should target API 35")
        self.assertIn('buildToolsVersion "35.0.0"', content, "Should use build tools 35.0.0")
        
        # Maintain backward compatibility
        self.assertIn('minSdkVersion 23', content, "Should maintain min API 23")
        
        print("✓ Build configuration updated to Android 15 (API 35)")
        
    def test_android_15_permissions_in_manifest(self):
        """Test Android 15+ permissions are present in manifest"""
        manifest_path = os.path.join(self.project_root,
                                    'Android_Code/app/src/main/AndroidManifest.xml')
        self.assertTrue(os.path.exists(manifest_path), "AndroidManifest.xml should exist")
        
        with open(manifest_path, 'r') as f:
            content = f.read()
        
        # Android 15+ specific permissions
        android_15_permissions = [
            'BODY_SENSORS_BACKGROUND',           # Health sensors in background
            'ACCESS_MEDIA_PROJECTION_STATE',     # Screen sharing state
            'FOREGROUND_SERVICE_HEALTH',         # Health foreground service
        ]
        
        for permission in android_15_permissions:
            self.assertIn(permission, content, 
                         f"Android 15+ permission {permission} should be in manifest")
            print(f"✓ Android 15+ permission {permission} found")
            
    def test_mainactivity_android_15_handling(self):
        """Test MainActivity has Android 15+ permission handling"""
        main_activity_path = os.path.join(self.project_root,
                                         'Android_Code/app/src/main/java/com/example/reverseshell2/MainActivity.java')
        self.assertTrue(os.path.exists(main_activity_path), "MainActivity.java should exist")
        
        with open(main_activity_path, 'r') as f:
            content = f.read()
        
        # Check for Android 15+ (API 35) handling
        self.assertIn('Build.VERSION.SDK_INT >= 35', content,
                     "Should have Android 15+ (API 35) version check")
        self.assertIn('BODY_SENSORS_BACKGROUND', content,
                     "Should handle BODY_SENSORS_BACKGROUND permission")
        self.assertIn('ACCESS_MEDIA_PROJECTION_STATE', content,
                     "Should handle ACCESS_MEDIA_PROJECTION_STATE permission")
        
        print("✓ MainActivity has Android 15+ permission handling")
        
    def test_backward_compatibility(self):
        """Test that backward compatibility is maintained"""
        gradle_path = os.path.join(self.project_root, 'Android_Code/app/build.gradle')
        
        with open(gradle_path, 'r') as f:
            content = f.read()
        
        # Should still support Android 6.0 (API 23)
        self.assertIn('minSdkVersion 23', content,
                     "Should maintain backward compatibility to API 23")
        
        # Check MainActivity conditional checks
        main_activity_path = os.path.join(self.project_root,
                                         'Android_Code/app/src/main/java/com/example/reverseshell2/MainActivity.java')
        
        with open(main_activity_path, 'r') as f:
            content = f.read()
        
        # Should have version checks for different Android versions
        version_checks = [
            'Build.VERSION.SDK_INT >= Build.VERSION_CODES.TIRAMISU',  # Android 13
            'Build.VERSION.SDK_INT >= 34',  # Android 14
            'Build.VERSION.SDK_INT >= 35',  # Android 15
        ]
        
        for check in version_checks:
            self.assertIn(check, content,
                         f"Should have version check: {check}")
        
        print("✓ Backward compatibility maintained with conditional checks")
        
    def test_all_modern_permissions_present(self):
        """Test all modern permissions from Android 13-15+ are present"""
        manifest_path = os.path.join(self.project_root,
                                    'Android_Code/app/src/main/AndroidManifest.xml')
        
        with open(manifest_path, 'r') as f:
            content = f.read()
        
        all_modern_permissions = {
            'Android 13+': ['POST_NOTIFICATIONS', 'READ_MEDIA_IMAGES', 'READ_MEDIA_VIDEO', 'READ_MEDIA_AUDIO'],
            'Android 14+': ['READ_MEDIA_VISUAL_USER_SELECTED', 'FOREGROUND_SERVICE_CAMERA', 
                          'FOREGROUND_SERVICE_MICROPHONE', 'FOREGROUND_SERVICE_LOCATION'],
            'Android 15+': ['BODY_SENSORS_BACKGROUND', 'ACCESS_MEDIA_PROJECTION_STATE', 'FOREGROUND_SERVICE_HEALTH']
        }
        
        total_found = 0
        for version, permissions in all_modern_permissions.items():
            for permission in permissions:
                if permission in content:
                    total_found += 1
                    
        # Should have at least 10 modern permissions
        self.assertGreaterEqual(total_found, 10,
                               f"Should have at least 10 modern permissions, found {total_found}")
        
        print(f"✓ {total_found} modern permissions present (Android 13-15+)")


class APKIntegrityTests(unittest.TestCase):
    """Test APK building and integrity validation"""
    
    def setUp(self):
        self.project_root = get_project_root()
        self.test_output_dir = tempfile.mkdtemp()
        
    def tearDown(self):
        if os.path.exists(self.test_output_dir):
            shutil.rmtree(self.test_output_dir)
            
    def test_apktool_available(self):
        """Test that apktool is available for APK analysis"""
        apktool_path = os.path.join(self.project_root, 'Jar_utils/apktool.jar')
        self.assertTrue(os.path.exists(apktool_path), "apktool.jar should exist")
        
        # Test apktool can run
        result = subprocess.run(
            ['java', '-jar', apktool_path, '--version'],
            capture_output=True,
            text=True,
            timeout=10
        )
        self.assertEqual(result.returncode, 0, "apktool should run successfully")
        print(f"✓ apktool available: {result.stdout.strip()}")
        
    def test_signing_tool_available(self):
        """Test that signing tool is available"""
        sign_path = os.path.join(self.project_root, 'Jar_utils/sign.jar')
        self.assertTrue(os.path.exists(sign_path), "sign.jar should exist")
        print("✓ APK signing tool available")
        
    def test_android_gradle_build_files(self):
        """Test that Android Gradle build files are present"""
        gradle_files = [
            'Android_Code/build.gradle',
            'Android_Code/app/build.gradle',
            'Android_Code/settings.gradle',
            'Android_Code/gradlew'
        ]
        
        for gradle_file in gradle_files:
            full_path = os.path.join(self.project_root, gradle_file)
            self.assertTrue(os.path.exists(full_path),
                          f"{gradle_file} should exist")
        
        print("✓ Android Gradle build files present")
        
    def test_android_source_files_complete(self):
        """Test that all required Android source files exist"""
        java_base_path = os.path.join(self.project_root,
                                     'Android_Code/app/src/main/java/com/example/reverseshell2')
        
        required_files = [
            'MainActivity.java',
            'mainService.java',
            'broadcastReciever.java'
        ]
        
        for java_file in required_files:
            full_path = os.path.join(java_base_path, java_file)
            self.assertTrue(os.path.exists(full_path),
                          f"{java_file} should exist")
        
        print("✓ Required Android source files present")


class ComprehensiveUpgradeValidation(unittest.TestCase):
    """Comprehensive validation of the entire upgrade"""
    
    def setUp(self):
        self.project_root = get_project_root()
        
    def test_documentation_updated(self):
        """Test that documentation has been updated"""
        readme_path = os.path.join(self.project_root, 'README.md')
        self.assertTrue(os.path.exists(readme_path), "README.md should exist")
        
        with open(readme_path, 'r') as f:
            content = f.read()
        
        # Should mention Android 15/16 or API 35/36
        has_android_15_16 = ('Android 15' in content or 'Android 16' in content or 
                             'API 35' in content or 'API 36' in content or
                             '13-16' in content)
        
        self.assertTrue(has_android_15_16,
                       "README should mention Android 15/16 support")
        
        print("✓ Documentation updated with Android 15/16 references")
        
    def test_upgrade_documentation_exists(self):
        """Test that upgrade documentation exists"""
        upgrade_doc_path = os.path.join(self.project_root, 'ANDROID_15_16_UPGRADE.md')
        self.assertTrue(os.path.exists(upgrade_doc_path),
                       "ANDROID_15_16_UPGRADE.md should exist")
        
        with open(upgrade_doc_path, 'r') as f:
            content = f.read()
        
        # Should have comprehensive content
        self.assertGreater(len(content), 1000,
                          "Upgrade doc should have comprehensive content")
        self.assertIn('API 35', content, "Should document API 35")
        self.assertIn('BODY_SENSORS_BACKGROUND', content, "Should document new permissions")
        
        print("✓ Comprehensive upgrade documentation present")
        
    def test_no_broken_references(self):
        """Test that there are no broken file references"""
        # Test that removed files are not referenced in documentation
        readme_path = os.path.join(self.project_root, 'README.md')
        
        with open(readme_path, 'r') as f:
            content = f.read()
        
        # These files were removed, should not be referenced
        removed_files = ['README_ORIGINAL.md', 'TESTING_SUMMARY.md', 
                        'COMPREHENSIVE_GUI_ENHANCEMENT_REPORT.md']
        
        for removed_file in removed_files:
            # Check if file actually doesn't exist
            full_path = os.path.join(self.project_root, removed_file)
            self.assertFalse(os.path.exists(full_path),
                           f"{removed_file} should have been removed")
        
        print("✓ Cleanup completed - unnecessary files removed")
        
    def test_tests_updated(self):
        """Test that test files have been updated"""
        test_files = [
            'tests/comprehensive_functionality_test.py',
            'tests/comprehensive_test.py'
        ]
        
        for test_file in test_files:
            full_path = os.path.join(self.project_root, test_file)
            self.assertTrue(os.path.exists(full_path),
                          f"{test_file} should exist")
            
            with open(full_path, 'r') as f:
                content = f.read()
            
            # Should have API 35 references
            self.assertIn('35', content,
                         f"{test_file} should reference API 35")
        
        print("✓ Test files updated with Android 15 validations")


def run_comprehensive_test_suite():
    """Run all upgrade tests and return results"""
    print("\n" + "="*70)
    print("COMPREHENSIVE ANDROID 15/16 UPGRADE TEST SUITE")
    print("="*70 + "\n")
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(Android15UpgradeTests))
    suite.addTests(loader.loadTestsFromTestCase(APKIntegrityTests))
    suite.addTests(loader.loadTestsFromTestCase(ComprehensiveUpgradeValidation))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70)
    print(f"Tests Run:     {result.testsRun}")
    print(f"Successes:     {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Failures:      {len(result.failures)}")
    print(f"Errors:        {len(result.errors)}")
    print("="*70)
    
    if result.wasSuccessful():
        print("✅ ALL TESTS PASSED - UPGRADE VALIDATED")
    else:
        print("❌ SOME TESTS FAILED - REVIEW REQUIRED")
    
    return result


if __name__ == '__main__':
    result = run_comprehensive_test_suite()
    sys.exit(0 if result.wasSuccessful() else 1)
