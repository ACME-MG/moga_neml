"""
 Title:         The area objective function
 Description:   The objective function for calculating the vertical areas between two curves
 Author:        Janzen Choi

"""

# Libraries
import math, numpy as np
from moga_neml.errors.__error__ import __Error__
from moga_neml.helper.data import get_thinned_list
from moga_neml.helper.interpolator import Interpolator

# The Area class
class Error(__Error__):
    
    def initialise(self, num_points:int=50, max_value:float=None):
        """
        Runs at the start, once
        """
        self.num_points = num_points
        x_list = self.get_x_data()
        y_list = self.get_y_data()
        self.interpolator = Interpolator(x_list, y_list, self.num_points)
        self.exp_x_end = min(x_list[-1], max_value) if max_value != None else x_list[-1]
        self.avg_y = abs(np.average(y_list))

    def get_value(self, prd_data:dict) -> float:
        """
        Computing the NRMSE

        Parameters:
        * `prd_data`: The predicted data

        Returns the error
        """
        x_label = self.get_x_label()
        y_label = self.get_y_label()
        prd_x_list = get_thinned_list(prd_data[x_label], self.num_points)
        prd_y_list = get_thinned_list(prd_data[y_label], self.num_points)
        exp_y_list = self.interpolator.evaluate(prd_x_list)
        area = [math.pow(prd_y_list[i] - exp_y_list[i], 2) for i in range(self.num_points) if prd_x_list[i] <= self.exp_x_end]
        return math.sqrt(np.average(area)) / self.avg_y