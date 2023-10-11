from tkinter import *
from tkinter import ttk
import math
import cmath
import os
from components.Map import Map
from components.Calculator import Calculator
from components.Settings import Settings

# TODO:
# in map initialise, map name, make it cross platform
# allos user to write fractions, and negatives
# prettify the calculator / styles
# make it so after every Enter clicked, the focus goes to next Entry
# options/settings
# - digits to round in Calculator.calculate - int
# map
# connection to foxhole api
# compile script to exe

    
    
def callback(P):
    if str.isdigit(P) or P == "":
        return True
    else:
        return False

class Main:
    def __init__(self, parent):
        frame = ttk.Frame(parent)
        frame.grid(column=0, row=0, sticky=(N, W, E, S))
        frame.columnconfigure(10, weight=4)
        frame.columnconfigure(20, weight=5)
        frame.columnconfigure(30, weight=1)
        frame.rowconfigure(10, weight=1)
        frame.rowconfigure(20, weight=1)
        frame.rowconfigure(30, weight=9)
        self.frame = frame
        
        #ttk.Label(frame, text="test", borderwidth=2, relief="raised").grid(column=10, row=10, sticky=(N, W, E, S))
        #ttk.Label(frame, text="test", borderwidth=2, relief="raised").grid(column=10, row=20, sticky=(N, W, E, S))
        #ttk.Label(frame, text="test", borderwidth=2, relief="raised").grid(column=10, row=30, sticky=(N, W, E, S))
        #ttk.Label(frame, text="test", borderwidth=2, relief="raised").grid(column=20, row=10, sticky=(N, W, E, S))
        #ttk.Label(frame, text="test", borderwidth=2, relief="raised").grid(column=20, row=20, sticky=(N, W, E, S))
        #ttk.Label(frame, text="test", borderwidth=2, relief="raised").grid(column=20, row=30, sticky=(N, W, E, S))
        #ttk.Label(frame, text="test", borderwidth=2, relief="raised").grid(column=30, row=10, sticky=(N, W, E, S))
        #ttk.Label(frame, text="test", borderwidth=2, relief="raised").grid(column=30, row=20, sticky=(N, W, E, S))
        #ttk.Label(frame, text="test", borderwidth=2, relief="raised").grid(column=30, row=30, sticky=(N, W, E, S))
        
        self.calculator = Calculator(frame, 10, 30, vcmd, artillery_types)
        self.map = Map(frame)
        //self.settings = Settings(frame)
    
    def startup(self):
        
        self.calculator.create()
        self.create_title(self.frame, title="artillery calculator")
        self.create_settings_icon(self.frame)
        
        
    def create_title(self, frame, column=10, row=10, title="",):
        title = ttk.Label(frame, text=title)
        title.grid(column=column, row=row, columnspan=2)
    
    #later separate this to other function
    def create_settings_icon(self, frame, column=30, row=10):
        
        image_name= os.path.dirname(os.path.realpath(__file__)) + "\\assets\\cog.png"
        image = PhotoImage(file=image_name)
        image = image.subsample(12) # https://stackoverflow.com/questions/6582387/image-resize-under-photoimage
        
        image_label = ttk.Label(frame, image=image)
        image_label.image = image
        image_label.grid(column=column, row=row, sticky=(N,W,E,S))

root = Tk()
root.title("Artillery calculator")
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

#creating number only validator
vcmd = root.register(callback)


artillery_types = {
    'Mortar' : 5,
    '120mm Gunboat' : 10,
    '120-68 Koronides Field Gun' : 25,
    'Huber Lariat 120mm' : 25,
    '50-500 Thunderbolt Cannon' : 25,
    'Hubel Exalt 150mm' : 25,
    'Rycker 4/3-F Wasp Nest' : 10,
    'Niska-Rycker MK. IX Skycaller' : 10,
    'DAE 3B-2 Hades Net' : 10,
    'R-17 Retiarius Skirmisher' : 10,
    'King Jester - MK. I-1' : 10,
    'T13 Deioneus Rocket Battery' : 10,
    'Storm Cannon' : 50,
    'Tempest Cannon RA-2' : 50,
}


#creating frames
mainframe = ttk.Frame(root, padding=3)
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
mainframe.columnconfigure(0, weight=1)
mainframe.rowconfigure(0, weight=1)

main = Main(mainframe)
main.startup()

#initialising components
#calculator = Calculator(mainframe)
#map = Map(mainframe)

root.mainloop()