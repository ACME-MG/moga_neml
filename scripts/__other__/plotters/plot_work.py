# Libraries
import matplotlib.pyplot as plt
import numpy as np, math
from copy import deepcopy
from scipy.interpolate import splev, splrep, splder

# The Interpolator Class
class Interpolator:

    # Constructor
    def __init__(self, x_list, y_list, resolution=50, smooth=False):
        thin_x_list = get_thinned_list(x_list, resolution)
        thin_y_list = get_thinned_list(y_list, resolution)
        smooth_amount = resolution if smooth else 0
        self.spl = splrep(thin_x_list, thin_y_list, s=smooth_amount)
    
    # Convert to derivative
    def differentiate(self):
        self.spl = splder(self.spl)

    # Evaluate
    def evaluate(self, x_list):
        return list(splev(x_list, self.spl))

# For differentiating a curve
def differentiate_curve(curve, x_label, y_label):
    curve = deepcopy(curve)
    interpolator = Interpolator(curve[x_label], curve[y_label])
    interpolator.differentiate()
    curve[y_label] = interpolator.evaluate(curve[x_label])
    return curve

# Returns a thinned list
def get_thinned_list(unthinned_list:list, density:int) -> list:
    src_data_size = len(unthinned_list)
    step_size = src_data_size / density
    thin_indexes = [math.floor(step_size*i) for i in range(1, density - 1)]
    thin_indexes = [0] + thin_indexes + [src_data_size - 1]
    return [unthinned_list[i] for i in thin_indexes]

# Tries to float cast a value
def try_float_cast(value:str) -> float:
    try:
        return float(value)
    except:
        return value

# Converts CSV data into a curve dict
def get_curve_dict(headers:list, data:list) -> dict:
    
    # Get indexes of data
    list_indexes = [i for i in range(len(data[2])) if data[2][i] != ""]
    info_indexes = [i for i in range(len(data[2])) if data[2][i] == ""]
    
    # Create curve
    curve = {}
    for index in list_indexes:
        value_list = [float(d[index]) for d in data]
        value_list = get_thinned_list(value_list, 200)
        curve[headers[index]] = value_list
    for index in info_indexes:
        curve[headers[index]] = try_float_cast(data[0][index])

    # Return curve
    return curve

# Gets the data for the work rate and work
def get_work(curve:dict, w_0:float, w_1:float) -> tuple:
    
    # Get stress
    if curve["type"] == "creep":
        curve["stress"] = [curve["stress"]] * len(curve["strain"])
    
    # Calculate work rate
    strain_rate_list = differentiate_curve(curve, "time", "strain")["strain"]
    stress_rate_list = differentiate_curve(curve, "time", "stress")["stress"]
    work_rate_function = lambda stress, strain_rate, stress_rate, youngs : stress*(strain_rate - stress_rate/youngs)
    work_rate_list = [work_rate_function(curve["stress"][i], strain_rate_list[i], stress_rate_list[i], curve["youngs"])
                      for i in range(len(curve["stress"]))]

    # Calculate work
    work_function = lambda work_rate : w_0 * work_rate + w_1
    work_rate_list = [math.log10(work_rate) if work_rate > 0 else 0 for work_rate in work_rate_list]
    work_list = [work_function(work_rate) for work_rate in work_rate_list]
    
    # Return
    # return curve["time"], work_rate_list
    return work_rate_list, work_list

# Initialise
work_failure_list = []
avg_work_rate_list = []

# File names
file_path_list = [
    # "../../data/creep/inl_1/AirBase_900_36_G22.csv",
    # "../../data/creep/inl_1/AirBase_900_31_G50.csv",
    # "../../data/creep/inl_1/AirBase_900_28_G45.csv",
    # "../../data/creep/inl_1/AirBase_900_26_G59_unox.csv",
    "../../data/tensile/inl/AirBase_900_D10.csv",
]

# Constants
# w_0, w_1 = 0.3684, 3.2014
w_0, w_1 = 0.9971, 3.8264

# Iterate through file paths
for file_path in file_path_list:

    # Read file
    with open(file_path, "r") as file:
        headers = file.readline().replace("\n","").split(",")
        data = [line.replace("\n","").split(",") for line in file.readlines()]
        curve = get_curve_dict(headers, data)
    
    # Get work rate and work
    work_rate_list, work_list = get_work(curve, w_0, w_1)
    plt.scatter(work_rate_list, work_list)

# plt.yscale("log")
# plt.xscale("log")
plt.savefig("plot")