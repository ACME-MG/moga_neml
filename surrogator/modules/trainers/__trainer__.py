"""
 Title:         Trainer
 Description:   Contains the basic structure for a trainer class
 Author:        Janzen Choi

"""

# Libraries
import sys
import numpy as np
from modules.mapper import MultiMapper

# Helper libraries
sys.path.append("../__common__")
from plotter import quick_plot

# The Model Class
class Trainer:

    # Constructor
    def __init__(self, model, name, output_lb, output_ub):

        # Define model and trainer name
        self.model = model
        self.name = name

        # Define input / output variables
        input_lb = self.model.get_param_lower_bounds()
        input_ub = self.model.get_param_upper_bounds()
        self.param_mapper = MultiMapper(input_lb, input_ub)
        self.curve_mapper = MultiMapper(output_lb, output_ub)
        self.input_size = len(input_lb)
        self.output_size = len(output_lb)

    # Returns the name of the trainer
    def get_name(self):
        return self.name

    # Returns the raw curve from the model
    def get_raw_curve(self, unmapped_input):
        curves = self.model.get_prd_curves(*unmapped_input)
        curve = {"x": curves[0]["x"], "y": curves[0]["y"]} if curves != [] else {"x": [], "y": []}
        return curve

    # Maps the input
    def map_input(self, unmapped_input):
        return self.param_mapper.map(unmapped_input)

    # Maps the output
    def map_output(self, unmapped_output):
        return self.curve_mapper.map(unmapped_output)

    # Unmaps the input
    def unmap_input(self, mapped_input):
        return self.param_mapper.unmap(mapped_input)

    # Unmaps the output
    def unmap_output(self, mapped_output):
        return self.curve_mapper.unmap(mapped_output)

    # Returns the input / output size
    def get_shape(self):
        return self.input_size, self.output_size

    # Makes a plot of the raw and restored curves
    def plot(self, mapped_input, mapped_output, path, file):

        # Unmap input / output
        unmapped_input = self.unmap_input(mapped_input)
        unmapped_output = self.unmap_output(mapped_output)

        # Get raw and restored curve
        raw_curve = self.get_raw_curve(unmapped_input)
        restored_curve = self.restore_curve(unmapped_output)
        
        # Plot
        quick_plot(raw_curve, restored_curve, "Original", "Restored", path, file)

    # Returns the input / output data with validification
    def get_io(self, unmapped_input):
        curve = self.get_raw_curve(unmapped_input)
        if validate_curve(curve):
            return self.__get_io__(unmapped_input, curve)
        return None, None

    # Returns the training input / output data (placeholder)
    def __get_io__(self, unmapped_input, curve):
        raise NotImplementedError

    # Converts the outputs into a curve (placeholder)
    def restore_curve(self, unmapped_output):
        raise NotImplementedError

# Returns the derivative via backward finite difference
def get_bfd(x_list, y_list):
    dy_list = []
    for i in range(1,len(x_list)):
        dy = (y_list[i]-y_list[i-1])/(x_list[i]-x_list[i-1]) if (x_list[i] > x_list[i-1] and y_list[i] > y_list[i-1]) else 100
        dy_list.append(dy)
    return dy_list

# Returns a sample creep curve
def get_sample_curve():
    polynomial = [0.1, -0.6, 1.3, 0]
    x_list = [10*x for x in range(100)]
    scaled_x_list = [x/225 for x in x_list]
    y_list = list(np.polyval(polynomial, scaled_x_list))
    y_list = [y/8 for y in y_list]
    return {"x": x_list, "y": y_list}

# Checks if corresponding creep curve is successful and within bounds
def validate_curve(curve):
    if curve["x"] == [] or curve["y"] == []: # or curve["y"][-1] < 0.01:
        return False
    valid_list = [y >= 0 and y <= 1 for y in curve["y"]]
    return not (False in valid_list)