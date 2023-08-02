"""
 Title:         The custom area objective function
 Description:   The objective function for calculating the (custom) vertical areas between two curves
 Author:        Janzen Choi

"""

# Libraries
import math, numpy as np
from moga_neml.errors.__error__ import __Error__
from moga_neml._maths.interpolator import Interpolator

# The Custom Area class
class Error(__Error__):
    
    # Runs at the start, once
    def initialise(self, values:list):
        interpolator = Interpolator(self.get_x_data(), self.get_y_data())
        self.exp_x_list = values
        self.exp_y_list = interpolator.evaluate(values)
        self.avg_y = abs(np.average(self.exp_y_list))

    # Computing the NRMSE
    def get_value(self, prd_data:dict) -> float:
        x_label = self.get_x_label()
        y_label = self.get_y_label()
        interpolator = Interpolator(prd_data[x_label], prd_data[y_label])
        prd_y_list = interpolator.evaluate(self.exp_x_list)
        area = [math.pow(prd_y_list[i] - self.exp_y_list[i], 2) for i in range(len(prd_y_list))]
        return math.sqrt(np.average(area)) / self.avg_y