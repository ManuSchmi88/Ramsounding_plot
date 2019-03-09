"""
Einfache GUI für das Rammsondierungsprogramm

Created by Manuel Schmid, Arbeitsloser Tunichtgut, 7.Februar 2019
"""

import tkinter as tk
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import asksaveasfilename
from tkinter.filedialog import askdirectory
import matplotlib
matplotlib.use('TkAgg')
from matplotlib import pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import numpy as np
import matplotlib.patches as patches
from os import listdir
from os.path import isfile, join

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
            self.data_container[d] = 0

        self.data_container['interval'] = 0.1
        self.data_container['zero_elevation'] = 0
        self.data_dict = {} #RENAME! Quick and Dirty!!!

class Calculator(object):

    def get_total_depth(self, container):
        """
        calculate total depth from raw_data
        """
        rms_depth = container.data_container['zero_elevation'] + float(int(len(container.data_container['raw_data'])) * 0.1) #TODO: contains hardcoded data
        
        return float(rms_depth)

    def get_total_depth_raw(self, data):
        """
        calculate total depth from raw_data
        TODO: Refactor. This is getting really messy.
        This function does not take the dp container input but can handle
        raw input data which is passed as argument
        """
        rms_depth_raw = 0 + float(int(len(data)) * 0.1) #TODO: contains hardcoded data
        
        return float(rms_depth_raw)

    def convert_data_to_plot_format(self, container):
        """
        Creates numpy-arrays from the raw input data.
        This needs to be done for plotting.
        """

        #expand depth_array to get a more nearest-neighbour like look
        nn_depth_array = np.arange(0, container.data_container['rms_depth'], container.data_container['interval'] / 100)
        nn_data_array = np.repeat(container.data_container['raw_data'], 100)

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

        for F in (landing_page, figure_page, folder_print_page):
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
        self.front_label.grid(column = 0, row = 0, padx = 50)
        self.button_open_file = tk.Button(
            self, text = 'Öffne .dat Dateien', fg = 'red', command = self.open_file)
        self.button_open_file.grid(column = 0, row = 1)

        self.button_load_directory = tk.Button(self, text = 'Öffne Ordner', command=self.open_folder)
        self.button_load_directory.grid(column = 0, row = 2)

    def open_file(self):
        """
        opens up a specific .dat file
        """
        filename = askopenfilename()
        dp.data_container['filename'] = filename
        print('Accessing file: ' + dp.data_container['filename'])
        self.append_data_to_class(self.load_data(filename))
        self.controller.show_frame(figure_page)
              
    def open_folder(self):
        """
        opens up a folder, containing .dat files
        """
        folderpath = askdirectory()
        self.folderpath = folderpath

        #create an array which contains all filenames in the folder as strs
        #ignores sub-directories
        filename_array = [name for name in listdir(self.folderpath) if isfile(join(self.folderpath, name))]
    
        #create a dictionary which holds the filename and the loaded data
        #exp_dict = {
        #   'rs1.dat' : [1 , 2 , 3 , 6 , 10, 5]   
        #           }

        for file in filename_array:
            path_to_file = str(self.folderpath + '/' +file)
            dp.data_dict[file] = self.load_data(path_to_file)

        self.controller.show_frame(folder_print_page)


    def load_data(self, filename):
        """
        loads .dat file into data_container and does some calculations
        """
        #file = open(dp.data_container['filename'], 'r')
        file = open(filename, 'r')
        data = file.readlines()
        file.close()
        data_int = [int(i) for i in data]
        data_int = np.array(data_int)

        #dp.data_container['raw_data'] = data_int
        #dp.data_container['rms_depth'] = ca.get_total_depth(dp)
        #dp.nn_depth_array , dp.nn_data_array = ca.convert_data_to_plot_format(dp)

        return data_int

    def append_data_to_class(self, data):
        '''
        TODO: Revisit this function. Quick and dirty solution.
        '''
        dp.data_container['raw_data'] = data
        dp.data_container['rms_depth'] = ca.get_total_depth(dp)
        dp.nn_depth_array , dp.nn_data_array = ca.convert_data_to_plot_format(dp)



