"""
 Title:         The x_max objective function
 Description:   The objective function for calculating the maximum x magnitude of two curves
 Author:        Janzen Choi

"""

# Libraries
from moga_neml.errors.__error__ import __Error__

# The maximum value class
class Error(__Error__):
    
    # Runs at the start, once
    def initialise(self):
        x_list = self.get_x_data()
        self.x_max = abs(max(x_list))
            
    # Computing the error
    def get_value(self, prd_data:list) -> float:
        x_label = self.get_x_label()
        return abs(self.x_max - max(prd_data[x_label])) / self.x_max