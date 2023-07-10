"""
 Title:         The min_data objective function
 Description:   The objective function that throws a big error if there are insufficient points
 Author:        Janzen Choi

"""

# Libraries
from moga_neml.errors.__error__ import __Error__

# Constants
MIN_DATA = 50

# The MinData class
class Error(__Error__):

    # Computing the error
    def get_value(self, prd_data:dict) -> float:
        x_label = self.get_x_label()
        if len(prd_data[x_label]) < MIN_DATA:
            return
        return 0 # it has sufficient data