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
    
    Returns the x and y coordinates (on the log 10 scale)
    """
    
    # Initialise function
    f_0 = lambda x : y_f*math.tanh(x_f*x - x_t) + y_t
    x_1 = (x_t - math.atanh(math.sqrt(1 - g_1/y_f/x_f))) / x_f
    x_2 = (x_t + math.atanh(math.sqrt(1 - g_2/y_f/x_f))) / x_f
    x_0 = x_1 - f_0(x_1) / g_1
    
    # Determine x coordinates based on sigmoid shifts
    num_points = 16
    x_list =  list(np.linspace(x_0, x_1, num_points))
    x_list += list(np.linspace(x_1, x_2, num_points))
    x_list += list(np.linspace(x_2, 0, num_points))
    
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
    y_list = [math.log10(y) if y > 0 else 0 for y in y_list]
    return x_list, y_list

wd_x_f, wd_y_f, wd_x_t, wd_y_t, wd_g_1, wd_g_2 = 79.673, 177.8, -16.505, 358.65, 17.6, 78.943
x_list, y_list = get_damage(wd_x_f, wd_y_f, wd_x_t, wd_y_t, wd_g_1, wd_g_2)

import matplotlib.pyplot as plt
plt.scatter(x_list, y_list)
plt.savefig("plot")