#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Test utilities for AndroRAT test suite
Handles path setup for importing server modules from tests
"""

import os
import sys

def setup_server_path():
    """Add server directory to Python path for imports"""
    test_dir = os.path.dirname(os.path.abspath(__file__))
    server_dir = os.path.join(os.path.dirname(test_dir), 'server')
    if server_dir not in sys.path:
        sys.path.insert(0, server_dir)
    return server_dir

def get_project_root():
    """Get the project root directory"""
    test_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.dirname(test_dir)

# Automatically setup server path when imported
setup_server_path()