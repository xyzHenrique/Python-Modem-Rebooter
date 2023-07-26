"""
created by: Henrique Rodrigues Pereira <https://github.com/RIick-013>

RIick - ")
"""

SCRIPT_VERSION = "5.2 - 26/07/23"

### Native libraries ###
import traceback
import datetime
import platform
import zipfile
import shutil
import json
import uuid
import os
import re

### Third libraries ###
import colorama

### Local libraries ###
from informations import Informations

class Logger:
    def __init__(self):
        ### Call and initialize third libraries
        colorama.init()

        ### Call and initialize local libraries
        self.structure = json.load(open("structure"))

        ### ... ###
        self.filename_format = "%d-%m"
        self.foldername_format = "%m-%Y" 

        self.file = {
            "file": None,
            "filename": self.get_date(self.filename_format),
            "extension": ".log"
        }

        self.folder = {
            "foldername": self.get_date(self.foldername_format),
            "folderpath": self.structure["Application.Logs"]["dir"]
        }

        self.current_datetime = {
            "date": self.get_time("%d/%m/%Y"),
            "time": self.get_date("%H:%M:%S")
        }

        self.fullpath = f"{self.folder['folderpath']}/{self.folder['foldername']}/{self.file['filename']}{self.file['extension']}"

    def get_date(self, date_format):
        return datetime.datetime.today().strftime(date_format)
        
    def get_time(self, time_format):
        return datetime.datetime.now().strftime(time_format)

    def initialize(self):
        def header():
            self.file["file"] = open(self.fullpath, "w")
            self.file["file"].write(f"""------------------------------------------------------------------------
Logging started at {self.current_datetime['date']} - {self.current_datetime['time']}
File                 : {self.file['filename']}{self.file['extension']}
Version              : {Informations['app_version']}
Computer             : Name: {platform.node()} || Mac: {':'.join(re.findall('..', '%012x' % uuid.getnode()))}
------------------------------------------------------------------------\n""")
            self.file["file"].close()  
        
        if os.path.exists(f"{self.folder['folderpath']}/{self.folder['foldername']}"):
            if os.path.exists(self.fullpath):
                self.compact_folder()
            else:
                header()
                
                self.compact_folder()
        else:
            try:
                os.mkdir(f"{self.folder['folderpath']}/{self.folder['foldername']}")

                header()

                self.compact_folder()

            except Exception:
                print(traceback.format_exc())

    def compact_folder(self):
        try:
            for dir in os.listdir(self.folder["folderpath"]):
                if not dir == self.get_date(self.foldername_format) and not os.path.splitext(dir)[1] == ".zip":
                    zip_file = zipfile.ZipFile(f"{self.folder['folderpath']}/{dir}.zip", "w", zipfile.ZIP_DEFLATED)

                    for root, dirs, files in os.walk(f"{self.folder['folderpath']}/{dir}"):
                        for file in files:
                            zip_file.write(os.path.join(root, file))
                    zip_file.close()

                    shutil.rmtree(f"{self.folder['folderpath']}/{dir}")

        except Exception:
            print(traceback.format_exc())
        
    def write(self, message: str, type=list(["INFO", "WARNING", "CRITICAL", "DEBUG"]), color = True, silence = False):
        str = f"[{self.current_datetime['time']}]: {type} - {message}\n"

        if os.path.exists(self.fullpath):
            self.file["file"] = open(self.fullpath, "a")
            self.file["file"].write(str)
            self.file["file"].close()

            if not silence:
                if color:
                    if type == "INFO":
                        print(colorama.Fore.LIGHTCYAN_EX + str)
                        
                    elif type == "WARNING":
                        print(colorama.Fore.YELLOW + str)
                        
                    if type == "CRITICAL":
                        print(colorama.Fore.RED + str)
                
                    elif type == "DEBUG":
                        print(colorama.Fore.LIGHTMAGENTA_EX + str)

                    if type == "SUCCESS":
                        print(colorama.Fore.LIGHTGREEN_EX + str)
                    
                    print(colorama.Fore.RESET)

                else:
                    print(str)
                
                