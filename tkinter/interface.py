"""
Einfache GUI für das Rammsondierungsprogramm

Created by Manuel Schmid, Arbeitsloser Tunichtgut, 7.Februar 2019
"""

import tkinter as tk
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import askdirectory
import matplotlib
matplotlib.use('TkAgg')
from matplotlib import pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import numpy as np
import matplotlib.patches as patches

large_font  = ('Arial Bold', 16)
medium_font = ('Arial', 12)
small_font  = ('Arial', 10)

class Data_provider(object):

    """
    Class which is used to hold data for plotting
    """
    def __init__(self):

        self.data_container = {}
        self.depth_array = 0
        self.nn_data_array = 0
        self.nn_depth_array = 0

        data_string_array = ['filename', 
                            'rms_depth', 
                            'interval',
                            'zero_elevation',
                            'raw_data']
        
        #populate data_container with values
        for d in data_string_array:
            self.data_container[d] = []

class Calculator(object):

    def get_total_depth(self, container):
        """
        calculate total depth from raw_data
        """
        rms_depth = 0 + len(container.data_container['raw_data'] * 0.1) #TODO: contains hardcoded data

        return rms_depth

    def convert_data_to_plot_format(self, container):
        """
        Creates numpy-arrays from the raw input data.
        This needs to be done for plotting.
        """

        #expand depth_array to get a more nearest-neighbour like look
        nn_depth_array = np.arange(0, container.data_container['rms_depth'], 0.1 / 100)
        nn_data_array = np.repeat(container.data_container['raw_data'], 1000)

        return nn_depth_array, nn_data_array
        

class App(tk.Tk):

    """
    Main Class which holds GUI elements
    """

    def __init__(self, *args, **kwargs):


        tk.Tk.__init__(self, *args, **kwargs)

        master_frame = tk.Frame(self)
        master_frame.pack(side = 'top', fill = 'both', expand = True)

        master_frame.grid_rowconfigure(0, weight = 1)
        master_frame.grid_columnconfigure(0, weight = 1)

        #dictionarty which holds all the pages
        self.frames = {}

        for F in (landing_page, figure_page, multiple_figures_page):
            frame = F(master_frame, self)
            self.frames[F] = frame
            frame.grid(row = 0, column = 0, sticky = 'nsew')

        print(self.frames)
        self.show_frame(landing_page)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class landing_page(tk.Frame):
    """
    First Page that pops up if programm is started. 
    """
    def __init__(self, parent, controller):
        
        self.controller = controller

        tk.Frame.__init__(self, parent)

        self.front_label = tk.Label(self, text = "Rammsondier Plotter", font = ("Arial Bold", 16))
        #self.front_label.pack()
        self.front_label.grid(column = 0, row = 0, padx = 50, pady = 15)
        self.button_open_file = tk.Button(
            self, text = 'Öffne .dat Dateien', fg = 'red', command = self.open_file
            )
        self.button_open_file.grid(column = 0, row = 1, pady = 15)

        self.button_load_directory = tk.Button(self, text = 'Öffne Ordner', command=self.open_folder)
        self.button_load_directory.grid(column = 0, row = 2)

    def open_file(self):
        """
        opens up a specific .dat file
        """
        filename = askopenfilename()
        dp.data_container['filename'] = filename
        print('Accessing file: ' + dp.data_container['filename'])
        self.load_data()
        self.controller.show_frame(figure_page)
              
    def open_folder(self):
        """
        opens up a folder, containing .dat files
        """
        foldername = askdirectory()
        self.foldername = foldername

    def load_data(self):
        """
        loads .dat file into data_container and does some calculations
        """
        file = open(dp.data_container['filename'], 'r')
        data = file.readlines()
        file.close()
        data_int = [int(i) for i in data]
        data_int = np.array(data_int)

        dp.data_container['raw_data'] = data_int
        dp.data_container['rms_depth'] = ca.get_total_depth(dp)
        dp.nn_data_array , dp.nn_depth_array = ca.convert_data_to_plot_format(dp)

        #DEBUG
        print(dp.nn_data_array)
        print(dp.data_container['rms_depth'])

class figure_page(tk.Frame):
    def __init__(self, parent, controller):
  
        #add the controller to self.namespace
        self.controller = controller

        #initialize frame and label
        tk.Frame.__init__(self, parent)
        self.figure_label = tk.Label(self, text= 'FIGUREPAGE_SINGLEFIGURE', font = large_font)
        self.figure_label.grid(column = 0, row = 0 )

        #button to navigate back to main_frame
        self.back_button = tk.Button(self, text = 'Back', command = self.back_to_home)
        self.back_button.grid(row = 0, column = 1) 

        self.print_button = tk.Button(self, text = 'Show', command = self.show_figure)
        self.print_button.grid(row = 0, column = 2)

        f = Figure()

    def show_figure(self):
        print('Show figure function was called!')

        print(dp.nn_data_array)

        fig, ax = plt.subplots(1)
        ax.plot(dp.nn_data_array, dp.nn_depth_array)
        canvas = FigureCanvasTkAgg(fig, self)
        canvas.draw()

        canvas.get_tk_widget().grid(column = 1, row = 1, pady = 15)

    def back_to_home(self):
        """
        This probably can get a global function. 
        Navigates back to home
        """
        self.controller.show_frame(landing_page)

class multiple_figures_page(tk.Frame):
    def __init__(self, parent, controller):

        #add the controller to self.namespace
        self.controller = controller

        tk.Frame.__init__(self,parent)
        self.multiple_figures_label = tk.Label(self, text = 'Multiple Figures', font = large_font)
        self.multiple_figures_label.grid(column = 0, row = 0)

        #button to navigate back to main_frame
        self.back_button = tk.Button(self, text = 'Back', command = self.back_to_home)
        self.back_button.grid(row = 0, column = 1)
        
    def back_to_home(self):
        """
        This probably can get a global function. 
        Navigates back to home
        """
        self.controller.show_frame(landing_page)


#initialise data_container class globally
dp = Data_provider()
ca = Calculator()
app = App()

app.mainloop()
#root.destroy()
