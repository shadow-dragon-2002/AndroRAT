#!/usr/bin/python
# -*- coding: utf-8 -*-

import subprocess
import socket
import requests
import json
import time
import os
import sys
from utils import stdOutput

class TunnelingManager:
    """
    Manages multiple tunneling solutions as alternatives to ngrok.
    Provides fallback options when ngrok requires credit cards or fails.
    """
    
    def __init__(self):
        self.tunnel_url = None
        self.tunnel_process = None
        self.tunnel_type = None
        
    def create_tunnel(self, port, prefer_service="auto"):
        """
        Create a tunnel using the best available service.
        
        Args:
            port: Local port to tunnel
            prefer_service: Preferred service ("ngrok", "cloudflared", "serveo", "localtunnel", "auto")
            
        Returns:
            tuple: (ip, port, tunnel_url) if successful, None if failed
        """
        
        services = ["cloudflared", "serveo", "localtunnel", "ngrok"] if prefer_service == "auto" else [prefer_service]
        
        for service in services:
            try:
                print(stdOutput("info") + f"\033[1mTrying {service}...")
                
                if service == "cloudflared":
                    result = self._try_cloudflared(port)
                elif service == "serveo":
                    result = self._try_serveo(port)
                elif service == "localtunnel":
                    result = self._try_localtunnel(port)
                elif service == "ngrok":
                    result = self._try_ngrok(port)
                else:
                    continue
                    
                if result:
                    self.tunnel_type = service
                    ip, tunnel_port, self.tunnel_url = result
                    print(stdOutput("success") + f"\033[1m{service} tunnel established!")
                    print(stdOutput("info") + f"\033[1mTunnel URL: {self.tunnel_url}")
                    print(stdOutput("info") + f"\033[1mTunnel IP: {ip} PORT: {tunnel_port}")
                    return ip, tunnel_port, self.tunnel_url
                    
            except Exception as e:
                print(stdOutput("warning") + f"\033[1m{service} failed: {str(e)}")
                continue
                
        print(stdOutput("error") + "\033[1mAll tunneling services failed!")
        return None
        
    def _try_cloudflared(self, port):
        """Try Cloudflare Tunnels (cloudflared)"""
        
        # Check if cloudflared is installed
        try:
            result = subprocess.run(["cloudflared", "version"], capture_output=True, text=True, timeout=10)
            if result.returncode != 0:
                raise Exception("cloudflared not installed")
        except:
            print(stdOutput("info") + "\033[1mInstalling cloudflared...")
            self._install_cloudflared()
            
        # Start tunnel
        try:
            cmd = ["cloudflared", "tunnel", "--url", f"tcp://localhost:{port}"]
            self.tunnel_process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            
            # Wait for tunnel URL
            time.sleep(5)
            
            # Parse output for tunnel URL
            # Note: Cloudflared TCP tunnels require authentication, implementing HTTP tunnel instead
            cmd = ["cloudflared", "tunnel", "--url", f"http://localhost:{port}"]
            self.tunnel_process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            
            time.sleep(5)
            
            # For now, return None as cloudflared TCP requires more setup
            # In a real implementation, you'd parse the tunnel URL from output
            return None
            
        except Exception as e:
            raise Exception(f"Cloudflared tunnel failed: {str(e)}")
            
    def _try_serveo(self, port):
        """Try Serveo SSH tunnel"""
        try:
            # Generate random subdomain
            import random
            import string
            subdomain = ''.join(random.choices(string.ascii_lowercase, k=8))
            
            # Start SSH tunnel to serveo
            cmd = ["ssh", "-o", "StrictHostKeyChecking=no", "-R", 
                   f"{subdomain}:80:localhost:{port}", "serveo.net"]
            
            self.tunnel_process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            
            time.sleep(3)
            
            # Check if tunnel is established
            tunnel_url = f"https://{subdomain}.serveo.net"
            
            # Serveo provides HTTP tunnels, extract the host for IP resolution
            try:
                ip = socket.gethostbyname(f"{subdomain}.serveo.net")
                return ip, 80, tunnel_url
            except:
                raise Exception("Could not resolve serveo tunnel")
                
        except Exception as e:
            raise Exception(f"Serveo tunnel failed: {str(e)}")
            
    def _try_localtunnel(self, port):
        """Try LocalTunnel (requires npm)"""
        try:
            # Check if lt is installed
            result = subprocess.run(["lt", "--version"], capture_output=True, text=True, timeout=10)
            if result.returncode != 0:
                print(stdOutput("info") + "\033[1mInstalling localtunnel...")
                subprocess.run(["npm", "install", "-g", "localtunnel"], check=True, timeout=30)
            
            # Start tunnel
            cmd = ["lt", "--port", str(port)]
            self.tunnel_process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            
            time.sleep(5)
            
            # Read tunnel URL from output
            output = self.tunnel_process.stdout.read()
            if "your url is:" in output:
                tunnel_url = output.split("your url is:")[1].strip()
                # Extract host for IP resolution
                from urllib.parse import urlparse
                parsed = urlparse(tunnel_url)
                ip = socket.gethostbyname(parsed.hostname)
                return ip, 80, tunnel_url
            else:
                raise Exception("Could not get tunnel URL")
                
        except Exception as e:
            raise Exception(f"LocalTunnel failed: {str(e)}")
            
    def _try_ngrok(self, port):
        """Try ngrok with improved error handling"""
        try:
            from pyngrok import ngrok, conf
            from pyngrok.exception import PyngrokNgrokHTTPError
            
            conf.get_default().monitor_thread = False
            
            try:
                tcp_tunnel = ngrok.connect(port, "tcp")
                ngrok_process = ngrok.get_ngrok_process()
                domain, tunnel_port = tcp_tunnel.public_url[6:].split(":")
                ip = socket.gethostbyname(domain)
                return ip, tunnel_port, tcp_tunnel.public_url
                
            except PyngrokNgrokHTTPError as e:
                if "credit or debit card" in str(e):
                    raise Exception("Ngrok requires credit card for TCP tunnels. Use --no-ngrok or install alternatives.")
                else:
                    raise Exception(f"Ngrok HTTP error: {str(e)}")
                    
        except ImportError:
            raise Exception("pyngrok not installed")
        except Exception as e:
            raise Exception(f"Ngrok failed: {str(e)}")
            
    def _install_cloudflared(self):
        """Install cloudflared based on platform"""
        import platform
        
        system = platform.system().lower()
        if system == "linux":
            # Download and install cloudflared for Linux
            try:
                import wget
                url = "https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64"
                wget.download(url, "/tmp/cloudflared")
                os.chmod("/tmp/cloudflared", 0o755)
                subprocess.run(["sudo", "mv", "/tmp/cloudflared", "/usr/local/bin/"], check=True)
            except:
                print(stdOutput("error") + "\033[1mFailed to install cloudflared. Please install manually.")
                raise Exception("Could not install cloudflared")
        else:
            print(stdOutput("warning") + "\033[1mCloudflared auto-install not supported on this platform.")
            raise Exception("Cloudflared not available")
            
    def close_tunnel(self):
        """Close active tunnel"""
        if self.tunnel_process:
            try:
                self.tunnel_process.terminate()
                self.tunnel_process.wait(timeout=5)
            except:
                self.tunnel_process.kill()
            self.tunnel_process = None
            
        if self.tunnel_type == "ngrok":
            try:
                from pyngrok import ngrok
                ngrok.disconnect(self.tunnel_url)
                ngrok.kill()
            except:
                pass
                
        self.tunnel_url = None
        self.tunnel_type = None
        print(stdOutput("info") + "\033[1mTunnel closed.")


def create_tunnel_with_alternatives(port, prefer_service="auto"):
    """
    Convenience function to create a tunnel with automatic fallback.
    
    Args:
        port: Local port to tunnel
        prefer_service: Preferred tunneling service
        
    Returns:
        TunnelingManager instance with active tunnel, or None if all failed
    """
    manager = TunnelingManager()
    result = manager.create_tunnel(port, prefer_service)
    
    if result:
        return manager, result
    else:
        return None, None