"""
 Title:         The y_area objective function
 Description:   The objective function for calculating the vertical areas between two curves
 Author:        Janzen Choi

"""

# Libraries
import numpy as np
import modules.errors.__error__ as error

# Helper libraries
import sys; sys.path += ["../__common__"]
from curve import get_thin_indexes
from derivative import Interpolator

# Constants
NUM_POINTS = 50

# The YArea class
class Error(error.ErrorTemplate):
    
    # Runs at the start, once
    def prepare(self):
        exp_curve = self.get_exp_curve()
        self.interpolator = Interpolator(exp_curve["x"], exp_curve["y"], NUM_POINTS)
        self.exp_x_end = exp_curve["x"][-1]
        self.avg_y = abs(np.average(exp_curve["y"]))
            
    # Computing the error
    def get_value(self, prd_curve:list[dict]) -> float:
        thin_indexes = get_thin_indexes(len(prd_curve["x"]), NUM_POINTS)
        prd_x_list = [prd_curve["x"][i] for i in thin_indexes]
        prd_y_list = [prd_curve["y"][i] for i in thin_indexes]
        exp_y_list = self.interpolator.evaluate(prd_x_list)
        area = [abs(exp_y_list[i] - prd_y_list[i]) for i in range(NUM_POINTS) if prd_x_list[i] <= self.exp_x_end]
        return np.average(area) / self.avg_y