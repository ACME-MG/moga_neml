"""
 Title:         The dummy objective function
 Description:   The objective function that just returns 0
 Author:        Janzen Choi

"""

# Libraries
from moga_neml.errors.__error__ import __Error__

# The Dummy class
class Error(__Error__):
    
    # Runs at the start, once
    def initialise(self):
        pass

    # Computes the NRMSE value
    def get_value(self, prd_data:dict) -> float:
        return 0
