"""
 Title:         The yield objective function
 Description:   The objective function for optimising the yield point of a tensile curve
 Author:        Janzen Choi

 """

# Libraries
import numpy as np
import scipy.interpolate as inter
import scipy.optimize as opt
from moga_neml.errors.__error__ import __Error__

# The Error class
class Error(__Error__):
    
    # Runs at the start, once (optional)
    def initialise(self):
        self.enforce_data_type("tensile")
        self.x_label = self.get_x_label()
        self.y_label = self.get_y_label()
        self.exp_yield = get_yield(self.get_exp_data(), self.x_label, self.y_label)
        self.mag_yield = (self.exp_yield[0]**2 + self.exp_yield[1]**2)**0.5

    # Computes the error value
    def get_value(self, prd_data:dict) -> float:
        prd_yield = get_yield(prd_data, self.x_label, self.y_label)
        distance = ((self.exp_yield[0] - prd_yield[0])**2 + (self.exp_yield[1] - prd_yield[1])**2)**0.5
        return distance / self.mag_yield

# Gets the yield point
def get_yield(data_dict:dict, x_label:str, y_label:str):
    
    # Initialise
    x_offset = 0.2/100.0
    x_list = data_dict[x_label]
    y_list = data_dict[y_label]
    youngs = y_list[1] / x_list[1]
    
    # Interpolate
    iff = inter.interp1d(x_list, y_list, bounds_error=False, fill_value=0)
    x_yield = opt.brentq(lambda x: iff(x) - youngs * (x - x_offset), 0.0, np.max(x_list))
    y_yield = float(iff(x_yield))
    return x_yield, y_yield
