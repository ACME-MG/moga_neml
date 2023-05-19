"""
 Title:         The x_end objective function
 Description:   The objective function for calculating the horizontal distance in which two curves end
 Author:        Janzen Choi

"""

# Libraries
import numpy as np
import modules.errors.__error__ as error

# The XEnd class
class Error(error.ErrorTemplate):
    
    # Runs at the start, once
    def prepare(self):
        exp_curve = self.get_exp_curve()
        self.exp_x_end = abs(exp_curve["x"][-1])

    # Computing the error
    def get_value(self, prd_curve:dict) -> float:
        return abs(prd_curve["x"][-1] - self.exp_x_end) / self.exp_x_end