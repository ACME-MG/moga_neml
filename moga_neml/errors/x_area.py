"""
 Title:         The x_area objective function
 Description:   The objective function for calculating the horizontal areas between two curves
 Author:        Janzen Choi

"""

# Libraries
import numpy as np
import moga_neml.errors.__error__ as error
from moga_neml._maths.curve import get_thin_indexes
from moga_neml._maths.derivative import Interpolator

# Constants
NUM_POINTS = 50

# The XArea class
class Error(error.__Error__):
    
    # Runs at the start, once
    def prepare(self):
        exp_curve = self.get_exp_curve()
        self.interpolator = Interpolator(exp_curve["y"], exp_curve["x"], NUM_POINTS)
        self.exp_y_end = exp_curve["y"][-1]
        self.avg_x = abs(np.average(exp_curve["x"]))

    # Computing the error
    def get_value(self, prd_curve:dict) -> float:
        thin_indexes = get_thin_indexes(len(prd_curve["x"]), NUM_POINTS)
        prd_x_list = [prd_curve["x"][i] for i in thin_indexes]
        prd_y_list = [prd_curve["y"][i] for i in thin_indexes]
        exp_x_list = self.interpolator.evaluate(prd_y_list)
        area = [abs(prd_x_list[i] - exp_x_list[i]) for i in range(NUM_POINTS) if prd_y_list[i] <= self.exp_y_end]
        return np.average(area) / self.avg_x