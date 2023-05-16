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
        self.interpolator_list, self.exp_x_end_list, self.avg_y_list = [], [], []
        for exp_curve in self.exp_curves:
            self.interpolator_list.append(Interpolator(exp_curve["x"], exp_curve["y"], NUM_POINTS))
            self.exp_x_end_list.append(exp_curve["x"][-1])
            self.avg_y_list.append(abs(np.average(exp_curve["y"])))
            
    # Computing the error
    def get_value(self, prd_curves:list[dict]) -> float:
        value_list = []
        for i in range(len(prd_curves)):
            if self.exp_curves[i]["type"] != self.type:
                continue
            thin_indexes = get_thin_indexes(len(prd_curves[i]["x"]), NUM_POINTS)
            prd_x_list = [prd_curves[i]["x"][j] for j in thin_indexes]
            prd_y_list = [prd_curves[i]["y"][j] for j in thin_indexes]
            exp_y_list = self.interpolator_list[i].evaluate(prd_x_list)
            area = [abs(prd_y_list[j] - exp_y_list[j]) for j in range(NUM_POINTS) if prd_x_list[j] <= self.exp_x_end_list[i]]
            value_list.append(np.average(area) / self.avg_y_list[i])
        return np.average(value_list)