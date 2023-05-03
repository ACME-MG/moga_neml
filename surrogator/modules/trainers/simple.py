"""
 Title:         Simple Trainer
 Description:   Trainer that uses a simple representation of the creep curve 
 Author:        Janzen Choi

"""

# Libraries
from modules.trainers.__trainer__ import TrainerTemplate
from scipy.interpolate import splev, splrep, splder
import math

# Constants
AXIAL_DISTANCE = 1.2
RESTORE_SIZE   = 10

# Simple Trainer Class
class Trainer(TrainerTemplate):

    # Constructor
    def __init__(self, model):
        super().__init__(
            model     = model,
            name      = "simple",
            output_lb = [0, 0, 0, 0, 0],
            output_ub = [1, 10000, 1, 10000, 1],
        )
    
    # Returns the training input / output data (placeholder)
    def __get_io__(self, unmapped_input, curve):
        
        # Get derivative
        x_list, y_list = curve["x"], curve["y"]
        spl = splrep(x_list, y_list, s=0)
        spl = splder(spl)
        dy_list = list(splev(x_list, spl))

        # Get secondary points
        dy_min = min(dy_list)
        dy_min_index = dy_list.index(dy_min)
        x_dy_min = x_list[dy_min_index]
        y_dy_min = y_list[dy_min_index]

        # Get tertiary points
        x_end = x_list[-1]
        y_end = y_list[-1]

        # Return mapped input / output
        mapped_input = super().map_input(unmapped_input)
        mapped_output = super().map_output([dy_min, x_dy_min, y_dy_min, x_end, y_end])
        return mapped_input, mapped_output

    # Converts representational points into a creep curve
    def restore_curve(self, mapped_output):

        # Extract representational points
        output   = super().unmap_output(mapped_output)
        dy_min   = output[0]
        x_dy_min = output[1]
        y_dy_min = output[2]
        x_end    = output[3]
        y_end    = output[4]

        # Calculate primary points
        x_p, y_p = [], []
        if x_dy_min != 0:
            m_p = (y_dy_min/x_dy_min)
            d_p = math.sqrt(x_dy_min**2 + y_dy_min**2)
            a_p = ((dy_min-m_p)/(1+m_p*dy_min))/d_p*AXIAL_DISTANCE
            b_p = -a_p*(d_p/2)**2
            x_p = [d_p*i/RESTORE_SIZE for i in range(RESTORE_SIZE)]
            y_p = [a_p*(x-d_p/2)**2+b_p for x in x_p]
            x_p, y_p = rotate_2d(x_p, y_p, math.atan(m_p))

        # Calculate tertiary points
        x_t, y_t = [], []
        if x_end-x_dy_min != 0:
            m_t = ((y_end-y_dy_min)/(x_end-x_dy_min))
            d_t = math.sqrt((x_end-x_dy_min)**2 + (y_end-y_dy_min)**2)
            a_t = ((m_t-dy_min)/(1+m_t*dy_min))/d_t*AXIAL_DISTANCE
            b_t = -a_t*(d_t/2)**2
            x_t = [d_t*i/RESTORE_SIZE for i in range(RESTORE_SIZE)]
            y_t = [a_t*(x-d_t/2)**2+b_t for x in x_t]
            x_t, y_t = rotate_2d(x_t, y_t, math.atan(m_t))
            x_t = [x+x_dy_min for x in x_t]
            y_t = [y+y_dy_min for y in y_t]

        # Combine points and return
        x_list = [0, x_dy_min, x_end]
        y_list = [0, y_dy_min, y_end]
        # x_list = [0, *x_p, x_dy_min, *x_t, x_end]
        # y_list = [0, *y_p, y_dy_min, *y_t, y_end]
        return {"x": x_list, "y": y_list}

# Rotates list of points by a certain angle
def rotate_2d(x_list, y_list, angle):
    x_new, y_new = [], []
    for i in range(len(x_list)):
        x_new.append(x_list[i]*math.cos(angle) - y_list[i]*math.sin(angle))
        y_new.append(x_list[i]*math.sin(angle) + y_list[i]*math.cos(angle))
    return x_new, y_new
