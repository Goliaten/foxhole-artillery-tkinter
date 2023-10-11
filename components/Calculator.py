from tkinter import *
from tkinter import ttk
import math
import cmath

def string_var_get_int_or_0_if_empty(string_var):
    if string_var.get() == "":
        return 0
    else:
        try:
            return int(string_var.get())
        except:
            return 0


def get_wind_offset(string_var, artillery_types):
    if string_var.get() in artillery_types.keys():
        return artillery_types[string_var.get()]
    else:
        return 0

class Calculator:
    def __init__(self, parent, column, row, validator, artillery_types):
        
        #creating string vars
        self.azim_var = StringVar()
        self.dist_var = StringVar()
        self.wind_azi_var = StringVar()
        self.wind_str_var = StringVar()
        self.wind_offset_var = StringVar()
        self.wind_offset_var.set(25)
        self.final_azi = StringVar()
        self.final_dist = StringVar()
        
        self.artillery_types = artillery_types
        
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
        self.azim_entry = ttk.Entry(frame, textvariable=self.azim_var, validate="all", validatecommand=(validator, '%P') )
        self.dist_label = ttk.Label(frame, text="Distance to target")
        self.dist_entry = ttk.Entry(frame, textvariable=self.dist_var, validate="all", validatecommand=(validator, '%P') )
        self.wind_azi_label = ttk.Label(frame, text="Wind azimuth")
        self.wind_azi_entry = ttk.Entry(frame, textvariable=self.wind_azi_var, validate="all", validatecommand=(validator, '%P') )
        self.wind_str_label = ttk.Label(frame, text="Wind strength")
        self.wind_str_combo = ttk.Combobox(frame, textvariable=self.wind_str_var)
        self.wind_str_combo['values'] = [0, 1, 2, 3, 4 ,5]
        self.wind_str_combo.state(['readonly'])
        self.wind_str_combo.current(0)
        
        self.arty_type_label = ttk.Label(frame, text="Artillery type")
        self.arty_type_combo = ttk.Combobox(frame, textvariable=self.wind_offset_var)
        self.arty_type_combo['values'] = list(artillery_types.keys())
        self.arty_type_combo.state(['readonly'])
        self.arty_type_combo.current(0)
        
        self.submit = ttk.Button(frame, text="calculate", command=self.calculate)
        self.final_azi_label = ttk.Label(frame, textvariable=self.final_azi)
        self.final_dist_label = ttk.Label(frame, textvariable=self.final_dist)
        
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
        
        target_location = cmath.rect( string_var_get_int_or_0_if_empty(self.dist_var), math.radians( string_var_get_int_or_0_if_empty(self.azim_var) ) )
        wind_offset = cmath.rect( string_var_get_int_or_0_if_empty(self.wind_str_var) * get_wind_offset(self.wind_offset_var, self.artillery_types) , math.radians(string_var_get_int_or_0_if_empty(self.wind_azi_var)) )
        final_target = cmath.polar( target_location - wind_offset )
        
        final_target = [final_target[0], final_target[1] * 360 / (2 * cmath.pi)]
        # correcting the scope of degrees(from -179 - 180 to 0 - 359)
        # also messing with numbers with e-14 from math.radians(360), and -0.0
        final_target[1] = 0.0 if round(final_target[1], 3) == -0.0 else final_target[1]
        final_target[1] = final_target[1] + 360 if final_target[1] < 0 else final_target[1]
        self.final_dist.set( round(final_target[0], 2) )
        self.final_azi.set( round(final_target[1], 2) )
        
    def get_var():
        pass