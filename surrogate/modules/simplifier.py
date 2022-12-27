"""
 Title:         Simplifier
 Description:   For simplifying creep curves into several points 
 Author:        Janzen Choi

"""

# Libraries
import numpy as np
import math

# Simplifier Class
class Simplifier:

    # Constructor
    def __init__(self, restore_size=10):
        self.restore_size = restore_size
        self.l_bounds = [0, 0, 0, 0, 0]
        self.u_bounds = [1, 10000, 100, 10000, 100]

    # Converts a creep curve into representational points
    def simplify_curve(self, curve):

        # Get derivative
        x_list, y_list = curve["x"], curve["y"]
        polynomial = np.polyfit(x_list, y_list, 15)
        d_polynomial = np.polyder(polynomial)
        dy_list = list(np.polyval(d_polynomial, x_list))
        # dy_list = get_bfd(x_list, y_list)

        # Get secondary points
        dy_min = min(dy_list)
        dy_min_index = dy_list.index(dy_min)
        x_dy_min = x_list[dy_min_index]
        y_dy_min = y_list[dy_min_index]

        # Get tertiary points
        x_end = x_list[-1]
        y_end = y_list[-1]

        # Return
        return [dy_min, x_dy_min, y_dy_min, x_end, y_end]

    # Converts representational points into a creep curve
    def restore_curve(self, points, axial=1.0):

        # Extract representational points
        dy_min   = points[0]
        x_dy_min = points[1]
        y_dy_min = points[2]
        x_end    = points[3]
        y_end    = points[4]

        # Calculate primary points
        x_p, y_p = [], []
        if x_dy_min != 0:
            m_p = (y_dy_min/x_dy_min)
            d_p = math.sqrt(x_dy_min**2 + y_dy_min**2)
            a_p = ((dy_min-m_p)/(1+m_p*dy_min))/d_p*axial
            b_p = -a_p*(d_p/2)**2
            x_p = [d_p*i/self.restore_size for i in range(self.restore_size)]
            y_p = [a_p*(x-d_p/2)**2+b_p for x in x_p]
            x_p, y_p = rotate_2d(x_p, y_p, math.atan(m_p))

        # Calculate tertiary points
        x_t, y_t = [], []
        if x_end-x_dy_min != 0:
            m_t = ((y_end-y_dy_min)/(x_end-x_dy_min))
            d_t = math.sqrt((x_end-x_dy_min)**2 + (y_end-y_dy_min)**2)
            a_t = ((m_t-dy_min)/(1+m_t*dy_min))/d_t*axial
            b_t = -a_t*(d_t/2)**2
            x_t = [d_t*i/self.restore_size for i in range(self.restore_size)]
            y_t = [a_t*(x-d_t/2)**2+b_t for x in x_t]
            x_t, y_t = rotate_2d(x_t, y_t, math.atan(m_t))
            x_t = [x+x_dy_min for x in x_t]
            y_t = [y+y_dy_min for y in y_t]

        # Combine points and return
        x_list = [0, *x_p, x_dy_min, *x_t, x_end]
        y_list = [0, *y_p, y_dy_min, *y_t, y_end]
        return {"x": x_list, "y": y_list}

# Returns a sample creep curve
def get_sample_curve():
    polynomial = [0.1, -0.6, 1.3, 0]
    x_list = [10*x for x in range(100)]
    scaled_x_list = [x/225 for x in x_list]
    y_list = list(np.polyval(polynomial, scaled_x_list))
    y_list = [y/8 for y in y_list]
    return {"x": x_list, "y": y_list}

# Returns the derivative via backward finite difference
def get_bfd(x_list, y_list):
    dy_list = []
    for i in range(1,len(x_list)):
        dy = (y_list[i]-y_list[i-1])/(x_list[i]-x_list[i-1]) if (x_list[i] > x_list[i-1] and y_list[i] > y_list[i-1]) else 100
        dy_list.append(dy)
    return dy_list

# Rotates list of points by a certain angle
def rotate_2d(x_list, y_list, angle):
    x_new, y_new = [], []
    for i in range(len(x_list)):
        x_new.append(x_list[i]*math.cos(angle) - y_list[i]*math.sin(angle))
        y_new.append(x_list[i]*math.sin(angle) + y_list[i]*math.cos(angle))
    return x_new, y_new
