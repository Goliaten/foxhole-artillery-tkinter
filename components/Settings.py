from tkinter import *
from tkinter import ttk

class Settings:
    def __init__(self, root):
        
        # https://tkdocs.com/tutorial/windows.html#wm
        
        dlg = Toplevel(root)
        self.dlg = dlg
        
        dlg.title("Settings")
        dlg.geometry("200x200")
        dlg.minsize(250, 100)
        dlg.protocol("WM_DELETE_WINDOW", self.destroy)
        dlg.attributes("-topmost", 1)
        
        dlg.iconify()
     
    def create(self):
        pass
    
    def destroy(self):
        self.dlg.grab_release()
        self.dlg.destroy()
    
    def load_settings():
        pass
    
    def save_settings():
        pass
    
    def exit_cancel():
        pass
    
    def exit_save():
        pass
    
    
    
    