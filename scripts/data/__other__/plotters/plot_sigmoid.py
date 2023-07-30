import math
import numpy as np

def get_damage(x_f:float, y_f:float, x_t:float, y_t:float, g_1:float, g_2:float):
    """
    Gets the damage interpolation sigmoid curve
    
    Parameters:
    * `x_f`: Scale factor for the x coordinates
    * `y_f`: Scale factor for the y coordinates
    * `x_t`: Translation amount for the x coordinates
    * `y_t`: Translation amount for the y coordinates
    * `g_1`: The gradient of the left side of the sigmoid
    * `g_2`: The gradient of the right side of the sigmoid
    
    Returns the x and y coordinates
    """
    
    # Check values
    if x_f == 0 or y_f == 0 or g_1 > x_f*y_f or g_2 > x_f*y_f:
        return -1
    
    # Initialise function
    f_0 = lambda x : y_f*math.tanh(x_f*x - x_t) + y_t
    x_1 = (x_t - math.atanh(math.sqrt(1 - g_1/y_f/x_f))) / x_f
    x_2 = (x_t + math.atanh(math.sqrt(1 - g_2/y_f/x_f))) / x_f
    
    # Determine x coordinates based on sigmoid shifts
    x_list = list(np.linspace(x_1, x_2, 16))
    x_list = [-16] + x_list + [0]
    
    # Determine damage based on x coordinates
    def get_y(x):
        if x < x_1:
            return g_1 * (x-x_1) + f_0(x_1)
        elif x > x_2:
            return g_2 * (x-x_2) + f_0(x_2)
        else:
            return f_0(x)
    
    # Calculate x and y coordinates and return
    y_list = [get_y(x) for x in x_list]
    return x_list, y_list

wd_x_f, wd_y_f, wd_x_t, wd_y_t, wd_g_1, wd_g_2 = 10.18, 162.86, -45.254, 176.03, 50.10608, 50.34346
x_list, y_list = get_damage(wd_x_f, wd_y_f, wd_x_t, wd_y_t, wd_g_1, wd_g_2)

import matplotlib.pyplot as plt
plt.scatter(x_list, y_list)
plt.savefig("plot")