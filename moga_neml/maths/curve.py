"""
 Title:         Curve related Functions
 Description:   Contains functions to manipulate curves
 Author:        Janzen Choi

"""

# Libraries
import math, numpy as np
from copy import deepcopy

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

# Returns a thinned list
def get_thinned_list(unthinned_list:list, density:int) -> list:
    src_data_size = len(unthinned_list)
    step_size = src_data_size / density
    thin_indexes = [math.floor(step_size*i) for i in range(1, density - 1)]
    thin_indexes = [0] + thin_indexes + [src_data_size - 1]
    return [unthinned_list[i] for i in thin_indexes]

# Returns a list of indexes corresponding to thinned data based on a defined cumulative distribution function
def get_custom_thin_indexes(src_data_size, dst_data_size, distribution):
    unmapped_indexes = [distribution(i/dst_data_size) for i in range(1,dst_data_size-1)]
    thin_indexes = [math.floor(i*src_data_size) for i in unmapped_indexes]
    thin_indexes = [0] + thin_indexes + [src_data_size-1]
    return thin_indexes

# Removes data after a specific x value of a curve
def remove_data_after(curve:dict, x_value:float, x_label:str) -> dict:
    
    # Initialise new curve
    new_curve = deepcopy(curve)
    for header in new_curve.keys():
        if isinstance(new_curve[header], list):
            new_curve[header] = []
            
    # Remove data after specific value
    for i in range(len(curve[x_label])):
        if curve[x_label][i] > x_value:
            break
        for header in new_curve.keys():
            if isinstance(new_curve[header], list):
                new_curve[header].append(curve[header][i])
    
    # Return new data
    return new_curve
