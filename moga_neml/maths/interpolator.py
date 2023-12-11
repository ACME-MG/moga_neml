"""
 Title:         Interpolator
 Description:   For interpolating curves
 Author:        Janzen Choi

"""

# Libraries
from scipy.interpolate import splev, splrep, splder
from moga_neml.maths.data import get_thinned_list

# The Interpolator Class
class Interpolator:

    def __init__(self, x_list:list, y_list:list, resolution:int=50, smooth:bool=False):
        """
        Class for interpolating two lists of values

        Parameters:
        * `x_list`:     List of x values
        * `y_list`:     List of y values
        * `resolution`: The resolution used for the interpolation
        * `smooth`:     Whether to smooth the interpolation
        """
        is_thick = len(x_list) > resolution
        thin_x_list = get_thinned_list(x_list, resolution) if is_thick else x_list
        thin_y_list = get_thinned_list(y_list, resolution) if is_thick else y_list
        smooth_amount = resolution if smooth else 0
        self.spl = splrep(thin_x_list, thin_y_list, s=smooth_amount)
    
    def differentiate(self) -> None:
        """
        Differentiate the interpolator
        """
        self.spl = splder(self.spl)

    def evaluate(self, x_list:list) -> list:
        """
        Run the interpolator for specific values

        Parameters
        * `x_list`: The list of x values

        Returns the evaluated values
        """
        return list(splev(x_list, self.spl))
