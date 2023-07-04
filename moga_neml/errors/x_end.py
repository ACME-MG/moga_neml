"""
 Title:         The x_end objective function
 Description:   The objective function for calculating the x end point
 Author:        Janzen Choi

"""

# Libraries
from moga_neml.errors.__error__ import __Error__

# The X End class
class Error(__Error__):
    
    # Runs at the start, once
    def initialise(self):
        x_list = self.get_x_data()
        self.exp_x_end = x_list[-1]

    # Computing the error
    def get_value(self, prd_data:dict) -> float:
        x_label = self.get_x_label()
        prd_x_end = prd_data[x_label][-1]
        return abs((prd_x_end - self.exp_x_end) / self.exp_x_end)