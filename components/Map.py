from tkinter import *
from tkinter import ttk

class Map:
    def __init__(self, parent):
        
        return
        
        #temporary variable, later replace with string_var
        image_name= os.path.dirname(os.path.realpath(__file__)) + "\\maps\\MapAcrithiaHex.png"
        print(image_name)
        
        #-- defining and configuring map frame --
        frame = ttk.Frame(parent)
        frame.grid(column=1, row=0, sticky=(W, E))
        frame.columnconfigure(0, weight=1)
        frame.rowconfigure(0, weight=1)
        frame.rowconfigure(1, weight=1)
        
        test = ttk.Label(frame, text="test map text")
        
        image = PhotoImage(file=image_name)
        image = image.subsample(3) # https://stackoverflow.com/questions/6582387/image-resize-under-photoimage
        
        
        
        image_label = ttk.Label(frame, image=image)
        image_label.image = image
        
        test.grid(column=0, row=0)
        image_label.grid(column=0, row=1, sticky="NSEW")