"""
 Title:         The n_cycles objective function
 Description:   The objective function for calculating the number of cycles in a periodic curve
 Author:        Janzen Choi

 """

# Libraries
import sys
import numpy as np
from math import ceil
import modules.errors.__error__ as error

# Helper libraries
sys.path += ["../__common__"]
from derivative import get_stationary_points

# The Error class
class Error(error.ErrorTemplate):
    
    # Runs at the start, once (optional)
    def prepare(self):
        sp_list = [len(get_stationary_points(exp_curve, 100, 0.9)) for exp_curve in self.exp_curves]
        self.exp_cycles_list = [ceil(sp / 2) for sp in sp_list]
        self.exp_avg_cycles = np.average(self.exp_cycles_list)

    # Computes the error value
    def get_value(self, prd_curves:list[dict]) -> float:
        prd_cycles_list = [get_stationary_points(prd_curve, 100, 0.9) for prd_curve in prd_curves]
        value_list = [abs(self.exp_cycles_list[i] - prd_cycles_list[i]) for i in range(len(self.exp_cycles_list))]