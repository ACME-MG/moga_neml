"""
 Title:         The x_peaks objective function
 Description:   The objective function for getting the wavelength of a periodic curve
 Author:        Janzen Choi

 """

# Libraries
import math, numpy as np
from moga_neml.errors.__error__ import __Error__
from moga_neml._maths.derivative import get_stationary_points

# The Error class
class Error(__Error__):
    
    # Runs at the start, once (optional)
    def initialise(self):
        self.enforce_data_type("cyclic")
        exp_data = self.get_exp_data()
        self.x_label = self.get_x_label()
        self.y_label = self.get_y_label()
        self.exp_x_peaks = get_x_peaks(exp_data, self.x_label, self.y_label)
        self.avg_exp_x = np.average(self.exp_x_peaks)

    # Computes the NRMSE value
    def get_value(self, prd_data:dict) -> float:
        prd_x_peaks = get_x_peaks(prd_data, self.x_label, self.y_label)
        min_peaks = min(len(self.exp_x_peaks), len(prd_x_peaks))
        dist_list = [math.pow(self.exp_x_peaks[i] - prd_x_peaks[i], 2) for i in range(min_peaks)]
        return math.sqrt(np.average(dist_list)) / self.avg_exp_x

# Returns the number of peaks
def get_x_peaks(data_dict:dict, x_label:str, y_label:str) -> int:
    sp_list = get_stationary_points(data_dict, x_label, y_label, 0.2, 0.9)
    x_peaks = [sp[x_label] for sp in sp_list]
    return x_peaks
