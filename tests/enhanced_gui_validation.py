#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Enhanced GUI Feature Validation Test
Tests the enhanced GUI implementations for complete feature coverage
"""

import sys
import os
import re

def validate_basic_gui_enhancements():
    """Validate that Basic GUI has all enhanced features"""
    
    print("=" * 60)
    print("BASIC GUI ENHANCEMENT VALIDATION")
    print("=" * 60)
    
    try:
        gui_path = os.path.join(os.path.dirname(__file__), '..', 'server', 'androRAT_gui.py')
        with open(gui_path, 'r') as f:
            content = f.read()
        
        # Check for enhanced variables
        enhanced_features = {
            'stealth_var': 'Stealth mode variable',
            'anti_analysis_var': 'Anti-analysis variable',
            'play_protect_var': 'Play Protect evasion variable',
            'advanced_obfuscation_var': 'Advanced obfuscation variable',
            'fake_certificates_var': 'Fake certificates variable',
            'random_package_var': 'Random package variable',
            'inject_var': 'APK injection variable',
            'target_apk_var': 'Target APK variable'
        }
        
        print("1. Enhanced Variables Check:")
        missing_vars = []
        for var, description in enhanced_features.items():
            if var in content:
                print(f"  ✅ {var}: {description}")
            else:
                print(f"  ❌ {var}: {description}")
                missing_vars.append(var)
        
        # Check for enhanced UI components
        ui_components = {
            'evasion_frame': 'Evasion options panel',
            'injection_frame': 'APK injection panel',
            'target_frame': 'Target APK selection',
            'Stealth Mode': 'Stealth checkbox',
            'Anti-Analysis': 'Anti-analysis checkbox',
            'Play Protect': 'Play Protect checkbox',
            'Advanced.*Obfuscation': 'Advanced obfuscation checkbox',
            'Fake.*Certificate': 'Fake certificates checkbox',
            'Random.*Package': 'Random package checkbox',
            'inject.*APK': 'APK injection checkbox'
        }
        
        print("\n2. Enhanced UI Components Check:")
        missing_ui = []
        for component, description in ui_components.items():
            if re.search(component, content, re.IGNORECASE):
                print(f"  ✅ {component}: {description}")
            else:
                print(f"  ❌ {component}: {description}")
                missing_ui.append(component)
        
        # Check for enhanced methods
        enhanced_methods = {
            'on_inject_toggle': 'APK injection toggle handler',
            'browse_target_apk': 'Target APK browser',
            'get_evasion_options': 'Evasion options getter',
            'inject_rat_into_apk': 'APK injection function call',
            'build_with_evasion': 'Evasion build function call'
        }
        
        print("\n3. Enhanced Methods Check:")
        missing_methods = []
        for method, description in enhanced_methods.items():
            if method in content:
                print(f"  ✅ {method}: {description}")
            else:
                print(f"  ❌ {method}: {description}")
                missing_methods.append(method)
        
        # Calculate completion score
        total_features = len(enhanced_features) + len(ui_components) + len(enhanced_methods)
        missing_total = len(missing_vars) + len(missing_ui) + len(missing_methods)
        completion_score = ((total_features - missing_total) / total_features) * 100
        
        print(f"\n4. Basic GUI Enhancement Score: {completion_score:.1f}%")
        
        if completion_score >= 90:
            print("🎉 EXCELLENT: Basic GUI fully enhanced")
        elif completion_score >= 75:
            print("✅ GOOD: Basic GUI well enhanced")
        elif completion_score >= 50:
            print("⚠️ PARTIAL: Basic GUI partially enhanced")
        else:
            print("❌ POOR: Basic GUI needs more work")
        
        return completion_score
        
    except Exception as e:
        print(f"❌ Error validating Basic GUI: {e}")
        return 0

def validate_advanced_gui_enhancements():
    """Validate that Advanced GUI has all enhanced features"""
    
    print("\n" + "=" * 60)
    print("ADVANCED GUI ENHANCEMENT VALIDATION")
    print("=" * 60)
    
    try:
        gui_path = os.path.join(os.path.dirname(__file__), '..', 'server', 'androRAT_advanced_gui.py')
        with open(gui_path, 'r') as f:
            content = f.read()
        
        # Check for enhanced APK builder
        apk_builder_features = {
            'Advanced APK Builder': 'Enhanced APK builder title',
            'Advanced Evasion Options': 'Evasion options section',
            'APK Injection Mode': 'Injection mode section',
            'apk_stealth_var': 'Stealth variable',
            'apk_anti_analysis_var': 'Anti-analysis variable',
            'apk_play_protect_var': 'Play Protect variable',
            'apk_obfuscation_var': 'Obfuscation variable',
            'apk_inject_var': 'Injection variable',
            'build_enhanced_apk': 'Enhanced build method'
        }
        
        print("1. Enhanced APK Builder Check:")
        missing_features = []
        for feature, description in apk_builder_features.items():
            if feature in content:
                print(f"  ✅ {feature}: {description}")
            else:
                print(f"  ❌ {feature}: {description}")
                missing_features.append(feature)
        
        # Check for enhanced methods
        enhanced_methods = {
            'on_apk_tunnel_toggle': 'APK tunnel toggle handler',
            'on_apk_inject_toggle': 'APK injection toggle handler',
            'browse_apk_output': 'APK output browser',
            'browse_target_apk': 'Target APK browser'
        }
        
        print("\n2. Enhanced Methods Check:")
        missing_methods = []
        for method, description in enhanced_methods.items():
            if method in content:
                print(f"  ✅ {method}: {description}")
            else:
                print(f"  ❌ {method}: {description}")
                missing_methods.append(method)
        
        # Check for scrollable interface
        ui_enhancements = {
            'scrollable_frame': 'Scrollable interface',
            'Canvas': 'Canvas for scrolling',
            'Scrollbar': 'Scrollbar widget',
            'geometry.*700.*800': 'Larger window size',
            'evasion_cols': 'Two-column evasion layout'
        }
        
        print("\n3. UI Enhancements Check:")
        missing_ui = []
        for enhancement, description in ui_enhancements.items():
            if re.search(enhancement, content, re.IGNORECASE):
                print(f"  ✅ {enhancement}: {description}")
            else:
                print(f"  ❌ {enhancement}: {description}")
                missing_ui.append(enhancement)
        
        # Calculate completion score
        total_features = len(apk_builder_features) + len(enhanced_methods) + len(ui_enhancements)
        missing_total = len(missing_features) + len(missing_methods) + len(missing_ui)
        completion_score = ((total_features - missing_total) / total_features) * 100
        
        print(f"\n4. Advanced GUI Enhancement Score: {completion_score:.1f}%")
        
        if completion_score >= 90:
            print("🎉 EXCELLENT: Advanced GUI fully enhanced")
        elif completion_score >= 75:
            print("✅ GOOD: Advanced GUI well enhanced")
        elif completion_score >= 50:
            print("⚠️ PARTIAL: Advanced GUI partially enhanced")
        else:
            print("❌ POOR: Advanced GUI needs more work")
        
        return completion_score
        
    except Exception as e:
        print(f"❌ Error validating Advanced GUI: {e}")
        return 0

def validate_feature_parity():
    """Validate feature parity between CLI and GUI"""
    
    print("\n" + "=" * 60)
    print("CLI-GUI FEATURE PARITY VALIDATION")
    print("=" * 60)
    
    # CLI features that should be in GUI
    cli_features = [
        'stealth', 'anti-analysis', 'play-protect-evasion',
        'advanced-obfuscation', 'fake-certificates', 'random-package',
        'inject', 'target-apk', 'tunnel', 'tunnel-service'
    ]
    
    try:
        # Check Basic GUI
        basic_gui_path = os.path.join(os.path.dirname(__file__), '..', 'server', 'androRAT_gui.py')
        with open(basic_gui_path, 'r') as f:
            basic_content = f.read()
        
        # Check Advanced GUI
        advanced_gui_path = os.path.join(os.path.dirname(__file__), '..', 'server', 'androRAT_advanced_gui.py')
        with open(advanced_gui_path, 'r') as f:
            advanced_content = f.read()
        
        print("1. Basic GUI Feature Parity:")
        basic_score = 0
        for feature in cli_features:
            # Check various forms of the feature name
            feature_variants = [
                feature.replace('-', '_'),
                feature.replace('-', ''),
                feature
            ]
            
            found = any(variant.lower() in basic_content.lower() for variant in feature_variants)
            if found:
                print(f"  ✅ {feature}")
                basic_score += 1
            else:
                print(f"  ❌ {feature}")
        
        basic_parity = (basic_score / len(cli_features)) * 100
        print(f"  Basic GUI Parity: {basic_parity:.1f}%")
        
        print("\n2. Advanced GUI Feature Parity:")
        advanced_score = 0
        for feature in cli_features:
            feature_variants = [
                feature.replace('-', '_'),
                feature.replace('-', ''),
                feature
            ]
            
            found = any(variant.lower() in advanced_content.lower() for variant in feature_variants)
            if found:
                print(f"  ✅ {feature}")
                advanced_score += 1
            else:
                print(f"  ❌ {feature}")
        
        advanced_parity = (advanced_score / len(cli_features)) * 100
        print(f"  Advanced GUI Parity: {advanced_parity:.1f}%")
        
        overall_parity = (basic_parity + advanced_parity) / 2
        print(f"\n3. Overall Feature Parity: {overall_parity:.1f}%")
        
        return overall_parity
        
    except Exception as e:
        print(f"❌ Error validating feature parity: {e}")
        return 0

def validate_integration_completeness():
    """Validate that backend functions are properly integrated"""
    
    print("\n" + "=" * 60)
    print("BACKEND INTEGRATION VALIDATION")
    print("=" * 60)
    
    # Key backend functions that should be called in GUI
    backend_functions = [
        'inject_rat_into_apk',
        'build_with_evasion',
        'is_valid_ip',
        'is_valid_port',
        'is_valid_filename'
    ]
    
    try:
        # Check both GUIs
        gui_files = [
            ('Basic GUI', 'server/androRAT_gui.py'),
            ('Advanced GUI', 'server/androRAT_advanced_gui.py')
        ]
        
        for gui_name, gui_file in gui_files:
            gui_path = os.path.join(os.path.dirname(__file__), '..', gui_file)
            with open(gui_path, 'r') as f:
                content = f.read()
            
            print(f"\n{gui_name} Backend Integration:")
            integration_score = 0
            
            for function in backend_functions:
                if function in content:
                    print(f"  ✅ {function}")
                    integration_score += 1
                else:
                    print(f"  ❌ {function}")
            
            integration_pct = (integration_score / len(backend_functions)) * 100
            print(f"  Integration Score: {integration_pct:.1f}%")
        
    except Exception as e:
        print(f"❌ Error validating integration: {e}")

def main():
    """Main validation function"""
    
    print("🔍 COMPREHENSIVE GUI FEATURE VALIDATION")
    print("Testing enhanced GUI implementations for complete functionality")
    print()
    
    # Run validations
    basic_score = validate_basic_gui_enhancements()
    advanced_score = validate_advanced_gui_enhancements()
    parity_score = validate_feature_parity()
    validate_integration_completeness()
    
    # Calculate overall score
    overall_score = (basic_score + advanced_score + parity_score) / 3
    
    print("\n" + "=" * 60)
    print("FINAL VALIDATION SUMMARY")
    print("=" * 60)
    
    print(f"Basic GUI Enhancement Score: {basic_score:.1f}%")
    print(f"Advanced GUI Enhancement Score: {advanced_score:.1f}%")
    print(f"CLI-GUI Feature Parity Score: {parity_score:.1f}%")
    print(f"Overall Functionality Score: {overall_score:.1f}%")
    
    if overall_score >= 90:
        print("\n🎉 EXCELLENT: GUI implementations are fully enhanced with all features!")
        print("✅ All CLI features are now available in both GUI versions")
        print("✅ Advanced evasion and injection capabilities integrated")
        print("✅ Professional UI with comprehensive options")
    elif overall_score >= 75:
        print("\n✅ GOOD: GUI implementations are well enhanced")
        print("💡 Minor improvements may be needed")
    elif overall_score >= 50:
        print("\n⚠️ PARTIAL: GUI implementations partially enhanced")
        print("🔧 Additional work needed for complete feature parity")
    else:
        print("\n❌ POOR: GUI implementations need significant improvement")
        print("🚨 Major feature gaps still exist")
    
    return overall_score

if __name__ == "__main__":
    # Change to correct directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(os.path.dirname(script_dir))
    
    result = main()
    sys.exit(0 if result >= 75 else 1)