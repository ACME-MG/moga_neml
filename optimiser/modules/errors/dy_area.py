"""
 Title:         The dy_area objective function
 Description:   The objective function for calculating the vertical areas between the derivatives of two curves
 Author:        Janzen Choi

"""

# Libraries
import numpy as np
import modules.errors.__error__ as error

# Helper libraries
import sys
sys.path += ["../__common__"]
from curve import get_thin_indexes
from derivative import Interpolator, get_bfd

# Constants
NUM_POINTS = 50

# The DyArea class
class DyArea(error.Error):

    # Constructor
    def __init__(self, type, weight, exp_curves):
        super().__init__("dy_area", type, weight, exp_curves)
    
    # Prepares for evaluation
    def prepare(self):
        self.interpolator_list, self.exp_x_end_list, self.avg_dy_list = [], [], []
        for exp_curve in self.exp_curves:
            interpolator = Interpolator(exp_curve["x"], exp_curve["y"], NUM_POINTS)
            interpolator.differentiate()
            self.interpolator_list.append(interpolator)
            self.exp_x_end_list.append(exp_curve["x"][-1])
            self.avg_dy_list.append(np.average(interpolator.evaluate(exp_curve["x"])))

    # Computes the error value
    def get_value(self, prd_curves:list[dict]) -> float:
        value_list = []
        for i in range(len(prd_curves)):
            if self.exp_curves[i]["type"] != self.type:
                continue
            thin_indexes = get_thin_indexes(len(prd_curves[i]["x"]), NUM_POINTS)
            prd_x_list = [prd_curves[i]["x"][j] for j in thin_indexes]
            prd_y_list = [prd_curves[i]["y"][j] for j in thin_indexes]
            prd_x_list, prd_dy_list = get_bfd(prd_x_list, prd_y_list)
            exp_dy_list = self.interpolator_list[i].evaluate(prd_x_list)
            area = [abs(prd_dy_list[j] - exp_dy_list[j]) for j in range(len(prd_dy_list)) if prd_x_list[j] <= self.exp_x_end_list[i]]
            value_list.append(np.average(area) / self.avg_dy_list[i])
        return np.average(value_list)