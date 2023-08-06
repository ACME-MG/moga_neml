"""
 Title:         Interpolator
 Description:   For interpolating curves
 Author:        Janzen Choi

"""

# Libraries
from scipy.interpolate import splev, splrep, splder
from moga_neml._maths.curve import get_thinned_list

# The Interpolator Class
class Interpolator:

    # Constructor
    def __init__(self, x_list:list, y_list:list, resolution:int=50, smooth:bool=False):
        self.thin_x_list = get_thinned_list(x_list, resolution)
        self.thin_y_list = get_thinned_list(y_list, resolution)
        smooth_amount = resolution if smooth else 0
        self.spl = splrep(self.thin_x_list, self.thin_y_list, s=smooth_amount)
    
    # Convert to derivative
    def differentiate(self) -> None:
        self.spl = splder(self.spl)

    # Evaluate
    def evaluate(self, x_list:list) -> list:
        return list(splev(x_list, self.spl))