class folder_print_page(tk.Frame):
    '''
    Create a page that asks what options you want to use for 
    creating multiple figures
    '''

    def __init__(self, parent, controller):

        #add the controller to self.namespace
        self.controller = controller

        self._depth = 0
        self._data = 0

        #initialize frame and label
        tk.Frame.__init__(self, parent)
        self.figure_label = tk.Label(self, text= 'Marius stinkt. Scheiss Programm', font = large_font)
        self.figure_label.grid(column = 0, row = 0 )

        #button to navigate back to main_frame
        self.back_button = tk.Button(self, text = 'Back', command = self.back_to_home)
        self.back_button.grid(row = 0, column = 4) 

        self.print_button = tk.Button(self, text = 'Save', command = self.save_figure)
        self.print_button.grid(row = 0, column = 3)

        self.color_bool = tk.IntVar()
        self.color_check = tk.Checkbutton(self, text="Colorcoding", variable=self.color_bool)
        self.color_check.grid(row = 4, column = 4)

        self.fill_between_bool = tk.IntVar()
        self.fill_check = tk.Checkbutton(self, text = "Fill between", variable = self.fill_between_bool)
        self.fill_check.grid(row = 4, column = 2)

        self.grid_bool = tk.IntVar()
        self.grid_check = tk.Checkbutton(self, text = "Grid", variable = self.grid_bool)
        self.grid_check.grid(row = 4, column = 3)

        #self.create_individual_plot(dp.data_dict)

    def save_figure(self):
    
        print('save_figure function was called!')

        #filename = asksaveasfilename()
        #plt.savefig(str(filename))

        self.create_individual_plot(dp.data_dict)
            

    def create_individual_plot(self, data):

        for keys in data:
            self._depth = ca.get_total_depth_raw(dp.data_dict[keys])
            self._data  = dp.data_dict[keys]

            _depth_nn = np.arange(0, self._depth, 0.1 / 100)
            _data_nn  = np.repeat(self._data , 100)


            fig, ax = plt.subplots(1)
            ax.plot(_data_nn, _depth_nn, 'k', linewidth = 2.3)
            ax.set_xlim([0,10])
            lower_ylim = round(self._depth + 0.5)
            ax.set_ylim([lower_ylim, 0])
            ax.xaxis.tick_top()
            ax.set_xlabel("Schlagzahl", fontsize = 18)
            ax.set_ylabel("Tiefe [m]", fontsize = 18)
            plt.savefig(str(f'test_{keys}.png'))

    
    def back_to_home(self):
        """
        This probably can get a global function. 
        Navigates back to home
        """
        #plt.close(self.fig)
        self.controller.show_frame(landing_page)


