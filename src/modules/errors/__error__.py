"""
 Title:         Error
 Description:   Contains the basic structure for an error class
 Author:        Janzen Choi

"""

# Libraries
import math
import numpy as np
from scipy.interpolate import splev, splrep, splder
import matplotlib.pyplot as plt

# The Error Class
class Error:

    # Constructor
    def __init__(self, name, exp_curves):
        self.name = name
        self.exp_curves = exp_curves

    # Returns the name of the error
    def get_name(self):
        return self.name

    # Returns the experimental curve
    def get_exp_curves(self):
        return self.exp_curves

    # Prepares the object for evaluation (placeholder)
    def prepare(self):
        raise NotImplementedError
    
    # Returns an error (placeholder)
    def get_value(self):
        raise NotImplementedError

# The Interpolator Class
class Interpolator:

    # Constructor
    def __init__(self, x_list, y_list, resolution=50, smooth=False):
        thin_indexes = get_thin_indexes(len(x_list), resolution)
        self.thin_x_list = [x_list[i] for i in thin_indexes]
        self.thin_y_list = [y_list[i] for i in thin_indexes]
        smooth_amount = resolution if smooth else 0
        self.spl = splrep(self.thin_x_list, self.thin_y_list, s=smooth_amount)
    
    # Convert to derivative
    def differentiate(self):
        self.spl = splder(self.spl)
        self.thin_x_list, self.thin_y_list = get_bfd(self.thin_x_list, self.thin_y_list)

    # Evaluate
    def evaluate(self, x_list):
        return list(splev(x_list, self.spl))
    
    # Tests the interpolation by plotting
    def __test__(self, path):
        plt.scatter(self.thin_x_list, self.thin_y_list, color="b")
        y_list = self.evaluate(self.thin_x_list)
        plt.plot(self.thin_x_list, y_list, color="r")
        plt.savefig(path)
        plt.cla()

# Returns a list of indexes corresponding to thinned data
def get_thin_indexes(src_data_size, dst_data_size):
    step_size = src_data_size/dst_data_size
    thin_indexes = [math.floor(step_size*i) for i in range(1,dst_data_size-1)]
    thin_indexes = [0] + thin_indexes + [src_data_size-1]
    return thin_indexes

# Returns the derivative via backward finite difference
def get_bfd(x_list, y_list):
    new_x_list, dy_list = [], []
    for i in range(1,len(x_list)):
        if x_list[i] > x_list[i-1]:
            new_x_list.append(x_list[i])
            dy_list.append((y_list[i]-y_list[i-1])/(x_list[i]-x_list[i-1]))
    return new_x_list, dy_list

# Returns the coordinates of non-outliers (good to use with derivatives)
def exclude_outliers(x_list, y_list):
    q_1 = np.percentile(y_list, 25)
    q_3 = np.percentile(y_list, 75)
    u_bound = q_3 + 1.5*(q_3-q_1)
    l_bound = q_1 - 1.5*(q_3-q_1)
    index_list = [i for i in range(len(y_list)) if y_list[i] >= l_bound and y_list[i] <= u_bound]
    x_list = [x_list[i] for i in index_list]
    y_list = [y_list[i] for i in index_list]
    return x_list, y_list