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
    if debug:
        if nl:
            print("\r\n", text)
            return
        print(text)

def dinput(text=""):
    if debug:
        input(text)

sgn = sign()
debug = True

class Settings:

    def __init__(self, root):
        
        # https://tkdocs.com/tutorial/windows.html#wm
        
        self.settings_framework_filename = "settings_framework.json"
        self.settings_filename = "settings.json"
        
        self.settings = {}
        self.framework = {}
        self.string_vars = {}
        self.root = root
        self.created = False
        self.allowed_widgets = ["radio", "check", "combo"]
        self.settings_count = 0
        self.pop_offset_x = 20
        self.pop_offset_y = 20
        self.settings_file_verified = False
     
    def create(self):
        
        dlg = Toplevel(self.root)
        dlg.protocol("WM_DELETE_WINDOW", self.destroy) # catch the close button
        dlg.resizable(FALSE, FALSE) # disable resize
        dlg.lift(self.root) # elevating window above rooot
        print( 'c',  self.root.winfo_geometry() )
        dlg.geometry(f'{dlg.winfo_width()}x{dlg.winfo_height()}+{self.root.winfo_x()+self.pop_offset_x}+{self.root.winfo_y()+self.pop_offset_y}')
        dlg.update()
        self.dlg = dlg
        
        
        self.frame = ttk.Frame(self.dlg)
        self.frame.grid(column=0, row=0)
        
        dlg.title("Settings")
        dlg.geometry("200x200")
        dlg.minsize(250, 100)
        dlg.protocol("WM_DELETE_WINDOW", self.destroy)
        dlg.attributes("-topmost", 1)
        
        self.created = True
        
        self.startup()
    
    def destroy(self):
        try:
            self.dlg.grab_release()
            self.dlg.destroy()
            self.created = False
        except Exception as e:
            print('Settings.destroy exception')
            print(e)
    
    def startup(self):
        framework, settings = self.verify_settings_file()
        
        self.add_footer()
        
        self.settings = settings
        self.framework = framework
    
    def verify_settings_file(self, internal=True):
        # disabling internal flag causes settings to not create widgets
        framework = {}
        settings = {}
        
        dprint("verifying settings")
        # load framework if exists
        if os.path.isfile(f"components{sgn}{self.settings_framework_filename}"):
            dprint("Loading framework")
            framework = self.load_framework()
        else:
            dprint("Framework not present")
            #idc right now to do it, maybe set some flag, to go different path
            #i dont wanna do large if blocks
            pass
        
        #------------------------------------------------------------------------------------------------------------------------------------------------------------------
        
        #      Hold on, we load settings, but we dont know, if they didnt change, or are correct in terms of keys - values. Need to validate 
        #      check if we can add save settings not present
        #      check if we can throw out settings not needed
        
        #------------------------------------------------------------------------------------------------------------------------------------------------------------------

        #load settings if exist, else make them
        if os.path.isfile(f"{self.settings_filename}"):
            dprint("Loading settings")
            settings = self.load_settings()
        else:
            dprint("Creating settings")
            settings = self.create_settings(framework)
        
        if internal:
            #create widgets if framework is loaded
            if framework:
                dprint("Creating widgets")
                self.create_widgets(framework, settings)
            else:
                dprint("Can't create settings with no framework")
        
        dprint("settings verification complete")
        
        return framework, settings
    
    def load_settings(self):
        
        with open(self.settings_filename, "r") as file:
            return json.loads(file.read())
    
    def load_settings_ext(self):
        if not self.settings_file_verified:
            self.settings_file_verified = True
            return self.verify_settings_file(False)[1]
        else:
            return self.load_settings()
        
    
    def load_framework(self):
    
        with open(f"components{sgn}{self.settings_framework_filename}", 'r') as file:
            return json.loads(file.read())
    
    def create_settings(self, framework):
        
        settings = {}
        
        for f_key, f_entry in framework.items():
            
            if f_key[0] == "_":
                #skippings item settings, as they are directly accessed by their refferenced settings
                continue
                
            elif f_entry[0] == "radio":
                # from framework we take the item setting, get the correct item, and take the value of it
                settings[f_key] = framework[f"_{f_key}"] [f_entry[2]] [0]
                
            elif f_entry[0] == "check":
                settings[f_key] = f_entry[2]
                
            elif f_entry[0] == "combo":
                settings[f_key] = framework[f"_{f_key}"] [f_entry[2]]
                
            else:
                dprint("unknown setting type: " + f_key)
                pass
        
        with open(self.settings_filename, "w") as file:
            file.write( json.dumps(settings, indent=4) )
            
        return settings
        
    def create_widgets(self, framework, settings):
        
        for f_key, f_entry in framework.items():
            
            
            if f_key[0] == "_":
                continue
            
            elif f_entry[0] == "radio":
                if f_key in settings.keys():
                
                    item_key_list = [x[0] for x in framework[f"_{f_key}"]]
                    dprint(f"- {f_entry[0]=} {f_key=} {settings[f_key]=}  {item_key_list=}")
                    
                    if settings[f_key] in item_key_list:
                    
                        item_index = item_key_list.index(settings[f_key])
                        self.add_field("radio", f_key, f_entry[1], item_index, framework[f"_{f_key}"])
                        
                    else:
                        # redundant line, but for now to keep logic in my head, I want to leave it
                        self.add_field("radio", f_key, f_entry[1], f_entry[2], framework[f"_{f_key}"])
                        
                else:
                    self.add_field("radio", f_key, f_entry[1], f_entry[2], framework[f"_{f_key}"])
                    
                
            elif f_entry[0] == "check":
                if f_key in settings.keys():
                    dprint(f"- {f_entry[0]=} {f_key=} {settings[f_key]=}")
                    self.add_field("check", f_key, f_entry[1], settings[f_key])
                else:
                    self.add_field("check", f_key, f_entry[1], f_entry[2])
                
            elif f_entry[0] == "combo":
            
                if f_key in settings.keys():
                
                    item_key_list = framework[f"_{f_key}"]
                    dprint(f"- {f_entry[0]=} {f_key=} {settings[f_key]=}  {item_key_list=}")
                    
                    if settings[f_key] in item_key_list:
                    
                        item_index = item_key_list.index(settings[f_key])
                        self.add_field("combo", f_key, f_entry[1], item_index, framework[f"_{f_key}"])
                        
                    else:
                        # redundant line, but for now to keep logic in my head, I want to leave it
                        self.add_field("combo", f_key, f_entry[1], f_entry[2], framework[f"_{f_key}"])
                        
                else:
                    self.add_field("combo", f_key, f_entry[1], f_entry[2], framework[f"_{f_key}"])
                
            else:
                dprint("unknown setting type: " + f_key)
    
    def add_field(self, widg_type, name, caption, default, items=[]):
        
        #dprint(f"{widg_type}, {name}, {caption}, {default}, {items}")
        
        
        # for now, handling grid will be separate
        self.frame.rowconfigure(self.settings_count, weight=1)
        subframe = ttk.Frame(self.frame)
        subframe.grid(column=0, row=self.settings_count, sticky=(W))
        subframe.columnconfigure(0, weight=1)
        subframe.columnconfigure(1, weight=1)
        
        if widg_type not in self.allowed_widgets:
            print(f"Err - {widg_type} not in allowed widgets. {name} {caption}")
            return
        
        if self.created:
            if widg_type == "check":
            
                var = StringVar()
                var.set(default)
                self.string_vars[name] = var
                
                ttk.Label(subframe, text=caption).grid(column=0, row=0)
                ttk.Checkbutton(subframe, variable=var).grid(column=1, row=0)
                
            elif widg_type == "combo":
                
                var = StringVar()
                var.set(items[default])
                self.string_vars[name] = var
                
                ttk.Label(subframe, text=caption).grid(column=0, row=0)
                widget = ttk.Combobox(subframe, textvariable=var)
                widget.grid(column=1, row=0)
                widget['values'] = items
                widget.state(['readonly'])
                widget.bind('<<ComboboxSelected>>', self.combobox_clear)
                
            elif widg_type == "radio":
            
                var = StringVar()
                self.string_vars[name] = var
                
                label_frame = ttk.Labelframe(subframe, text=caption)
                label_frame.grid(column=0, row=0)
                for y, x in enumerate(items):
                    label_frame.rowconfigure(y, weight=1)
                    ttk.Radiobutton(label_frame, text=x[1], variable=var, value=x[0]).grid(column=1, row=y)
                    if x[0] == items[default][0]:
                        var.set(x[0])
                
                
            
            else:
                print("not implemented")
                return
        
        self.settings_count += 1
    
    def add_footer(self):
        
        self.frame.rowconfigure(self.settings_count, weight=1) # this is the last row, so no need to increment settings_count
        subframe = ttk.Frame(self.frame)
        subframe.grid(column=0, row=self.settings_count)
        subframe.columnconfigure(0, weight=1)
        subframe.columnconfigure(1, weight=1)
        
        save = ttk.Button(subframe, text="save", command=self.click_save)
        save.grid(column=0, row=0, sticky=[E])
        
        cancel = ttk.Button(subframe, text="exit", command=self.click_exit)
        cancel.grid(column=1, row=0, sticky=[W])
    
    def save_settings(self):
        self.settings = self.get_settings()
        with open(self.settings_filename, "w") as file:
            file.write( json.dumps(self.settings, indent=4) )
    
    def click_save(self, *event):
        
        self.save_settings()
        print(self.settings)
        print("save")
    
    def click_exit(self, *event):
        self.destroy()
        print("exit")
        
    def combobox_clear(self, event):
        event.widget.selection_clear()
    
    def get_settings(self):
        
        out = {}
        for key, value in self.string_vars.items():
            out[key] = value.get()
        
        return out
        
    
    