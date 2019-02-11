import numpy as np
import matplotlib.pyplot as plt

def open_file(filename:str, filetype = 'ascii'):
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
    data = np.array(data)
    return data

class RSProfile():
    """
    This class will hold the necessary information about
    the individual ramsounding profiles

    We would need:
        Absolute Depth : Meter u.Gk [Float]
        Zero-Point     : Which depth did you start profiling [Float]
        Type           : Which Type of RS did you use [String/Id]
        n10            : Counts per 10cm [array]
        lat/lon        : coordinates of ramsoundiung
   
    """

    def __init__(self, rs_type:str):
        """
        initial input parameters:
            rs_type :   DPL - Light Ramsounding
                        DPM - Medium Ramsounding
                        DPH - Heavy Ramsounding
        """

        if rs_type in ('DPL', 'DPM', 'DPH'):
            self.rs_type = rs_type
        else:
            raise NotImplementedError

    def attach_n10_values(self, filepath):
        '''
        Reads the functions to read and convert the original datafiles
        and attaches it to self
        '''

        self.n10_values = convert_to_int(open_file(filepath))

    def set_zero_elevation(self, zero_elevation = 0):
        self.zero_elevation = zero_elevation

    def calculate_total_depth(self):
        '''
        calculates the total depth
        Right now this assumes that we are talking about N10 values
        so therefore they were counted in 10cm intervals.
        '''

        self.total_depth = self.zero_elevation + len(self.n10_values) * 0.1 
    
    def create_plot(self, with_coloring=True):
        '''
        create the depth plot
        '''
        
        ##this stuff creates the necessary x-y-arrays
        depth_array = np.arange(self.zero_elevation, self.total_depth, 0.1)
        #expand depth_array to get a more nearest-neighbour like look
        nn_depth_array = np.arange(self.zero_elevation, self.total_depth, 0.1 / 100)
        nn_data_array = np.repeat(self.n10_values,100)

        #get transitions boundary indices for dpm_limits
        #TODO: write a nice for n in info['dpm_limits] blabla loop.
        #right now this is just for testing:
        weich_indices  = np.where(np.logical_and(nn_data_array >= 0, nn_data_array < 4))
        breiig_indices = np.where(np.logical_and(nn_data_array >= 4, nn_data_array < 8))
        steif_indices  = np.where(np.logical_and(nn_data_array >= 8, nn_data_array < 14))
        halbfest_indices  = np.where(np.logical_and(nn_data_array >= 14, nn_data_array < 28))
        fest_indices = np.where(nn_data_array >= 28)

        ##create the actual plot
        fig, ax = plt.subplots(1, figsize = [8,8])
        ax.plot(nn_data_array, nn_depth_array, 'k', linewidth = 2.3)
        ax.set_xlim([0,50])
        ax.set_ylim(4,0)
        ax.xaxis.tick_top()

        if with_coloring == True:
            for i in weich_indices:
                ax.hlines(nn_depth_array[i],nn_data_array[i] ,90,alpha = 0.01)
            for i in breiig_indices:
                ax.hlines(nn_depth_array[i],nn_data_array[i] ,90,alpha = 0.01, color = 'blue')
            for i in steif_indices:
                ax.hlines(nn_depth_array[i],nn_data_array[i] ,90, alpha = 0.01, color = 'magenta')
            for i in halbfest_indices:
                ax.hlines(nn_depth_array[i],nn_data_array[i] ,90, alpha = 0.01, color = 'yellow')
            for i in fest_indices:
                ax.hlines(nn_depth_array[i],nn_data_array[i] ,90, alpha = 0.02, color = 'red')

        ax.axes.tick_params(labelsize = 16)
        ax.set_xlabel('Schlagzahl', fontsize = 18)
        ax.xaxis.set_label_position('top')

        ax.set_ylabel('Tiefe [m]', fontsize = 18)

        ax.grid(linewidth = 1.2)

        ax.fill_betweenx(nn_depth_array, nn_data_array, hatch='/')

        plt.savefig('rs_array.png')
        plt.close()

    
