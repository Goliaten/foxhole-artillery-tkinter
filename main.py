from tkinter import *
from tkinter import ttk
import math
import cmath
import os

# TODO::
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

def string_var_get_int_or_0_if_empty(string_var):
    if string_var.get() == "":
        return 0
    else:
        try:
            return int(string_var.get())
        except:
            return 0

def get_wind_offset(string_var):
    if string_var.get() in artillery_types.keys():
        return artillery_types[string_var.get()]
    else:
        return 0
        
class Calculator:
    def __init__(self, parent, column, row):
        
        #-- defining and configuring calculator frame --
        frame = ttk.Frame(parent)
        frame.grid(column=column, row=row, sticky=(W, E))
        frame.columnconfigure(0, weight=1)
        frame.columnconfigure(1, weight=1)
        frame.rowconfigure(0, weight=1)
        frame.rowconfigure(1, weight=1)
        frame.rowconfigure(2, weight=1)
        frame.rowconfigure(3, weight=1)
        frame.rowconfigure(4, weight=1)
        
        #-- defining widgets --
        self.azim_label = ttk.Label(frame, text="Azimuth to target")
        self.azim_entry = ttk.Entry(frame, textvariable=azim_var, validate="all", validatecommand=(vcmd, '%P') )
        self.dist_label = ttk.Label(frame, text="Distance to target")
        self.dist_entry = ttk.Entry(frame, textvariable=dist_var, validate="all", validatecommand=(vcmd, '%P') )
        self.wind_azi_label = ttk.Label(frame, text="Wind azimuth")
        self.wind_azi_entry = ttk.Entry(frame, textvariable=wind_azi_var, validate="all", validatecommand=(vcmd, '%P') )
        self.wind_str_label = ttk.Label(frame, text="Wind strength")
        self.wind_str_combo = ttk.Combobox(frame, textvariable=wind_str_var)
        self.wind_str_combo['values'] = [0, 1, 2, 3, 4 ,5]
        self.wind_str_combo.state(['readonly'])
        self.wind_str_combo.current(0)
        
        self.arty_type_label = ttk.Label(frame, text="Artillery type")
        self.arty_type_combo = ttk.Combobox(frame, textvariable=wind_offset_var)
        self.arty_type_combo['values'] = list(artillery_types.keys())
        self.arty_type_combo.state(['readonly'])
        self.arty_type_combo.current(0)
        
        self.submit = ttk.Button(frame, text="calculate", command=self.calculate)
        self.final_azi_label = ttk.Label(frame, textvariable=final_azi)
        self.final_dist_label = ttk.Label(frame, textvariable=final_dist)
        
    def create(self):
        #-- positioning widgets --
        self.azim_label.grid(column=0, row=0, sticky=(E))
        self.azim_entry.grid(column=1, row=0, sticky=(W))
        self.dist_label.grid(column=0, row=1, sticky=(E))
        self.dist_entry.grid(column=1, row=1, sticky=(W))
        self.wind_azi_label.grid(column=0, row=2, sticky=(E))
        self.wind_azi_entry.grid(column=1, row=2, sticky=(W))
        self.wind_str_label.grid(column=0, row=3, sticky=(E))
        self.wind_str_combo.grid(column=1, row=3, sticky=(W))
        self.arty_type_label.grid(column=0, row=4, sticky=(E))
        self.arty_type_combo.grid(column=1, row=4, sticky=(W))
        self.submit.grid(row=5, columnspan=2)
        self.final_azi_label.grid(column=0, row=6, sticky=(E))
        self.final_dist_label.grid(column=1, row=6, sticky=(W))
        
    def calculate(self, *args):
        
        target_location = cmath.rect( string_var_get_int_or_0_if_empty(dist_var), math.radians( string_var_get_int_or_0_if_empty(azim_var) ) )
        wind_offset = cmath.rect( string_var_get_int_or_0_if_empty(wind_str_var) * get_wind_offset(wind_offset_var) , math.radians(string_var_get_int_or_0_if_empty(wind_azi_var)) )
        final_target = cmath.polar( target_location - wind_offset )
        
        final_target = [final_target[0], final_target[1] * 360 / (2 * cmath.pi)]
        # correcting the scope of degrees(from -179 - 180 to 0 - 359)
        # also messing with numbers with e-14 from math.radians(360), and -0.0
        final_target[1] = 0.0 if round(final_target[1], 3) == -0.0 else final_target[1]
        final_target[1] = final_target[1] + 360 if final_target[1] < 0 else final_target[1]
        final_dist.set( round(final_target[0], 2) )
        final_azi.set( round(final_target[1], 2) )
        
        #print(final_target)
        
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
        
        self.calculator = Calculator(frame, 10, 30)
        self.map = Map(frame)
    
    def startup(self):
        
        self.calculator.create()
        self.create_title(self.frame, title="artillery calculator")
        self.create_settings(self.frame)
        
    def create_title(self, frame, column=10, row=10, title="",):
        title = ttk.Label(frame, text=title)
        title.grid(column=column, row=row, columnspan=2)
    
    #later separate this to other function
    def create_settings(self, frame, column=30, row=10):
        
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

#creating string vars
azim_var = StringVar()
dist_var = StringVar()
wind_azi_var = StringVar()
wind_str_var = StringVar()
wind_offset_var = StringVar()
wind_offset_var.set(25)
final_azi = StringVar()
final_dist = StringVar()

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