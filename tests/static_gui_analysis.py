#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Static GUI Analysis - No GUI Dependencies
Analyzes GUI code for feature completeness without requiring tkinter
"""

import sys
import os
import re
import json

def analyze_cli_features():
    """Extract all CLI features from androRAT.py"""
    
    try:
        androrat_path = os.path.join(os.path.dirname(__file__), '..', 'server', 'androRAT.py')
        with open(androrat_path, 'r') as f:
            content = f.read()
        
        # Extract argument parser definitions
        features = {}
        
        # Find all add_argument calls with better regex
        patterns = [
            r"parser\.add_argument\('([^']+)'[^)]*help='([^']*)'",
            r"parser\.add_argument\('([^']+)'[^)]*help=\"([^\"]*)\""
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, content)
            for arg, help_text in matches:
                features[arg.lstrip('-')] = help_text or "No description"
        
        # Also check for metavar arguments
        metavar_pattern = r"parser\.add_argument\('([^']+)'[^)]*metavar=\"([^\"]*)\""
        matches = re.findall(metavar_pattern, content)
        for arg, metavar in matches:
            if arg.lstrip('-') not in features:
                features[arg.lstrip('-')] = f"Parameter: {metavar}"
        
        return features
        
    except Exception as e:
        print(f"Error analyzing CLI features: {e}")
        return {}

def analyze_gui_file(gui_path, gui_name):
    """Analyze a GUI file for feature support"""
    
    try:
        with open(gui_path, 'r') as f:
            content = f.read()
        
        # Check for various feature indicators
        feature_indicators = {
            'stealth': ['stealth', 'stealth_var', 'StealthVar', 'STEALTH'],
            'anti_analysis': ['anti_analysis', 'anti-analysis', 'antianalysis', 'anti_var'],
            'play_protect_evasion': ['play_protect', 'play-protect', 'playprotect', 'play_var'],
            'advanced_obfuscation': ['advanced_obfuscation', 'advanced-obfuscation', 'obfuscation', 'obfuscate'],
            'fake_certificates': ['fake_certificates', 'fake-certificates', 'certificates', 'cert'],
            'inject': ['inject', 'injection', 'inject_var', 'target_apk'],
            'target_apk': ['target_apk', 'target-apk', 'targetapk', 'apk_path'],
            'tunnel_service': ['tunnel_service', 'tunnel-service', 'tunneling', 'ngrok'],
            'random_package': ['random_package', 'random-package', 'package'],
            'build_functionality': ['build', 'start_build', 'build_apk', 'create_build'],
            'shell_functionality': ['shell', 'start_shell', 'create_shell', 'terminal'],
            'evasion_options': ['evasion', 'options', 'config', 'settings'],
            'file_operations': ['file', 'browse', 'filedialog', 'upload', 'download'],
            'client_management': ['client', 'connected', 'refresh', 'select'],
            'logging': ['log', 'add_log', 'message', 'output'],
            'validation': ['validate', 'check', 'verify', 'input'],
            'threading': ['thread', 'queue', 'async', 'background']
        }
        
        found_features = {}
        for feature, indicators in feature_indicators.items():
            found = False
            for indicator in indicators:
                if indicator.lower() in content.lower():
                    found = True
                    break
            found_features[feature] = found
        
        # Count methods and classes
        method_count = len(re.findall(r'def\s+\w+\(', content))
        class_count = len(re.findall(r'class\s+\w+', content))
        
        # Look for specific method names
        important_methods = {
            'build_methods': ['start_build', 'build_apk', 'validate_build'],
            'shell_methods': ['start_shell', 'shell', 'command'],
            'client_methods': ['refresh_client', 'select_client', 'load_client'],
            'file_methods': ['browse_file', 'upload', 'download', 'file_dialog'],
            'evasion_methods': ['apply_evasion', 'stealth', 'obfuscate']
        }
        
        method_analysis = {}
        for category, methods in important_methods.items():
            found_methods = []
            for method in methods:
                if method in content:
                    found_methods.append(method)
            method_analysis[category] = found_methods
        
        return {
            'name': gui_name,
            'features': found_features,
            'method_count': method_count,
            'class_count': class_count,
            'method_analysis': method_analysis,
            'file_size': len(content),
            'line_count': len(content.split('\n'))
        }
        
    except Exception as e:
        print(f"Error analyzing {gui_name}: {e}")
        return None

def analyze_utils_functions():
    """Analyze utils.py for available functions"""
    
    try:
        utils_path = os.path.join(os.path.dirname(__file__), '..', 'server', 'utils.py')
        with open(utils_path, 'r') as f:
            content = f.read()
        
        # Extract function definitions
        functions = re.findall(r'def\s+(\w+)\(', content)
        
        # Categorize functions
        function_categories = {
            'build_functions': [],
            'evasion_functions': [],
            'injection_functions': [],
            'device_functions': [],
            'shell_functions': [],
            'utility_functions': []
        }
        
        # Categorize based on function names
        for func in functions:
            func_lower = func.lower()
            if 'build' in func_lower:
                function_categories['build_functions'].append(func)
            elif any(keyword in func_lower for keyword in ['evasion', 'stealth', 'obfuscate', 'anti', 'protect', 'fake']):
                function_categories['evasion_functions'].append(func)
            elif any(keyword in func_lower for keyword in ['inject', 'merge', 'extract', 'sign']):
                function_categories['injection_functions'].append(func)
            elif any(keyword in func_lower for keyword in ['get', 'read', 'call', 'location', 'sms', 'audio', 'video']):
                function_categories['device_functions'].append(func)
            elif any(keyword in func_lower for keyword in ['shell', 'recv', 'cmd']):
                function_categories['shell_functions'].append(func)
            else:
                function_categories['utility_functions'].append(func)
        
        return {
            'total_functions': len(functions),
            'categories': function_categories,
            'all_functions': functions
        }
        
    except Exception as e:
        print(f"Error analyzing utils.py: {e}")
        return None

def generate_feature_gap_report():
    """Generate comprehensive feature gap analysis"""
    
    print("=" * 80)
    print("COMPREHENSIVE GUI FEATURE GAP ANALYSIS")
    print("=" * 80)
    print()
    
    # Analyze CLI features
    print("1. CLI FEATURE ANALYSIS")
    print("-" * 40)
    cli_features = analyze_cli_features()
    
    print(f"Total CLI Features: {len(cli_features)}")
    for feature, description in cli_features.items():
        print(f"  - {feature}: {description}")
    print()
    
    # Analyze GUI implementations
    print("2. GUI IMPLEMENTATION ANALYSIS")
    print("-" * 40)
    
    gui_files = [
        ('server/androRAT_gui.py', 'Basic GUI'),
        ('server/androRAT_advanced_gui.py', 'Advanced GUI')
    ]
    
    gui_analyses = []
    for gui_file, gui_name in gui_files:
        gui_path = os.path.join(os.path.dirname(__file__), '..', gui_file)
        if os.path.exists(gui_path):
            analysis = analyze_gui_file(gui_path, gui_name)
            if analysis:
                gui_analyses.append(analysis)
                
                print(f"\n{gui_name.upper()}:")
                print(f"  File size: {analysis['file_size']} characters")
                print(f"  Lines: {analysis['line_count']}")
                print(f"  Classes: {analysis['class_count']}")
                print(f"  Methods: {analysis['method_count']}")
                
                print(f"  Feature Support:")
                for feature, supported in analysis['features'].items():
                    status = "✅" if supported else "❌"
                    print(f"    {status} {feature}")
                
                print(f"  Method Categories:")
                for category, methods in analysis['method_analysis'].items():
                    print(f"    {category}: {len(methods)} methods {methods}")
    
    # Analyze utils functions
    print("\n3. BACKEND FUNCTION ANALYSIS")
    print("-" * 40)
    utils_analysis = analyze_utils_functions()
    
    if utils_analysis:
        print(f"Total Backend Functions: {utils_analysis['total_functions']}")
        for category, functions in utils_analysis['categories'].items():
            print(f"  {category}: {len(functions)} functions")
            for func in functions[:5]:  # Show first 5
                print(f"    - {func}")
            if len(functions) > 5:
                print(f"    ... and {len(functions) - 5} more")
    
    # Generate gap analysis
    print("\n4. CRITICAL FEATURE GAP ANALYSIS")
    print("-" * 40)
    
    critical_cli_features = [
        'stealth', 'anti_analysis', 'play_protect_evasion', 
        'advanced_obfuscation', 'fake_certificates', 'inject', 'target_apk'
    ]
    
    for gui_analysis in gui_analyses:
        print(f"\n{gui_analysis['name'].upper()} Missing Features:")
        missing_count = 0
        for feature in critical_cli_features:
            if not gui_analysis['features'].get(feature, False):
                print(f"  ❌ {feature}")
                missing_count += 1
        
        if missing_count == 0:
            print("  ✅ All critical features present")
        else:
            print(f"  Total missing: {missing_count}/{len(critical_cli_features)}")
    
    # Generate recommendations
    print("\n5. IMPROVEMENT RECOMMENDATIONS")
    print("-" * 40)
    
    recommendations = {
        'Basic GUI': [
            "Add evasion options panel with checkboxes for stealth, anti-analysis, etc.",
            "Add APK injection mode with target APK file browser",
            "Add advanced build options section",
            "Add progress indicators for build operations",
            "Add input validation with visual feedback"
        ],
        'Advanced GUI': [
            "Integrate all CLI evasion features into APK builder",
            "Add real-time client monitoring dashboard",
            "Add bulk client operations and grouping",
            "Add client data export and reporting features",
            "Add automated testing and validation features"
        ],
        'Both GUIs': [
            "Add configuration profiles and templates",
            "Add comprehensive help system and tooltips",
            "Add dark/light theme support",
            "Add keyboard shortcuts and accessibility features",
            "Add logging levels and log export functionality"
        ]
    }
    
    for gui_type, recs in recommendations.items():
        print(f"\n{gui_type}:")
        for i, rec in enumerate(recs, 1):
            print(f"  {i}. {rec}")
    
    # Generate specific implementation tasks
    print("\n6. IMPLEMENTATION PRIORITY TASKS")
    print("-" * 40)
    
    priority_tasks = [
        ("HIGH", "Add evasion options to Basic GUI (stealth, anti-analysis, play-protect)"),
        ("HIGH", "Add APK injection functionality to both GUIs"),
        ("MEDIUM", "Add advanced obfuscation and certificate options"),
        ("MEDIUM", "Enhance Advanced GUI with real-time monitoring"),
        ("LOW", "Add configuration save/load functionality"),
        ("LOW", "Add theme and accessibility options")
    ]
    
    for priority, task in priority_tasks:
        print(f"  [{priority}] {task}")
    
    return {
        'cli_features': cli_features,
        'gui_analyses': gui_analyses,
        'utils_analysis': utils_analysis,
        'recommendations': recommendations
    }

def main():
    """Main analysis function"""
    
    # Change to correct directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(os.path.dirname(script_dir))
    
    # Generate analysis
    analysis_result = generate_feature_gap_report()
    
    # Save results to file
    output_file = os.path.join(script_dir, 'gui_feature_gap_analysis.json')
    try:
        # Convert analysis to JSON-serializable format
        json_result = {
            'cli_features_count': len(analysis_result['cli_features']),
            'cli_features': list(analysis_result['cli_features'].keys()),
            'gui_count': len(analysis_result['gui_analyses']),
            'gui_summaries': [
                {
                    'name': gui['name'],
                    'supported_features': sum(1 for v in gui['features'].values() if v),
                    'total_features': len(gui['features']),
                    'method_count': gui['method_count'],
                    'class_count': gui['class_count']
                }
                for gui in analysis_result['gui_analyses']
            ],
            'backend_functions': analysis_result['utils_analysis']['total_functions'] if analysis_result['utils_analysis'] else 0
        }
        
        with open(output_file, 'w') as f:
            json.dump(json_result, f, indent=2)
        
        print(f"\n📊 Analysis saved to: {output_file}")
        
    except Exception as e:
        print(f"Warning: Could not save analysis to file: {e}")
    
    print("\n" + "=" * 80)
    print("ANALYSIS COMPLETE")
    print("=" * 80)

if __name__ == "__main__":
    main()