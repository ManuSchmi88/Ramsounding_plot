#import necessary libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches

def open_file(filename, filetype = 'ascii'):
    '''
    Opens the specified file

    input:
        filename : path to the file you want to open
        filetype : 'ascii'
                   'xls'
                   defines the filetype you are using. 
                   TODO: implement xls capability
    '''

    if filetype == 'ascii':    
        file = open(filename, 'r')
        data = file.readlines()
        file.close()
    elif filetype == 'xls':
        print('Reading Excel files is not yet implemented.')
    else:
        print('Wrong filetype.')
    
    return data

def convert_to_int(data):
    '''
    Convert data from datafile to ints. 
    N10-values are always of type(int) so its ok.
    '''
    data = [int(i) for i in data]

    return data

class ramsounding(self):
    '''
    Create class which holds the information about a individual ramsounding.
    This can/needs to go somewhere else later.
    '''

    def __init__(self, rs_type,  zero_elevation = 0):
        '''
        input parameters: 

        rs_type :   DPL - Light Ramsounding
                    DPM - Medium Ramsounding
                    DPH - Heavy Ramsounding

        zero_elevation: Defines in which depth you started counting your N10 values
        '''

        self.rs_type = rs_type
        self.zero_elevation = zero_elevation
    
    def attach_n10_values(self, filepath):
        '''
        Reads the functions to read and convert the original datafiles
        and attaches it to self
        '''

        self.n10_values = convert_to_int(open_file(filepath))

    def calculate_total_depth(self):
        '''
        calculates the total depth
        Right now this assumes that we are talking about N10 values
        so therefore they were counted in 10cm intervals.
        '''

        self.total_depth = self.zero_elevation + len(self.n10_values) * 0.1 

    