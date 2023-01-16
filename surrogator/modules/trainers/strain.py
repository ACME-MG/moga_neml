"""
 Title:         Strain Trainer
 Description:   Trainer that uses a strain representation of the creep curve 
 Author:        Janzen Choi

"""

# Libraries
from modules.trainers.__trainer__ import Trainer
import numpy as np

# Constants
CURVE_SIZE = 1000
STEP_SIZE  = 10

# Strain Trainer Class
class Strain(Trainer):

    # Constructor
    def __init__(self, model):
        super().__init__(
            model     = model,
            name      = "strain",
            output_lb = [0] * CURVE_SIZE,
            output_ub = [1] * CURVE_SIZE,
        )
    
    # Returns the training input / output data (placeholder)
    def __get_io__(self, unmapped_input, curve):
        
        # Get polynomial
        x_list, y_list = curve["x"], curve["y"]
        polynomial = np.polyfit(x_list, y_list, 15)

        # Reconstruct curve
        x_list = list(range(0, round(x_list[-1]), STEP_SIZE))
        y_list = list(np.polyval(polynomial, x_list))
        y_list += [y_list[-1]] * (CURVE_SIZE-len(y_list))
        
        # Map and return
        mapped_input = super().map_input(unmapped_input)
        mapped_output = super().map_output(y_list)
        return mapped_input, mapped_output

    # Converts representational points into a creep curve
    def restore_curve(self, mapped_output):

        # Get unmapped strain values
        unmapped_output = super().unmap_output(mapped_output)

        # Assume that strain monotonically increases
        previous, x_list, y_list = -1, [], []
        for i in range(CURVE_SIZE):
            if unmapped_output[i] <= previous:
                break
            previous = unmapped_output[i]
            x_list.append(STEP_SIZE*i)
            y_list.append(unmapped_output[i])

        # Return
        return {"x": x_list, "y": y_list}
