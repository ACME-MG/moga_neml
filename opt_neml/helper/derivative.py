"""
 Title:         Derivative
 Description:   For interpolating and differentating curves
 Author:        Janzen Choi

"""
# Libraries
import matplotlib.pyplot as plt
from copy import deepcopy
from scipy.interpolate import splev, splrep, splder
from opt_neml.helper.curve import get_thin_indexes

# The Interpolator Class
class Interpolator:

    # Constructor
    def __init__(self, x_list, y_list, resolution=50, smooth=False):
        thin_indexes = get_thin_indexes(len(x_list), resolution)
        self.thin_x_list = [x_list[i] for i in thin_indexes]
        self.thin_y_list = [y_list[i] for i in thin_indexes]
        smooth_amount = resolution if smooth else 0
        self.spl = splrep(self.thin_x_list, self.thin_y_list, s=smooth_amount)
    
    # Convert to derivative
    def differentiate(self):
        self.spl = splder(self.spl)
        self.thin_x_list, self.thin_y_list = get_bfd(self.thin_x_list, self.thin_y_list)

    # Evaluate
    def evaluate(self, x_list):
        return list(splev(x_list, self.spl))

    # Tests the interpolation by plotting
    def __test__(self, path):
        plt.scatter(self.thin_x_list, self.thin_y_list, color="b")
        y_list = self.evaluate(self.thin_x_list)
        plt.plot(self.thin_x_list, y_list, color="r")
        plt.savefig(path)
        plt.cla()

# Returns the derivative via backward finite difference
def get_bfd(x_list, y_list):
    new_x_list, dy_list = [], []
    for i in range(1,len(x_list)):
        if x_list[i] > x_list[i-1]:
            new_x_list.append(x_list[i])
            dy_list.append((y_list[i]-y_list[i-1])/(x_list[i]-x_list[i-1]))
    return new_x_list, dy_list

# Removes data after the Xth local minima/maxima
def remove_after_sp(curve, nature, window, acceptance, nominal=0):

    # Get all stationary points
    curve = deepcopy(curve)
    d_curve = differentiate_curve(curve)
    sp_list = get_stationary_points(d_curve, window, acceptance)
    
    # Get all stationary points
    sp_list = [sp for sp in sp_list if sp["nature"] == nature]
    if len(sp_list) == nominal:
        return curve
    sp = sp_list[nominal]

    # Remove data after local stationary point
    curve["x"] = [curve["x"][i] for i in range(len(curve["x"])) if i < sp["index"]]
    curve["y"] = [curve["y"][i] for i in range(len(curve["y"])) if i < sp["index"]]
    return curve

# Returns a list of the stationary points and their nature (of a noisy curve)
def get_stationary_points(curve, window, acceptance):

    # Initialise
    d_curve = differentiate_curve(curve)
    sp_list = []

    # Gets the locations where the derivative passes through the x axis
    for i in range(len(d_curve["x"])-1):
        if ((d_curve["y"][i] <= 0 and d_curve["y"][i+1] >= 0) or (d_curve["y"][i] >= 0 and d_curve["y"][i+1] <= 0)):
            sp_list.append({
                "x":      curve["x"][i],
                "y":      curve["y"][i],
                "dy":     d_curve["y"][i],
                "index":  i,
                "nature": get_sp_nature(d_curve["y"], i, window, acceptance)
            })
    
    # Return list of dictionaries
    return sp_list

# Checks the left and right of a list of values to determine if a point is stationary
def get_sp_nature(dy_list, index, window=200, acceptance=0.9):
    
    # Determine gradient on the left
    dy_left = dy_list[index-window:index]
    left_pos_size = len([dy for dy in dy_left if dy > 0])
    left_pos = left_pos_size > window*acceptance
    left_neg = left_pos_size < window*(1-acceptance)
    
    # Determine gradient on the right
    dy_right = dy_list[index:index+window+1]
    right_pos_size = len([dy for dy in dy_right if dy > 0])
    right_pos = right_pos_size > window*acceptance
    right_neg = right_pos_size < window*(1-acceptance)

    # Determine nature
    if left_pos and right_neg:
        return "max"
    elif left_neg and right_pos:
        return "min"
    else:
        return "uncertain"
    
# For differentiating a curve
def differentiate_curve(curve):
    curve = deepcopy(curve)
    interpolator = Interpolator(curve["x"], curve["y"])
    interpolator.differentiate()
    curve["y"] = interpolator.evaluate(curve["x"])
    return curve