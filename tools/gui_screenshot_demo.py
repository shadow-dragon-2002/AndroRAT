#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
GUI Screenshot Generator
Creates a visual demonstration of the AndroRAT GUI
"""

import sys
import os

# Add server directory to path for imports
tools_dir = os.path.dirname(os.path.abspath(__file__))
server_dir = os.path.join(os.path.dirname(tools_dir), 'server')
sys.path.insert(0, server_dir)

import tkinter as tk
import subprocess
import time

def create_gui_screenshot():
    """Create a screenshot of the AndroRAT GUI"""
    print("📸 Creating AndroRAT GUI screenshot...")
    
    # Setup virtual display
    os.environ['DISPLAY'] = ':99'
    xvfb = subprocess.Popen(['Xvfb', ':99', '-screen', '0', '1024x768x24'], 
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(2)
    
    try:
        import androRAT_gui
        
        # Create GUI
        root = tk.Tk()
        root.title("AndroRAT - Android Remote Administration Tool")
        root.geometry("800x600")
        root.configure(bg='#f0f0f0')
        
        app = androRAT_gui.AndroRATGUI(root)
        
        # Configure with sample data
        app.ip_var.set("192.168.1.100")
        app.port_var.set("8000")
        app.output_var.set("modern_android.apk")
        app.icon_var.set(True)
        app.ngrok_var.set(False)
        
        # Add some sample log messages
        app.add_log("AndroRAT GUI Interface Ready", "INFO")
        app.add_log("Android 13+ compatibility enabled", "INFO")
        app.add_log("Modern permissions configured", "INFO")
        app.add_log("Foreground services updated", "INFO")
        app.add_log("GUI interface fully functional", "INFO")
        app.add_log("Ready to build APK for Android 13+", "INFO")
        
        # Update status
        app.status_var.set("Ready - AndroRAT modernized for Android 13+")
        
        # Update GUI
        root.update()
        time.sleep(1)
        
        # Try to take screenshot using system command
        try:
            screenshot_result = subprocess.run([
                'import', '-window', 'root', '/tmp/androrat_gui_demo.png'
            ], capture_output=True, text=True, timeout=10)
            
            if screenshot_result.returncode == 0:
                print("✅ GUI screenshot saved to /tmp/androrat_gui_demo.png")
            else:
                print("⚠️  Screenshot command failed, creating text representation")
        except:
            print("⚠️  Screenshot tools not available")
        
        # Create a text-based representation
        print("\n" + "=" * 80)
        print("GUI VISUAL REPRESENTATION")
        print("=" * 80)
        print("""
┌────────────────────────────────────────────────────────────────────────────┐
│ AndroRAT - Android Remote Administration Tool                           [×] │
├────────────────────────────────────────────────────────────────────────────┤
│ [Build APK] [Shell Connection] [Activity Logs]                              │
├────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│ AndroRAT APK Builder                                                         │
│ Configure and build your Android RAT APK                                    │
│                                                                              │
│ ┌─ Configuration ──────────────────────────────────────────────────────────┐ │
│ │ ┌─ Connection Settings ─────────────────────────────────────────────────┐ │ │
│ │ │ ☐ Use Ngrok tunnel (automatically sets IP)                           │ │ │
│ │ │ IP Address: [192.168.1.100    ] Port: [8000     ]                   │ │ │
│ │ └───────────────────────────────────────────────────────────────────────┘ │ │
│ │ ┌─ Output Settings ─────────────────────────────────────────────────────┐ │ │
│ │ │ APK Name: [modern_android.apk ] [Browse]                             │ │ │
│ │ │ ☑ Visible icon after installation                                    │ │ │
│ │ └───────────────────────────────────────────────────────────────────────┘ │ │
│ └──────────────────────────────────────────────────────────────────────────┘ │
│                                                                              │
│ [Build APK] [Clear Log]                                                      │
│ ████████████████████████████████████████████████████████████████████████████ │
│                                                                              │
│ Activity Logs:                                                               │
│ ┌────────────────────────────────────────────────────────────────────────┐   │
│ │ [INFO] AndroRAT GUI Interface Ready                                    │   │
│ │ [INFO] Android 13+ compatibility enabled                              │   │
│ │ [INFO] Modern permissions configured                                   │   │
│ │ [INFO] Foreground services updated                                     │   │
│ │ [INFO] GUI interface fully functional                                  │   │
│ │ [INFO] Ready to build APK for Android 13+                             │   │
│ └────────────────────────────────────────────────────────────────────────┘   │
│                                                                              │
├────────────────────────────────────────────────────────────────────────────┤
│ Ready - AndroRAT modernized for Android 13+                                 │
└────────────────────────────────────────────────────────────────────────────┘
""")
        print("=" * 80)
        print("✅ GUI Visual Representation Created")
        
        # Clean shutdown
        root.destroy()
        
    except Exception as e:
        print(f"❌ GUI screenshot creation failed: {e}")
    finally:
        try:
            xvfb.terminate()
            xvfb.wait(timeout=5)
        except:
            pass

if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    create_gui_screenshot()