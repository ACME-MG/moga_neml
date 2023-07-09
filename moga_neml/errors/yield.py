"""
 Title:         The yield objective function
 Description:   The objective function for optimising the yield point of a tensile curve
 Author:        Janzen Choi

 """

# Libraries
import math, numpy as np
import scipy.interpolate as inter
import scipy.optimize as opt
from moga_neml.errors.__error__ import __Error__
from moga_neml._optimise.controller import BIG_VALUE

# The Error class
class Error(__Error__):
    
    # Runs at the start, once (optional)
    def initialise(self):
        self.enforce_data_type("tensile")
        self.exp_yield = get_yield(self.get_exp_data())
        self.mag_yield = math.sqrt(math.pow(self.exp_yield[0], 2) + math.pow(self.exp_yield[1], 2))

    # Computes the error value
    def get_value(self, prd_data:dict) -> float:
        try:
            prd_yield = get_yield(prd_data)
        except ValueError:
            return BIG_VALUE
        distance = math.sqrt(math.pow(self.exp_yield[0] - prd_yield[0], 2) + math.pow(self.exp_yield[1] - prd_yield[1], 2))
        return distance / self.mag_yield

# Gets the yield point
def get_yield(data_dict:dict):
    
    # Extract data
    x_offset = 0.2/100.0
    x_list = data_dict["strain"]
    y_list = data_dict["stress"]
    
    # Calculate elastic modulus
    youngs = (y_list[4] - y_list[0]) / (x_list[4] - x_list[0])
    
    # Interpolate
    iff = inter.interp1d(x_list, y_list, bounds_error=False, fill_value=0)
    x_yield = opt.brentq(lambda x: iff(x) - youngs * (x - x_offset), 0.0, np.max(x_list))
    y_yield = float(iff(x_yield))
    return x_yield, y_yield
