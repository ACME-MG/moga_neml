"""
 Title:         The x_peaks objective function
 Description:   The objective function for getting the wavelength of a periodic curve
 Author:        Janzen Choi

 """

# Libraries
import numpy as np
import moga_neml.errors.__error__ as error
from moga_neml._maths.derivative import get_stationary_points

# The Error class
class Error(error.__Error__):
    
    # Runs at the start, once (optional)
    def prepare(self):
        exp_curve = self.get_exp_curve()
        exp_stationary_points = get_stationary_points(exp_curve, 100, 0.9)
        self.exp_x_peaks = [esp["x"] for esp in exp_stationary_points]

    # Computes the error value
    def get_value(self, prd_curve:dict) -> float:
        prd_stationary_points = get_stationary_points(prd_curve, 100, 0.9)
        prd_x_peaks = [psp["x"] for psp in prd_stationary_points]
        min_peaks = min(len(self.exp_x_peaks), len(prd_x_peaks))
        return np.average([abs((self.exp_x_peaks[i] - prd_x_peaks[i]) / self.exp_x_peaks[i]) for i in range(min_peaks)])