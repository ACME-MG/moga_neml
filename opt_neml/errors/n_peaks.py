"""
 Title:         The n_cycles objective function
 Description:   The objective function for calculating the number of cycles in a periodic curve
 Author:        Janzen Choi

 """

# Libraries
import opt_neml.errors.__error__ as error
from opt_neml.helper.derivative import get_stationary_points

# The Error class
class Error(error.ErrorTemplate):
    
    # Runs at the start, once (optional)
    def prepare(self):
        exp_curve = self.get_exp_curve()
        self.exp_num_cycles = len(get_stationary_points(exp_curve, 100, 0.9))

    # Computes the error value
    def get_value(self, prd_curve:dict) -> float:
        prd_num_cycles = len(get_stationary_points(prd_curve, 100, 0.9))
        return abs(self.exp_num_cycles - prd_num_cycles) / self.exp_num_cycles