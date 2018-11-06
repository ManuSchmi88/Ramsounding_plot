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
    
    '''