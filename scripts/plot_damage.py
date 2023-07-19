
import math
import numpy as np
import matplotlib.pyplot as plt

# Gets the damage value for interpolation
#   x_f and y_f for scaling (0, 1)
#   x_t and y_t for translating
#   g_1 and g_2 are left and right gradients (0, 1)
def get_damage(x_0, x_f, y_f, x_t, y_t, g_1, g_2):
    
    # Check values
    if x_f == 0 or y_f == 0 or g_1 > x_f*y_f or g_2 > x_f*y_f:
        return -1
    
    # Get all possible values
    f_0 = lambda x : y_f*math.tanh(x_f*x - x_t) + y_t
    x_1 = (x_t - math.atanh(math.sqrt(1 - g_1/y_f/x_f))) / x_f
    x_2 = (x_t + math.atanh(math.sqrt(1 - g_2/y_f/x_f))) / x_f
    
    # Determine which part of the curve the x_0 value lies
    if x_0 < x_1:
        return g_1 * (x_0 - x_1) + f_0(x_1)
    elif x_0 > x_2:
        return g_2 * (x_0 - x_2) + f_0(x_2)
    else:
        return f_0(x_0)

x_list = list(np.linspace(-16, 0, 20))
y_list = [get_damage(x, 1, 1, 0, 0, 0.01, 0.01) for x in x_list]
plt.scatter(x_list, y_list)
plt.savefig("plot")
