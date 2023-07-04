"""
 Title:         The y_max objective function
 Description:   The objective function for calculating the maximum y magnitude of two curves
 Author:        Janzen Choi

"""

# Libraries
from moga_neml.errors.__error__ import __Error__

# The YArea class
class Error(__Error__):
    
    # Runs at the start, once
    def initialise(self):
        y_list = self.get_y_data()
        self.y_max = abs(max(y_list))
            
    # Computing the error
    def get_value(self, prd_data:list) -> float:
        y_label = self.get_y_label()
        return abs(self.y_max - max(prd_data[y_label])) / self.y_max