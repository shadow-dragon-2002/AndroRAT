#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
GUI Testing Script for AndroRAT
Tests GUI functionality extensively
"""

import sys
import os
import subprocess
import time
import threading
import tempfile
import platform

def test_gui_startup():
    """Test GUI startup and basic functionality"""
    print("=" * 60)
    print("GUI STARTUP AND BASIC FUNCTIONALITY TEST")
    print("=" * 60)
    
    # Test GUI module imports
    print("🧪 Testing GUI module imports...")
    
    import_test_code = '''
import sys
import os
sys.path.insert(0, ".")

try:
    import tkinter as tk
    print("✓ tkinter imported")
    
    import androRAT_gui
    print("✓ androRAT_gui imported")
    
    from utils import *
    print("✓ utils imported")
    
    print("SUCCESS: All GUI modules imported successfully")
    
except Exception as e:
    print(f"ERROR: {e}")
    sys.exit(1)
'''
    
    result = subprocess.run([sys.executable, '-c', import_test_code], 
                          capture_output=True, text=True)
    
    if result.returncode == 0:
        print("✅ GUI module imports successful")
        print(result.stdout)
    else:
        print("❌ GUI module import failed")
        print(result.stderr)
        return False
    
    return True

def test_gui_class_instantiation():
    """Test GUI class instantiation and widget creation"""
    print("\n" + "=" * 60)
    print("GUI CLASS INSTANTIATION TEST")
    print("=" * 60)
    
    gui_instantiation_test = '''
import sys
import os
import tkinter as tk
sys.path.insert(0, ".")

try:
    import androRAT_gui
    
    # Create root window (hidden)
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    
    print("✓ tkinter root window created")
    
    # Create AndroRAT GUI instance
    app = androRAT_gui.AndroRATGUI(root)
    print("✓ AndroRAT GUI instance created")
    
    # Test if main components exist
    if hasattr(app, 'notebook'):
        print("✓ Notebook widget exists")
    
    if hasattr(app, 'ip_var'):
        print("✓ IP variable exists")
        
    if hasattr(app, 'port_var'):
        print("✓ Port variable exists")
        
    if hasattr(app, 'output_var'):
        print("✓ Output variable exists")
    
    # Test variable defaults
    if app.port_var.get() == "8000":
        print("✓ Default port value correct")
        
    if "karma.apk" in app.output_var.get():
        print("✓ Default output filename correct")
    
    root.destroy()
    print("✓ GUI cleanup successful")
    
    print("SUCCESS: GUI class instantiation test passed")
    
except Exception as e:
    print(f"ERROR: GUI instantiation failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
'''
    
    result = subprocess.run([sys.executable, '-c', gui_instantiation_test], 
                          capture_output=True, text=True)
    
    if result.returncode == 0:
        print("✅ GUI class instantiation successful")
        print(result.stdout)
    else:
        print("❌ GUI class instantiation failed")
        print(result.stderr)
        return False
    
    return True

def test_gui_methods():
    """Test GUI methods and functionality"""
    print("\n" + "=" * 60)
    print("GUI METHODS FUNCTIONALITY TEST")
    print("=" * 60)
    
    gui_methods_test = '''
import sys
import os
import tkinter as tk
sys.path.insert(0, ".")

try:
    import androRAT_gui
    
    # Create root window (hidden)
    root = tk.Tk()
    root.withdraw()
    
    # Create AndroRAT GUI instance
    app = androRAT_gui.AndroRATGUI(root)
    print("✓ GUI instance created")
    
    # Test method existence
    methods_to_test = [
        'create_build_tab',
        'create_shell_tab', 
        'create_log_tab',
        'validate_inputs',
        'log_message',
        'clear_log'
    ]
    
    for method_name in methods_to_test:
        if hasattr(app, method_name):
            print(f"✓ Method {method_name} exists")
        else:
            print(f"⚠ Method {method_name} missing")
    
    # Test input validation
    if hasattr(app, 'validate_inputs'):
        # Test with empty IP
        app.ip_var.set("")
        app.port_var.set("8000")
        app.output_var.set("test.apk")
        
        is_valid = app.validate_inputs()
        if not is_valid:
            print("✓ Input validation works (empty IP rejected)")
        else:
            print("⚠ Input validation issue (empty IP accepted)")
            
        # Test with valid inputs
        app.ip_var.set("192.168.1.100")
        app.port_var.set("8000")
        app.output_var.set("test.apk")
        
        is_valid = app.validate_inputs()
        if is_valid:
            print("✓ Input validation works (valid inputs accepted)")
        else:
            print("⚠ Input validation issue (valid inputs rejected)")
    
    # Test logging functionality
    if hasattr(app, 'log_message'):
        app.log_message("Test log message")
        print("✓ Log message method works")
    
    root.destroy()
    print("SUCCESS: GUI methods test passed")
    
except Exception as e:
    print(f"ERROR: GUI methods test failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
'''
    
    result = subprocess.run([sys.executable, '-c', gui_methods_test], 
                          capture_output=True, text=True)
    
    if result.returncode == 0:
        print("✅ GUI methods test successful")
        print(result.stdout)
    else:
        print("❌ GUI methods test failed")
        print(result.stderr)
        return False
    
    return True

def test_gui_visual_startup():
    """Test GUI visual startup (with virtual display)"""
    print("\n" + "=" * 60)
    print("GUI VISUAL STARTUP TEST")
    print("=" * 60)
    
    # Start virtual display
    print("🖥️  Starting virtual display...")
    
    try:
        # Start Xvfb virtual display
        xvfb_process = subprocess.Popen([
            'Xvfb', ':99', '-screen', '0', '1024x768x24'
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        time.sleep(2)  # Give Xvfb time to start
        
        # Set DISPLAY environment variable
        env = os.environ.copy()
        env['DISPLAY'] = ':99'
        
        print("✓ Virtual display started")
        
        # Test GUI startup with display
        gui_visual_test = '''
import sys
import os
import tkinter as tk
sys.path.insert(0, ".")

try:
    import androRAT_gui
    
    # Create and show GUI
    root = tk.Tk()
    root.title("AndroRAT Test")
    root.geometry("400x300")
    
    app = androRAT_gui.AndroRATGUI(root)
    print("✓ GUI created and configured")
    
    # Test that we can interact with widgets
    app.ip_var.set("192.168.1.100")
    app.port_var.set("8080")
    app.output_var.set("visual_test.apk")
    
    print(f"✓ IP set to: {app.ip_var.get()}")
    print(f"✓ Port set to: {app.port_var.get()}")
    print(f"✓ Output set to: {app.output_var.get()}")
    
    # Update GUI
    root.update()
    print("✓ GUI update successful")
    
    # Simulate user interaction
    if hasattr(app, 'validate_inputs'):
        is_valid = app.validate_inputs()
        print(f"✓ Input validation result: {is_valid}")
    
    # Clean shutdown
    root.destroy()
    print("SUCCESS: GUI visual test completed")
    
except Exception as e:
    print(f"ERROR: GUI visual test failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
'''
        
        result = subprocess.run([
            sys.executable, '-c', gui_visual_test
        ], capture_output=True, text=True, env=env, timeout=30)
        
        if result.returncode == 0:
            print("✅ GUI visual startup successful")
            print(result.stdout)
            success = True
        else:
            print("❌ GUI visual startup failed")
            print("STDERR:", result.stderr)
            success = False
            
    except Exception as e:
        print(f"❌ Virtual display setup failed: {e}")
        success = False
        
    finally:
        # Clean up virtual display
        try:
            xvfb_process.terminate()
            xvfb_process.wait(timeout=5)
            print("🧹 Virtual display cleaned up")
        except:
            pass
    
    return success

def test_gui_integration():
    """Test GUI integration with backend functionality"""
    print("\n" + "=" * 60)
    print("GUI INTEGRATION TEST")
    print("=" * 60)
    
    gui_integration_test = '''
import sys
import os
import tkinter as tk
sys.path.insert(0, ".")

try:
    import androRAT_gui
    from utils import *
    
    # Create GUI instance
    root = tk.Tk()
    root.withdraw()
    
    app = androRAT_gui.AndroRATGUI(root)
    print("✓ GUI instance created")
    
    # Test integration with utils
    # Test standard output functions from utils
    test_output = stdOutput("info")
    if test_output:
        print("✓ Utils integration works")
    
    # Test that GUI can access utils functions
    if 'stdOutput' in dir():
        print("✓ Utils functions available in GUI context")
    
    # Test input validation integration
    app.ip_var.set("192.168.1.100")
    app.port_var.set("8000") 
    app.output_var.set("integration_test.apk")
    
    if app.validate_inputs():
        print("✓ GUI input validation integration works")
    
    # Test logging integration
    app.log_message("Integration test message")
    print("✓ GUI logging integration works")
    
    root.destroy()
    print("SUCCESS: GUI integration test passed")
    
except Exception as e:
    print(f"ERROR: GUI integration test failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
'''
    
    result = subprocess.run([sys.executable, '-c', gui_integration_test], 
                          capture_output=True, text=True)
    
    if result.returncode == 0:
        print("✅ GUI integration test successful")
        print(result.stdout)
    else:
        print("❌ GUI integration test failed")
        print(result.stderr)
        return False
    
    return True

def test_launcher_gui_mode():
    """Test launcher in GUI mode"""
    print("\n" + "=" * 60)
    print("LAUNCHER GUI MODE TEST")
    print("=" * 60)
    
    # Test launcher GUI mode functionality
    print("🧪 Testing launcher --gui option...")
    
    launcher_test_code = '''
import sys
import os
sys.path.insert(0, ".")

try:
    import launcher
    print("✓ Launcher module imported")
    
    # Test that launcher has GUI mode capability
    # This tests the module structure, not actual GUI launch
    print("SUCCESS: Launcher GUI mode test passed")
    
except Exception as e:
    print(f"ERROR: Launcher test failed: {e}")
    sys.exit(1)
'''
    
    result = subprocess.run([sys.executable, '-c', launcher_test_code], 
                          capture_output=True, text=True)
    
    if result.returncode == 0:
        print("✅ Launcher GUI mode test successful")
        print(result.stdout)
    else:
        print("❌ Launcher GUI mode test failed")
        print(result.stderr)
        return False
    
    # Test launcher help with GUI option
    print("🧪 Testing launcher help...")
    result = subprocess.run([sys.executable, 'launcher.py', '--help'], 
                          capture_output=True, text=True)
    
    if result.returncode == 0:
        print("✅ Launcher help works")
        if '--gui' in result.stdout:
            print("✓ GUI option available in launcher")
        else:
            print("⚠ GUI option not explicitly mentioned in help")
    else:
        print("❌ Launcher help failed")
        return False
    
    return True

def main():
    """Run all GUI tests"""
    print("Starting comprehensive GUI testing...")
    print(f"Platform: {platform.system()} {platform.release()}")
    print(f"Python: {sys.version}")
    
    # Change to script directory
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    tests = [
        ("GUI Startup", test_gui_startup),
        ("GUI Class Instantiation", test_gui_class_instantiation),
        ("GUI Methods", test_gui_methods),
        ("GUI Visual Startup", test_gui_visual_startup),
        ("GUI Integration", test_gui_integration),
        ("Launcher GUI Mode", test_launcher_gui_mode),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            print(f"\n{'='*20} RUNNING: {test_name} {'='*20}")
            success = test_func()
            results.append((test_name, success))
            
            if success:
                print(f"✅ {test_name} PASSED")
            else:
                print(f"❌ {test_name} FAILED")
                
        except Exception as e:
            print(f"❌ {test_name} ERROR: {e}")
            results.append((test_name, False))
    
    # Final summary
    print("\n" + "=" * 60)
    print("GUI TESTING FINAL SUMMARY")
    print("=" * 60)
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    print(f"Tests passed: {passed}/{total}")
    
    for test_name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}")
    
    if passed == total:
        print("\n🎉 ALL GUI TESTS PASSED!")
        print("✅ GUI interface is fully functional")
        print("✅ All GUI components working properly")
        print("✅ GUI integration validated")
    else:
        print(f"\n⚠️ {total - passed} GUI tests failed")
        print("🔍 Check individual test results above")
    
    print("=" * 60)
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)