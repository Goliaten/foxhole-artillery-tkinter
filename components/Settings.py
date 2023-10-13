from tkinter import *
from tkinter import ttk

class Settings:
    def __init__(self, root):
        
        # https://tkdocs.com/tutorial/windows.html#wm
        
        self.string_vars = {}
        self.root = root
        self.created = False
        self.allowed_widgets = ["radio", "checkbox", "combobox"]
        self.settings = {}#------------------------------------------------------------
        #have predefined structure or load structure from file for settings?
        #prob have it predefined with default variables, and overwrite them with settings, to prevent any missing
        #but then again, predefined in here, or in separate file?
        #in separate file easier for management, here more "secure"
        #take separate file approach
     
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
    
    def load_settings():
        pass#--------------------------------------------------------------
    
    def save_settings():
        pass
    
    def exit_cancel():
        pass
    
    def exit_save():
        pass
    
    
    
    