"""
 Title:         Derivative
 Description:   For interpolating and differentating curves
 Author:        Janzen Choi

"""
# Libraries
import matplotlib.pyplot as plt
from copy import deepcopy
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
        self.thin_x_list, self.thin_y_list = get_bfd(self.thin_x_list, self.thin_y_list)

    # Evaluate
    def evaluate(self, x_list:list) -> None:
        return list(splev(x_list, self.spl))

    # Tests the interpolation by plotting
    def __test__(self, path:str) -> None:
        plt.scatter(self.thin_x_list, self.thin_y_list, color="b")
        y_list = self.evaluate(self.thin_x_list)
        plt.plot(self.thin_x_list, y_list, color="r")
        plt.savefig(path)
        plt.cla()

# Returns the derivative via backward finite difference
def get_bfd(x_list:list, y_list:list) -> tuple:
    new_x_list, dy_list = [], []
    for i in range(1,len(x_list)):
        if x_list[i] > x_list[i-1]:
            new_x_list.append(x_list[i])
            dy_list.append((y_list[i]-y_list[i-1])/(x_list[i]-x_list[i-1]))
    return new_x_list, dy_list

# Removes data after the Xth local minima/maxima
def remove_after_sp(curve:dict, nature:str, x_label:str, y_label:str, window:int, acceptance:int, nominal:int=0) -> dict:

    # Get all stationary points
    curve = deepcopy(curve)
    d_curve = differentiate_curve(curve, x_label, y_label)
    sp_list = get_stationary_points(d_curve, x_label, y_label, window, acceptance)
    # print([sp for sp in sp_list if sp["nature"] == nature])
    
    # Get all stationary points
    sp_list = [sp for sp in sp_list if sp["nature"] == nature]
    if len(sp_list) <= nominal:
        return curve
    sp = sp_list[nominal]

    # Remove data after local stationary point
    curve[x_label] = [curve[x_label][i] for i in range(len(curve[x_label])) if i < sp["index"]]
    curve[y_label] = [curve[y_label][i] for i in range(len(curve[y_label])) if i < sp["index"]]
    return curve

# Returns a list of the stationary points and their nature (of a noisy curve)
def get_stationary_points(curve:dict, x_label:str, y_label:str, window:int, acceptance:int) -> list:

    # Initialise
    d_curve = differentiate_curve(curve, x_label, y_label)
    dy_label = f"d_{y_label}"
    sp_list = []

    # Gets the locations where the derivative passes through the x axis
    for i in range(len(d_curve[x_label])-1):
        if ((d_curve[y_label][i] <= 0 and d_curve[y_label][i+1] >= 0) or (d_curve[y_label][i] >= 0 and d_curve[y_label][i+1] <= 0)):
            sp_list.append({
                x_label:  curve[x_label][i],
                y_label:  curve[y_label][i],
                dy_label: d_curve[y_label][i],
                "index":  i,
                "nature": get_sp_nature(d_curve[y_label], i, window, acceptance)
            })
    
    # Return list of dictionaries
    return sp_list

# Checks the left and right of a list of values to determine if a point is stationary
def get_sp_nature(dy_list:list, index:int, window=0.1, acceptance=0.9) -> str:
    
    # Redefine window as a fraction of the data size
    window_abs = round(len(dy_list) * window)
    
    # Determine gradient on the left
    dy_left = dy_list[index-window_abs:index]
    left_pos_size = len([dy for dy in dy_left if dy > 0])
    left_pos = left_pos_size > window_abs*acceptance
    left_neg = left_pos_size < window_abs*(1-acceptance)
    
    # Determine gradient on the right
    dy_right = dy_list[index:index+window_abs+1]
    right_pos_size = len([dy for dy in dy_right if dy > 0])
    right_pos = right_pos_size > window_abs*acceptance
    right_neg = right_pos_size < window_abs*(1-acceptance)

    # Determine nature
    if left_pos and right_neg:
        return "max"
    elif left_neg and right_pos:
        return "min"
    else:
        return "uncertain"
    
# For differentiating a curve
def differentiate_curve(curve:dict, x_label:str, y_label:str) -> dict:
    curve = deepcopy(curve)
    interpolator = Interpolator(curve[x_label], curve[y_label])
    interpolator.differentiate()
    curve[y_label] = interpolator.evaluate(curve[x_label])
    return curve