
import math
import numpy as np
import matplotlib.pyplot as plt

# Gets the damage value for interpolation
#   x_f and y_f for scaling (0, 1)
#   x_t and y_t for translating
#   g_1 and g_2 are left and right gradients (0, 1)
def get_damage(x_list, x_f, y_f, x_t, y_t, g_1, g_2):
    
    # Check values
    if x_f == 0 or y_f == 0 or g_1 > x_f*y_f or g_2 > x_f*y_f:
        return -1
    
    # Get all possible values
    f_0 = lambda x : y_f*math.tanh(x_f*x - x_t) + y_t
    x_1 = (x_t - math.atanh(math.sqrt(1 - g_1/y_f/x_f))) / x_f
    x_2 = (x_t + math.atanh(math.sqrt(1 - g_2/y_f/x_f))) / x_f
    
    # Determine which part of the curve the x_0 value lies
    new_x_list = []
    for x in x_list:
        if x < x_1:
            new_x_list.append(g_1 * (x-x_1) + f_0(x_1))
        elif x > x_2:
            new_x_list.append(g_2 * (x-x_2) + f_0(x_2))
        else:
            new_x_list.append(f_0(x))
    return new_x_list

x_list = list(np.linspace(-16, 16, 32))
y_list = get_damage(x_list, 1, 1, 0, 0, 0.01, 0.1)
plt.scatter(x_list, y_list)
plt.savefig("plot")