class figure_page(tk.Frame):

    def __init__(self, parent, controller):
  
        #add the controller to self.namespace
        self.controller = controller

        #initialize frame and label
        tk.Frame.__init__(self, parent)
        self.figure_label = tk.Label(self, text= 'Schlagzahl Auswertung', font = large_font)
        self.figure_label.grid(column = 0, row = 0 )

        #button to navigate back to main_frame
        self.back_button = tk.Button(self, text = 'Back', command = self.back_to_home)
        self.back_button.grid(row = 0, column = 4) 

        self.print_button = tk.Button(self, text = 'Show', command = self.show_figure)
        self.print_button.grid(row = 0, column = 2)

        self.print_button = tk.Button(self, text = 'Save', command = self.save_figure)
        self.print_button.grid(row = 0, column = 3)

        self.color_bool = tk.IntVar()
        self.color_check = tk.Checkbutton(self, text="Colorcoding", variable=self.color_bool)
        self.color_check.grid(row = 4, column = 4)

        self.fill_between_bool = tk.IntVar()
        self.fill_check = tk.Checkbutton(self, text = "Fill between", variable = self.fill_between_bool)
        self.fill_check.grid(row = 4, column = 2)

        self.grid_bool = tk.IntVar()
        self.grid_check = tk.Checkbutton(self, text = "Grid", variable = self.grid_bool)
        self.grid_check.grid(row = 4, column = 3)

        self.show_figure()

    def show_figure(self):

        print('show_figure function was called!')

        self.fig, self.ax = plt.subplots(1)
        self.ax.plot(dp.nn_data_array, dp.nn_depth_array, 'k', linewidth = 2.3)
        self.ax.set_xlim([0,10])
        lower_ylim = round(dp.data_container['rms_depth'] + 0.5)
        self.ax.set_ylim(lower_ylim,0)
        self.ax.xaxis.tick_top()

        self.ax.set_xlabel("Schlagzahl", fontsize = 18)
        self.ax.set_ylabel("Tiefe [m]", fontsize = 18)

        canvas = FigureCanvasTkAgg(self.fig, self)
        canvas.draw()
        canvas.get_tk_widget().grid(column = 1, row = 1, pady = 15)
        #toolbar = NavigationToolbar2Tk(canvas, self)
        #toolbar.update()
        if self.color_bool.get() == 1:
            self.colorcode_indices(self.fig, self.ax)

        if self.fill_between_bool.get() == 1:
            self.fill_between(self.fig, self.ax)

        if self.grid_bool.get() == 1:
            self.with_grid(self.fig, self.ax)

    def save_figure(self):

        print('save_figure function was called!')

        filename = asksaveasfilename()
        plt.savefig(str(filename))

    def colorcode_indices(self, fig, ax):
        """
        If this function is called the figure will be colorcoded 
        according to the different "steifigkeits-indizes"

        weich : 0 - 4
        breiig: 4 - 8
        steif:  8 - 14
        halbfest: 14 - 28
        fest: > 28
        """

        print('colorcode function was called')

        _data = dp.nn_data_array
        weich_indices    = np.where(np.logical_and(_data >= 0, _data < 4))
        breiig_indices   = np.where(np.logical_and(_data >= 4, _data < 8))
        steif_indices    = np.where(np.logical_and(_data >= 8, _data < 14))
        halbfest_indices = np.where(np.logical_and(_data >= 14, _data < 28))
        fest_indices     = np.where(_data >= 28)


        for i in weich_indices:
            ax.hlines(dp.nn_depth_array[i],dp.nn_data_array[i] ,90, alpha = 0.01)
        for i in breiig_indices:
            ax.hlines(dp.nn_depth_array[i],dp.nn_data_array[i] ,90, alpha = 0.01, color = 'blue')
        for i in steif_indices:
            ax.hlines(dp.nn_depth_array[i],dp.nn_data_array[i] ,90, alpha = 0.01, color = 'magenta')
        for i in halbfest_indices:
            ax.hlines(dp.nn_depth_array[i],dp.nn_data_array[i] ,90, alpha = 0.01, color = 'yellow')
        for i in fest_indices:
            ax.hlines(dp.nn_depth_array[i],dp.nn_data_array[i] ,90, alpha = 0.02, color = 'red')


    def fill_between(self, fig, ax):
        """
        If box is checked, it fills the space between the y-axis and the values
        """
        ax.fill_betweenx(dp.nn_depth_array, dp.nn_data_array, hatch = '/', color = 'k', alpha = 0.3)

    def with_grid(self, fig, ax):
        """
        If box is checked, plot gets a grid
        """
        ax.grid(linewidth = 1.2)

    def add_label_automatically(self, fig, ax):
        """
        add a label, the first time we have 50cm of a specific ground e.g steif
        """

        print("This is going to be complicated")

    def back_to_home(self):
        """
        This probably can get a global function. 
        Navigates back to home
        """
        #plt.close(self.fig)
        self.controller.show_frame(landing_page)

#initialise data_container class globally
if __name__ == '__main__':
    dp = Data_provider()
    ca = Calculator()
    app = App()

app.mainloop()
#root.destroy()
