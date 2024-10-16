import platform
import ctypes
import os
from datetime import datetime

def isWindows():
    if platform.system() == "Windows":
        return True
    else:
        print("[ERROR] This action only supports Windows operating systems")
        return False

def isAdmin():
    if ctypes.windll.shell32.IsUserAnAdmin():
        return True
    else:
        print("[ERROR] This action requires administrative privileges")
        return False

def getPath():
    dest_path = input("[USERINPUT] Enter the artifact destination path: ")

    if os.path.exists(dest_path):
        timestamp = datetime.now().strftime(f"%Y%m%d%H%M%S")
        dest_path = os.path.join(dest_path, timestamp)
        os.makedirs(os.path.join(dest_path, "registry"), exist_ok=True)
        return dest_path
    else:
        print("[ERROR] Path does not exist")
        return False