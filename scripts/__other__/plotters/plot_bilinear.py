import math
import numpy as np


def get_damage(a_0:float, a_1:float, b_0:float, b_1:float):
    """
    Gets the damage interpolation bilinear curve
    
    Parameters:
    * `a_0`: Gradient for left side of bilinear function
    * `a_1`: Vertical intercept for left side of bilinear function
    * `b_0`: Gradient for right side of bilinear function
    * `b_1`: Vertical intercept for right side of bilinear function
    
    Returns the x and y coordinates (on the log10-log10 scale)
    """
    
    # Get x values
    x_0 = -a_1 / a_0                # x intercept of left line and x axis
    x_1 = (b_1 - a_1) / (a_0 - b_0) # x intercept of two lines
    x_2 = 3                         # x intercept of right line and y axis
    
    # Get y values
    y_0 = 0                         # y intercept of left line and x axis
    y_1 = a_0 * x_1 + a_1           # y intercept of two lines
    y_2 = b_0 * x_2 + b_1           # y intercept of right line and y axis
    
    # Combine, log, and return
    num_points = 16
    x_list = list(np.linspace(x_0, x_1, num_points)) + list(np.linspace(x_1, x_2, num_points))
    y_list = list(np.linspace(y_0, y_1, num_points)) + list(np.linspace(y_1, y_2, num_points))
    return x_list, y_list

x_list, y_list = get_damage(0.3684, 3.2014, 0.9971, 3.8264)

import matplotlib.pyplot as plt
plt.scatter(x_list, y_list)
plt.savefig("plot")