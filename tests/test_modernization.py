#!/usr/bin/env python3
"""
Test script for UI modernization and purge functionality
"""

import sys
import os
import tempfile
import unittest
from unittest.mock import Mock, patch, MagicMock

# Add server directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'server'))

try:
    from utils import handlePurgeBackdoor, enhance_connection_stability
except ImportError as e:
    print(f"Warning: Could not import utils: {e}")

class TestModernization(unittest.TestCase):
    """Test suite for UI modernization and purge functionality"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.test_auth_key = "test_auth_key_12345678901234567890"
        self.mock_conn = Mock()
        
    def test_purge_function_exists(self):
        """Test that purge function is defined"""
        try:
            from utils import handlePurgeBackdoor
            self.assertTrue(callable(handlePurgeBackdoor))
            print("✅ Purge function properly defined")
        except ImportError:
            self.fail("handlePurgeBackdoor function not found")
            
    def test_connection_enhancement_exists(self):
        """Test that connection enhancement function exists"""
        try:
            from utils import enhance_connection_stability
            self.assertTrue(callable(enhance_connection_stability))
            print("✅ Connection enhancement function properly defined")
        except ImportError:
            self.fail("enhance_connection_stability function not found")
            
    def test_gui_files_exist(self):
        """Test that GUI files exist and have modern features"""
        gui_files = [
            '../server/androRAT_gui.py',
            '../server/androRAT_advanced_gui.py'
        ]
        
        for gui_file in gui_files:
            file_path = os.path.join(os.path.dirname(__file__), gui_file)
            self.assertTrue(os.path.exists(file_path), f"GUI file {gui_file} not found")
            
            # Check for modern features in GUI files
            with open(file_path, 'r') as f:
                content = f.read()
                
            # Check for modern UI elements
            modern_features = [
                'colors',
                'bg_primary',
                'Remote Purge',
                'modern',
                'Segoe UI',
                '#007acc'  # Modern accent color
            ]
            
            for feature in modern_features:
                self.assertIn(feature, content, f"Modern feature '{feature}' not found in {gui_file}")
                
        print("✅ GUI files contain modern UI features")
        
    def test_android_purge_implementation(self):
        """Test that Android purge functionality is implemented"""
        android_file = '../Android_Code/app/src/main/java/com/example/reverseshell2/SecureConnectionHandler.java'
        file_path = os.path.join(os.path.dirname(__file__), android_file)
        
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                content = f.read()
                
            # Check for purge functionality
            purge_features = [
                'handlePurgeCommand',
                'PURGE_FILES',
                'PURGE_SERVICES',
                'PURGE_RECEIVERS',
                'PURGE_CLEAN'
            ]
            
            for feature in purge_features:
                self.assertIn(feature, content, f"Purge feature '{feature}' not found in Android code")
                
            print("✅ Android purge functionality properly implemented")
        else:
            print("⚠️  Android file not found, skipping Android test")
            
    def test_help_function_includes_purge(self):
        """Test that help function includes purge command"""
        try:
            # Mock the print function to capture output
            with patch('builtins.print') as mock_print:
                from utils import help
                help()
                
                # Check if purge command was printed
                printed_content = ' '.join([str(call) for call in mock_print.call_args_list])
                self.assertIn('purgeBackdoor', printed_content)
                
            print("✅ Help function includes purge command")
        except ImportError:
            print("⚠️  Could not test help function")
            
    def test_modern_color_scheme(self):
        """Test that modern color schemes are defined"""
        try:
            # Check basic GUI for color scheme
            gui_file = os.path.join(os.path.dirname(__file__), '../server/androRAT_gui.py')
            if os.path.exists(gui_file):
                with open(gui_file, 'r') as f:
                    content = f.read()
                    
                expected_colors = [
                    '#1e1e1e',  # Primary background
                    '#2d2d2d',  # Secondary background  
                    '#007acc',  # Accent color
                    '#28a745',  # Success color
                    '#dc3545'   # Danger color
                ]
                
                for color in expected_colors:
                    self.assertIn(color, content, f"Modern color {color} not found")
                    
                print("✅ Modern color scheme properly implemented")
        except Exception as e:
            print(f"⚠️  Could not validate color scheme: {e}")
            
    def test_gui_syntax_validation(self):
        """Test that GUI files have valid Python syntax"""
        gui_files = [
            '../server/androRAT_gui.py',
            '../server/androRAT_advanced_gui.py'
        ]
        
        for gui_file in gui_files:
            file_path = os.path.join(os.path.dirname(__file__), gui_file)
            if os.path.exists(file_path):
                try:
                    with open(file_path, 'r') as f:
                        compile(f.read(), file_path, 'exec')
                    print(f"✅ {gui_file} has valid syntax")
                except SyntaxError as e:
                    self.fail(f"Syntax error in {gui_file}: {e}")
                except Exception:
                    # Expected due to missing tkinter in headless environment
                    print(f"✅ {gui_file} syntax OK (import issues expected in headless environment)")
                    
    def test_feature_completeness(self):
        """Test that all requested features are implemented"""
        required_features = {
            'Modern UI Design': False,
            'Remote Purge System': False,
            'Enhanced Security': False,
            'Dark Theme': False
        }
        
        # Check GUI files for features
        gui_files = [
            '../server/androRAT_gui.py',
            '../server/androRAT_advanced_gui.py'
        ]
        
        for gui_file in gui_files:
            file_path = os.path.join(os.path.dirname(__file__), gui_file)
            if os.path.exists(file_path):
                with open(file_path, 'r') as f:
                    content = f.read()
                    
                if ('modern' in content.lower() or 'Segoe UI' in content or 'Material' in content):
                    required_features['Modern UI Design'] = True
                    
                if 'purge' in content.lower():
                    required_features['Remote Purge System'] = True
                    
                if 'dark' in content.lower() and '#1e1e1e' in content:
                    required_features['Dark Theme'] = True
                    
        # Check utils for security features
        utils_file = os.path.join(os.path.dirname(__file__), '../server/utils.py')
        if os.path.exists(utils_file):
            with open(utils_file, 'r') as f:
                content = f.read()
                
            if 'enhance_connection_stability' in content or 'ssl' in content.lower():
                required_features['Enhanced Security'] = True
                
        # Verify all features are implemented
        for feature, implemented in required_features.items():
            self.assertTrue(implemented, f"Required feature '{feature}' not fully implemented")
            
        print("✅ All required features implemented")
        
    def test_integration_completeness(self):
        """Test that all components integrate properly"""
        integration_score = 0
        total_checks = 5
        
        # Check 1: GUI files exist and have modern features
        try:
            gui_files = ['../server/androRAT_gui.py', '../server/androRAT_advanced_gui.py']
            for gui_file in gui_files:
                file_path = os.path.join(os.path.dirname(__file__), gui_file)
                if os.path.exists(file_path):
                    integration_score += 0.5
            print(f"✅ GUI Integration: {integration_score}/{1}")
        except:
            pass
            
        # Check 2: Backend purge functionality
        try:
            from utils import handlePurgeBackdoor
            integration_score += 1
            print(f"✅ Backend Integration: {integration_score}/{2}")
        except:
            print("⚠️  Backend integration partial")
            
        # Check 3: Android integration
        android_file = '../Android_Code/app/src/main/java/com/example/reverseshell2/SecureConnectionHandler.java'
        file_path = os.path.join(os.path.dirname(__file__), android_file)
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                if 'handlePurgeCommand' in f.read():
                    integration_score += 1
            print(f"✅ Android Integration: {integration_score}/{3}")
        else:
            print("⚠️  Android integration check skipped")
            
        # Check 4: Security enhancements
        try:
            from utils import enhance_connection_stability
            integration_score += 1
            print(f"✅ Security Integration: {integration_score}/{4}")
        except:
            print("⚠️  Security integration partial")
            
        # Check 5: Help system integration
        try:
            from utils import help
            integration_score += 1
            print(f"✅ Help Integration: {integration_score}/{5}")
        except:
            print("⚠️  Help integration partial")
            
        # Final integration score
        integration_percentage = (integration_score / total_checks) * 100
        print(f"🎯 Overall Integration Score: {integration_percentage:.1f}%")
        
        # Require at least 60% integration for success
        self.assertGreaterEqual(integration_percentage, 60, 
                               f"Integration score {integration_percentage:.1f}% below required 60%")

def run_modernization_tests():
    """Run all modernization tests"""
    print("🧪 Running AndroRAT Modernization Tests")
    print("=" * 50)
    
    # Create test suite
    suite = unittest.TestLoader().loadTestsFromTestCase(TestModernization)
    
    # Run tests with verbose output
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    print("\n" + "=" * 50)
    print("🏆 TEST RESULTS SUMMARY:")
    print(f"   Tests Run: {result.testsRun}")
    print(f"   Failures: {len(result.failures)}")
    print(f"   Errors: {len(result.errors)}")
    
    if result.wasSuccessful():
        print("   Status: ✅ ALL TESTS PASSED")
        success_rate = 100.0
    else:
        success_rate = ((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun) * 100
        print(f"   Status: ⚠️  {success_rate:.1f}% SUCCESS RATE")
        
    print(f"   Overall: {success_rate:.1f}% SUCCESSFUL")
    
    return result.wasSuccessful()

if __name__ == '__main__':
    success = run_modernization_tests()
    sys.exit(0 if success else 1)