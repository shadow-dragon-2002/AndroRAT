#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
APK Integrity Checker
Validates APK structure, permissions, and build integrity
"""

import os
import sys
import subprocess
import tempfile
import shutil
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path

# Import test utilities
from test_utils import setup_server_path, get_project_root
setup_server_path()


class APKIntegrityChecker:
    """Check APK file integrity and structure"""
    
    def __init__(self, apk_path):
        """Initialize checker with APK path"""
        self.apk_path = apk_path
        self.project_root = get_project_root()
        self.apktool_path = os.path.join(self.project_root, 'Jar_utils/apktool.jar')
        self.results = {
            'valid': True,
            'errors': [],
            'warnings': [],
            'checks': []
        }
        
    def check_apk_exists(self):
        """Check if APK file exists"""
        if not os.path.exists(self.apk_path):
            self.results['valid'] = False
            self.results['errors'].append(f"APK file not found: {self.apk_path}")
            return False
        
        self.results['checks'].append("✓ APK file exists")
        return True
        
    def check_apk_is_zip(self):
        """Check if APK is a valid ZIP archive"""
        try:
            with zipfile.ZipFile(self.apk_path, 'r') as zip_ref:
                file_list = zip_ref.namelist()
                
            # APK should have certain files
            required_files = ['AndroidManifest.xml', 'classes.dex', 'resources.arsc']
            missing_files = []
            
            for req_file in required_files:
                if req_file not in file_list:
                    missing_files.append(req_file)
            
            if missing_files:
                self.results['warnings'].append(f"Missing typical APK files: {missing_files}")
            
            self.results['checks'].append(f"✓ APK is valid ZIP with {len(file_list)} files")
            return True
            
        except zipfile.BadZipFile:
            self.results['valid'] = False
            self.results['errors'].append("APK is not a valid ZIP archive")
            return False
        except Exception as e:
            self.results['errors'].append(f"Error checking ZIP: {str(e)}")
            return False
            
    def check_apk_signature(self):
        """Check if APK is signed"""
        try:
            with zipfile.ZipFile(self.apk_path, 'r') as zip_ref:
                file_list = zip_ref.namelist()
                
            # Check for signature files
            signature_dirs = ['META-INF/CERT.RSA', 'META-INF/CERT.SF', 'META-INF/MANIFEST.MF']
            has_v1_signature = any(sig in file_list for sig in signature_dirs)
            
            # Check for v2/v3 signature (APK Signature Scheme v2/v3)
            # These are in a special APK Signing Block, not visible in ZIP entries
            
            if has_v1_signature:
                self.results['checks'].append("✓ APK has v1 signature (JAR signing)")
            else:
                self.results['warnings'].append("APK may not be signed with v1 signature")
            
            return True
            
        except Exception as e:
            self.results['errors'].append(f"Error checking signature: {str(e)}")
            return False
            
    def decompile_and_check_manifest(self):
        """Decompile APK and check manifest for Android 15+ features"""
        if not os.path.exists(self.apktool_path):
            self.results['warnings'].append("apktool not available - skipping detailed checks")
            return False
            
        temp_dir = tempfile.mkdtemp()
        
        try:
            # Decompile APK
            result = subprocess.run(
                ['java', '-jar', self.apktool_path, 'd', self.apk_path, '-o', temp_dir, '-f'],
                capture_output=True,
                text=True,
                timeout=60
            )
            
            if result.returncode != 0:
                self.results['warnings'].append(f"Could not decompile APK: {result.stderr}")
                return False
            
            # Check AndroidManifest.xml
            manifest_path = os.path.join(temp_dir, 'AndroidManifest.xml')
            if not os.path.exists(manifest_path):
                self.results['errors'].append("Decompiled APK missing AndroidManifest.xml")
                return False
            
            # Parse manifest
            tree = ET.parse(manifest_path)
            root = tree.getroot()
            
            # Extract namespace
            ns = {'android': 'http://schemas.android.com/apk/res/android'}
            
            # Check SDK versions
            uses_sdk = root.find('.//uses-sdk')
            if uses_sdk is not None:
                min_sdk = uses_sdk.get('{http://schemas.android.com/apk/res/android}minSdkVersion', 'unknown')
                target_sdk = uses_sdk.get('{http://schemas.android.com/apk/res/android}targetSdkVersion', 'unknown')
                
                self.results['checks'].append(f"✓ minSdkVersion: {min_sdk}, targetSdkVersion: {target_sdk}")
                
                # Check if targeting Android 15+
                try:
                    target_sdk_int = int(target_sdk) if target_sdk.isdigit() else 0
                    if target_sdk_int >= 35:
                        self.results['checks'].append("✓ Targeting Android 15+ (API 35+)")
                    elif target_sdk_int >= 34:
                        self.results['warnings'].append("Targeting Android 14 - upgrade to 15+ recommended")
                except ValueError:
                    pass
            
            # Check permissions
            permissions = root.findall('.//uses-permission')
            permission_names = []
            
            for perm in permissions:
                perm_name = perm.get('{http://schemas.android.com/apk/res/android}name', '')
                if perm_name:
                    # Extract just the permission name without package
                    perm_short = perm_name.split('.')[-1] if '.' in perm_name else perm_name
                    permission_names.append(perm_short)
            
            self.results['checks'].append(f"✓ Found {len(permission_names)} permissions")
            
            # Check for Android 15+ permissions
            android_15_perms = ['BODY_SENSORS_BACKGROUND', 'ACCESS_MEDIA_PROJECTION_STATE']
            found_android_15 = [p for p in android_15_perms if p in permission_names]
            
            if found_android_15:
                self.results['checks'].append(f"✓ Android 15+ permissions found: {found_android_15}")
            
            # Check for modern foreground service types
            services = root.findall('.//service')
            for service in services:
                fg_type = service.get('{http://schemas.android.com/apk/res/android}foregroundServiceType', '')
                if fg_type:
                    self.results['checks'].append(f"✓ Foreground service type: {fg_type}")
            
            return True
            
        except subprocess.TimeoutExpired:
            self.results['errors'].append("APK decompilation timed out")
            return False
        except Exception as e:
            self.results['errors'].append(f"Error during decompilation: {str(e)}")
            return False
        finally:
            # Cleanup
            if os.path.exists(temp_dir):
                shutil.rmtree(temp_dir)
                
    def check_apk_size(self):
        """Check APK size is reasonable"""
        try:
            size_bytes = os.path.getsize(self.apk_path)
            size_mb = size_bytes / (1024 * 1024)
            
            self.results['checks'].append(f"✓ APK size: {size_mb:.2f} MB")
            
            # Warn if APK is too small (likely incomplete) or too large
            if size_mb < 0.5:
                self.results['warnings'].append(f"APK size is very small ({size_mb:.2f} MB) - may be incomplete")
            elif size_mb > 100:
                self.results['warnings'].append(f"APK size is large ({size_mb:.2f} MB) - consider optimization")
            
            return True
            
        except Exception as e:
            self.results['errors'].append(f"Error checking size: {str(e)}")
            return False
            
    def run_all_checks(self):
        """Run all integrity checks"""
        print(f"\nChecking APK: {self.apk_path}")
        print("="*70)
        
        # Run checks
        checks = [
            ("Existence", self.check_apk_exists),
            ("ZIP Structure", self.check_apk_is_zip),
            ("Signature", self.check_apk_signature),
            ("Size", self.check_apk_size),
            ("Manifest & Permissions", self.decompile_and_check_manifest),
        ]
        
        for check_name, check_func in checks:
            print(f"\n{check_name}:")
            check_func()
        
        # Print results
        print("\n" + "="*70)
        print("CHECK RESULTS")
        print("="*70)
        
        for check in self.results['checks']:
            print(check)
        
        if self.results['warnings']:
            print("\n⚠️  WARNINGS:")
            for warning in self.results['warnings']:
                print(f"  - {warning}")
        
        if self.results['errors']:
            print("\n❌ ERRORS:")
            for error in self.results['errors']:
                print(f"  - {error}")
        
        print("\n" + "="*70)
        if self.results['valid'] and not self.results['errors']:
            print("✅ APK INTEGRITY CHECK PASSED")
        else:
            print("❌ APK INTEGRITY CHECK FAILED")
        print("="*70 + "\n")
        
        return self.results


def check_apk_file(apk_path):
    """Convenience function to check an APK file"""
    checker = APKIntegrityChecker(apk_path)
    return checker.run_all_checks()


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python3 apk_integrity_checker.py <path_to_apk>")
        print("\nExample:")
        print("  python3 apk_integrity_checker.py output.apk")
        sys.exit(1)
    
    apk_path = sys.argv[1]
    results = check_apk_file(apk_path)
    
    # Exit with appropriate code
    sys.exit(0 if results['valid'] and not results['errors'] else 1)
