"""
 Title:         The end_value objective function
 Description:   The objective function for calculating the x end point
 Author:        Janzen Choi

"""

# Libraries
from moga_neml.errors.__error__ import __Error__

# The X End class
class Error(__Error__):
    
    def initialise(self, factor:float=10):
        """
        Runs at the start, once

        Parameters:
        * `factor`: The factor to penalise for unconservative predictions
        """
        x_list = self.get_x_data()
        self.factor = factor
        self.exp_x_end = x_list[-1]

    def get_value(self, prd_data:dict) -> float:
        """
        Computing the NRMSE

        Parameters:
        * `prd_data`: The predicted data

        Returns the error
        """
        x_label = self.get_x_label()
        prd_end_value = prd_data[x_label][-1]
        error = abs((prd_end_value - self.exp_x_end) / self.exp_x_end)
        if self.exp_x_end < prd_end_value:
            return error * self.factor
        return error