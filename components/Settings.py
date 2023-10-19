from tkinter import *
from tkinter import ttk
import os.path
from os import name
import json

#getting the directory division sign used in OS
def sign():
    if name == "posix":
        return "/"
    else:
        return "\\"

def dprint(text, nl=True):
    if(debug):
        if nl:
            print("\r\n", text)
            return
        print(text)

sgn = sign()
debug = True

class Settings:
    def __init__(self, root):
        
        # https://tkdocs.com/tutorial/windows.html#wm
        
        self.settings_framework = "settings_framework.json"
        self.settings = "settings.json"
        
        self.string_vars = {}
        self.root = root
        self.created = False
        self.allowed_widgets = ["radio", "check", "combo"]
        
        #------------------------------------------------------------
        #have predefined structure or load structure from file for settings?
        #prob have it predefined with default variables, and overwrite them with settings, to prevent any missing
        #but then again, predefined in here, or in separate file?
        #in separate file easier for management, here more "secure"
        #take separate file approach
        #plus you can put there types of fields for each setting, and have them taken to different variable
        
        self.startup()
     
    def create(self):
        
        dlg = Toplevel(self.root)
        self.dlg = dlg
        self.frame = ttk.Frame(self.dlg)
        
        dlg.title("Settings")
        dlg.geometry("200x200")
        dlg.minsize(250, 100)
        dlg.protocol("WM_DELETE_WINDOW", self.destroy)
        dlg.attributes("-topmost", 1)
        
        self.created = True
    
    def destroy(self):
        try:
            self.dlg.grab_release()
            self.dlg.destroy()
            self.created = False
        except Exception as e:
            print(e)
    
    def add_field(self, widg_type, name, caption):
        
        if widg_type not in self.allowed_widgets:
            print(f"Err - {widg_type} not in allowed widgets. {name} {caption}")
            return
        
        if self.created:
            if widg_type == "radio":
                pass #--------------------------------------------------------
            else:
                print("not implemented yet")
    
    def startup(self):
        framework = {}
        settings = {}
        
        # if settings file exists
        if os.path.isfile(f"components{sgn}{self.settings_framework}"):
            dprint("Loading framework")
            framework = self.load_framework()
        else:
            dprint("Framework not present")
            #idc right now to do it, maybe set some flag, to go different path
            #i dont wanna do large if blocks
            pass
        
        print(framework)
        
        if os.path.isfile(f"{self.settings}"):
            dprint("Loading settings")
            settings = self.load_settings()
        else:
            dprint("settings not present")
            settings = self.create_settings(framework)
            
        dprint(settings)
            
        input("now we wait")
            
    
    def load_settings(self):
        
        with open(self.settings, "r") as file:
            return json.loads(file.read())
        
    
    def save_settings(self):
        pass
        
    def load_framework(self):
    
        with open(f"components{sgn}{self.settings_framework}", 'r') as file:
            return json.loads(file.read())
    
    def create_settings(self, framework):
        
        settings = {}
        
        for f_key, f_entry in framework.items():
            
            #dprint(f"{f_key}, {f_entry}", False)
            
            if f_entry[0] == "radio":
                # from framework we take the item setting, get the correct item, and take the value of it
                settings[f_key] = framework[f"_{f_key}"] [f_entry[2]] [0]
                
            elif f_entry[0] == "check":
                settings[f_key] = f_entry[2]
                
            elif f_entry[0] == "combo":
                settings[f_key] = framework[f"_{f_key}"] [f_entry[2]] [0]
                
            elif f_key[0] == "_":
                #skippings item settings, as they are directly accessed by their refferenced settings
                continue
                
            else:
                dprint("unknown setting type: " + f_key)
                pass
                
        #dprint(settings, False)
        
        with open(self.settings, "w") as file:
            file.write( json.dumps(settings, indent=4) )
            
        return settings
        
    def create_widgets(self):
        pass
    
    def exit_cancel(self):
        pass
    
    def exit_save(self):
        pass
    
    
    
    