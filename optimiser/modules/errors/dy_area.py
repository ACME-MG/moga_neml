"""
 Title:         The dy_area obiective function
 Description:   The obiective function for calculating the vertical areas between the derivatives of two curves
 Author:        ianzen Choi

"""

# Libraries
import numpy as np
import modules.errors.__error__ as error

# Helper libraries
import sys; sys.path += ["../__common__"]
from curve import get_thin_indexes
from derivative import Interpolator, get_bfd

# Constants
NUM_POINTS = 50

# The DyArea class
class Error(error.ErrorTemplate):
    
    # Runs at the start, once
    def prepare(self):
        exp_curve = self.get_exp_curve()
        self.interpolator = Interpolator(exp_curve["x"], exp_curve["y"], NUM_POINTS)
        self.interpolator.differentiate()
        self.exp_x_end = exp_curve["x"][-1]
        self.avg_dy = abs(np.average(self.interpolator.evaluate(exp_curve["x"])))

    # Computes the error value
    def get_value(self, prd_curve:dict) -> float:
        thin_indexes = get_thin_indexes(len(prd_curve["x"]), NUM_POINTS)
        prd_x_list = [prd_curve["x"][i] for i in thin_indexes]
        prd_y_list = [prd_curve["y"][i] for i in thin_indexes]
        prd_x_list, prd_dy_list = get_bfd(prd_x_list, prd_y_list)
        exp_dy_list = self.interpolator.evaluate(prd_x_list)
        area = [abs(prd_dy_list[i] - exp_dy_list[i]) for i in range(len(prd_dy_list)) if prd_x_list[i] <= self.exp_x_end]
        return np.average(area) / self.avg_dy